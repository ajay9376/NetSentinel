"""
Model Loader & Inference Engine for NetSentinel
Handles serialized bundle loading and production inference with anti-leakage guards.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from app.config import MODELS_DIR, BENCHMARKS_PATH, THREAT_SEVERITY

@st.cache_resource(show_spinner=False)
def load_classification_bundle():
    """Loads fitted classification bundle containing models, imputer, scaler, and metadata."""
    bundle_path = os.path.join(MODELS_DIR, "classification_bundle.joblib")
    if os.path.exists(bundle_path):
        try:
            return joblib.load(bundle_path)
        except Exception as e:
            st.error(f"Error loading classification bundle: {e}")
            return None
    return None

@st.cache_resource(show_spinner=False)
def load_regression_bundle():
    """Loads fitted regression bundle containing models, encoders, scalers, and metadata."""
    bundle_path = os.path.join(MODELS_DIR, "regression_bundle.joblib")
    if os.path.exists(bundle_path):
        try:
            return joblib.load(bundle_path)
        except Exception as e:
            st.error(f"Error loading regression bundle: {e}")
            return None
    return None

@st.cache_resource(show_spinner=False)
def load_clustering_bundle():
    """Loads fitted clustering bundle containing KMeans, PCA, scaler, and sample projections."""
    bundle_path = os.path.join(MODELS_DIR, "clustering_bundle.joblib")
    if os.path.exists(bundle_path):
        try:
            return joblib.load(bundle_path)
        except Exception as e:
            st.error(f"Error loading clustering bundle: {e}")
            return None
    return None

@st.cache_data(show_spinner=False)
def load_benchmarks():
    """Loads verified benchmark metrics extracted from the 3 capstone notebooks."""
    if os.path.exists(BENCHMARKS_PATH):
        try:
            with open(BENCHMARKS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.warning(f"Failed to read benchmarks cache: {e}")
    return {"regression": [], "classification": [], "clustering": []}

def run_classification_inference(df_input: pd.DataFrame, model_name: str = "Random Forest"):
    """
    Executes real inference on network traffic flows using the saved classification pipeline.
    Preserves exact training transformations without target leakage.
    """
    bundle = load_classification_bundle()
    if bundle is None:
        raise RuntimeError("Classification model bundle not found in models/ directory.")

    features = bundle["features"]
    imputer = bundle["imputer"]
    scaler = bundle["scaler"]
    models = bundle["models"]

    if model_name not in models:
        model_name = "Random Forest"
    selected_model = models[model_name]

    df_proc = df_input.copy()
    df_proc.columns = df_proc.columns.str.strip()

    # Drop target column if present to guarantee no data leakage
    if "Label" in df_proc.columns:
        df_proc = df_proc.drop(columns=["Label"])

    # Feature Engineering (reproduce training pipeline)
    if "Total Fwd Packets" in df_proc.columns and "Total Backward Packets" in df_proc.columns:
        if "Total Packets" not in df_proc.columns:
            df_proc["Total Packets"] = df_proc["Total Fwd Packets"] + df_proc["Total Backward Packets"]

    if "Total Length of Fwd Packets" in df_proc.columns and "Total Length of Bwd Packets" in df_proc.columns:
        if "Total Length of Packets" not in df_proc.columns:
            df_proc["Total Length of Packets"] = df_proc["Total Length of Fwd Packets"] + df_proc["Total Length of Bwd Packets"]

    # Check for missing expected features
    missing_cols = [c for c in features if c not in df_proc.columns]
    unexpected_cols = [c for c in df_proc.columns if c not in features]

    # Impute missing columns with zeros if minor discrepancy, or align
    for c in missing_cols:
        df_proc[c] = 0.0

    # Align column order strictly to model feature space
    X_input = df_proc[features].copy()

    # Apply fitted training-time imputer and standard scaler
    X_imp = imputer.transform(X_input)
    X_scaled = scaler.transform(X_imp)

    # Generate predictions
    preds = selected_model.predict(X_scaled)

    # Generate prediction probabilities if supported
    probs = None
    confidences = []
    if hasattr(selected_model, "predict_proba"):
        probs = selected_model.predict_proba(X_scaled)
        confidences = np.max(probs, axis=1) * 100
    else:
        confidences = [100.0] * len(preds)

    # Prepare result dataframe
    results_df = df_input.copy()
    results_df["Predicted_Threat"] = preds
    results_df["Confidence (%)"] = np.round(confidences, 2)
    
    # Map severity and recommended action
    severities = []
    actions = []
    for p in preds:
        info = THREAT_SEVERITY.get(p, {"level": "High", "action": "Inspect Packet Payload"})
        severities.append(info["level"])
        actions.append(info["action"])
        
    results_df["Threat_Level"] = severities
    results_df["Recommended_Action"] = actions

    summary = {
        "total_analyzed": len(df_input),
        "benign_count": int(np.sum(preds == "BENIGN")),
        "threat_count": int(np.sum(preds != "BENIGN")),
        "missing_features_handled": len(missing_cols),
        "model_used": model_name,
        "class_counts": pd.Series(preds).value_counts().to_dict(),
        "probabilities": probs,
        "classes": list(selected_model.classes_) if hasattr(selected_model, "classes_") else []
    }

    return results_df, summary

def run_regression_inference(df_input: pd.DataFrame):
    """
    Executes real inference on network connection flows predicting packet loss 'sloss'.
    """
    bundle = load_regression_bundle()
    if bundle is None:
        raise RuntimeError("Regression model bundle not found in models/ directory.")

    num_cols = bundle["num_cols"]
    cat_cols = bundle["cat_cols"]
    num_imputer = bundle["num_imputer"]
    cat_imputer = bundle["cat_imputer"]
    encoder = bundle["encoder"]
    scaler = bundle["scaler"]
    model = bundle["model"]

    df_proc = df_input.copy()
    if "sloss" in df_proc.columns:
        df_proc = df_proc.drop(columns=["sloss"])

    # Feature engineering
    if "sbytes" in df_proc.columns and "dbytes" in df_proc.columns:
        if "total_bytes" not in df_proc.columns:
            df_proc["total_bytes"] = df_proc["sbytes"] + df_proc["dbytes"]
    if "spkts" in df_proc.columns and "dpkts" in df_proc.columns:
        if "total_packets" not in df_proc.columns:
            df_proc["total_packets"] = df_proc["spkts"] + df_proc["dpkts"]

    for c in num_cols:
        if c not in df_proc.columns:
            df_proc[c] = 0.0
    for c in cat_cols:
        if c not in df_proc.columns:
            df_proc[c] = "unknown"

    X_num = num_imputer.transform(df_proc[num_cols])
    X_cat = cat_imputer.transform(df_proc[cat_cols])
    X_cat_enc = encoder.transform(X_cat)
    X_all = np.hstack([X_num, X_cat_enc])
    X_scaled = scaler.transform(X_all)

    preds = model.predict(X_scaled)
    preds = np.clip(preds, 0, None)  # packet loss cannot be negative

    results_df = df_input.copy()
    results_df["Predicted_sloss"] = np.round(preds, 3)
    results_df["QoS_Health"] = [
        "Optimal" if p < 2 else ("Degraded" if p < 10 else "Critical Loss") for p in preds
    ]
    return results_df, preds
