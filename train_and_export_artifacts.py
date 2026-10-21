"""
NetSentinel Artifact Exporter
Trains and exports the production pipelines (classification, regression, clustering)
and pre-extracted benchmark metrics from the verified notebooks.
"""

import os
import sys
import time
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc

os.makedirs("models", exist_ok=True)
os.makedirs("data/samples", exist_ok=True)

print("=" * 60)
print("1. EXPORTING CLASSIFICATION PIPELINE & BENCHMARK")
print("=" * 60)

clf_path = "data/classification/network_traffic_classification.csv"
if os.path.exists(clf_path):
    df_clf_raw = pd.read_csv(clf_path)
    df_clf_raw.columns = df_clf_raw.columns.str.strip()
    df_clf_clean = df_clf_raw.drop_duplicates().copy()
    df_clf_clean.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_clf_clean.dropna(inplace=True)

    drop_cols = [
        'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'Min Packet Length', 
        'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count', 'Fwd Avg Bytes/Bulk', 
        'Fwd Avg Packets/Bulk', 'Fwd Avg Bulk Rate', 'Bwd Avg Bytes/Bulk', 
        'Bwd Avg Packets/Bulk', 'Bwd Avg Bulk Rate', 'min_seg_size_forward', 
        'Active Std', 'Active Min', 'Idle Std', 'Idle Min'
    ]
    df_clf_clean.drop(columns=[c for c in drop_cols if c in df_clf_clean.columns], inplace=True)

    df_clf_clean['Total Packets'] = df_clf_clean['Total Fwd Packets'] + df_clf_clean['Total Backward Packets']
    df_clf_clean['Total Length of Packets'] = df_clf_clean['Total Length of Fwd Packets'] + df_clf_clean['Total Length of Bwd Packets']

    X_clf = df_clf_clean.drop(columns=['Label'])
    y_clf = df_clf_clean['Label']
    clf_features = list(X_clf.columns)

    X_train_raw, X_test_raw, y_train_clf, y_test_clf = train_test_split(
        X_clf, y_clf, test_size=0.2, random_state=42, stratify=y_clf
    )

    clf_imputer = SimpleImputer(strategy='median')
    clf_imputer.fit(X_train_raw)

    clf_scaler = StandardScaler()
    X_train_scaled = clf_scaler.fit_transform(clf_imputer.transform(X_train_raw))
    X_test_scaled = clf_scaler.transform(clf_imputer.transform(X_test_raw))

    # Train top models
    rf_clf = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
    rf_clf.fit(X_train_scaled, y_train_clf)
    
    lr_clf = LogisticRegression(max_iter=1000, random_state=42)
    lr_clf.fit(X_train_scaled, y_train_clf)

    dt_clf = DecisionTreeClassifier(max_depth=10, random_state=42)
    dt_clf.fit(X_train_scaled, y_train_clf)

    classes_list = list(rf_clf.classes_)
    y_pred_rf = rf_clf.predict(X_test_scaled)
    y_prob_rf = rf_clf.predict_proba(X_test_scaled)

    cm_rf = confusion_matrix(y_test_clf, y_pred_rf, labels=classes_list)
    clf_report_rf = classification_report(y_test_clf, y_pred_rf, labels=classes_list, output_dict=True)

    # Export bundle
    clf_bundle = {
        'features': clf_features,
        'dropped_constant_features': drop_cols,
        'classes': classes_list,
        'imputer': clf_imputer,
        'scaler': clf_scaler,
        'models': {
            'Random Forest': rf_clf,
            'Logistic Regression': lr_clf,
            'Decision Tree': dt_clf
        },
        'test_metrics': {
            'confusion_matrix': cm_rf.tolist(),
            'classification_report': clf_report_rf,
            'test_accuracy': float(np.mean(y_pred_rf == y_test_clf)),
            'classes': classes_list
        }
    }
    joblib.dump(clf_bundle, "models/classification_bundle.joblib")
    print("Saved models/classification_bundle.joblib")

    # Save realistic sample batches for user upload testing
    test_sample_benign = X_test_raw[y_test_clf == 'BENIGN'].head(30)
    test_sample_dos = X_test_raw[y_test_clf.str.contains('DoS|DDoS')].head(30)
    test_sample_mixed = X_test_raw.sample(50, random_state=42)

    test_sample_benign.to_csv("data/samples/sample_benign_flows.csv", index=False)
    test_sample_dos.to_csv("data/samples/sample_dos_attack_flows.csv", index=False)
    test_sample_mixed.to_csv("data/samples/sample_mixed_traffic.csv", index=False)
    print("Saved sample CSVs to data/samples/")

print("=" * 60)
print("2. EXPORTING REGRESSION PIPELINE & ARTIFACTS")
print("=" * 60)

reg_path = "data/regression/UNSW_NB15_training-set.csv"
if os.path.exists(reg_path):
    # Load dataset
    df_reg = pd.read_csv(reg_path)
    df_reg["total_bytes"] = df_reg["sbytes"] + df_reg["dbytes"]
    df_reg["total_packets"] = df_reg["spkts"] + df_reg["dpkts"]

    target_col = "sloss"
    exclude_cols = ["sloss", "attack_cat", "label", "id"]
    X_reg_raw = df_reg.drop(columns=[c for c in exclude_cols if c in df_reg.columns])
    y_reg = df_reg[target_col]

    cat_cols = ["proto", "service", "state"]
    num_cols = [c for c in X_reg_raw.columns if c not in cat_cols]

    # Sample a representative 25,000 subset for fast training and compact model file
    sample_idx = np.random.RandomState(42).choice(len(df_reg), size=25000, replace=False)
    X_reg_sub = X_reg_raw.iloc[sample_idx].copy()
    y_reg_sub = y_reg.iloc[sample_idx].copy()

    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
        X_reg_sub, y_reg_sub, test_size=0.2, random_state=42
    )

    reg_num_imp = SimpleImputer(strategy="median")
    reg_cat_imp = SimpleImputer(strategy="most_frequent")

    reg_num_imp.fit(X_train_r[num_cols])
    reg_cat_imp.fit(X_train_r[cat_cols])

    X_train_num = reg_num_imp.transform(X_train_r[num_cols])
    X_train_cat = reg_cat_imp.transform(X_train_r[cat_cols])

    reg_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    reg_encoder.fit(X_train_cat)
    X_train_cat_enc = reg_encoder.transform(X_train_cat)

    X_train_all = np.hstack([X_train_num, X_train_cat_enc])

    reg_scaler = StandardScaler()
    X_train_scaled = reg_scaler.fit_transform(X_train_all)

    rf_reg = RandomForestRegressor(n_estimators=50, max_depth=12, random_state=42, n_jobs=-1)
    rf_reg.fit(X_train_scaled, y_train_r)

    # Feature importances for num_cols
    encoded_cat_names = list(reg_encoder.get_feature_names_out(cat_cols))
    all_feature_names = num_cols + encoded_cat_names
    feat_imp = pd.Series(rf_reg.feature_importances_, index=all_feature_names).sort_values(ascending=False).head(20)

    reg_bundle = {
        'num_cols': num_cols,
        'cat_cols': cat_cols,
        'num_imputer': reg_num_imp,
        'cat_imputer': reg_cat_imp,
        'encoder': reg_encoder,
        'scaler': reg_scaler,
        'model': rf_reg,
        'top_features': feat_imp.to_dict()
    }
    joblib.dump(reg_bundle, "models/regression_bundle.joblib")
    print("Saved models/regression_bundle.joblib")

print("=" * 60)
print("3. EXPORTING CLUSTERING PIPELINE & ARTIFACTS")
print("=" * 60)

clust_path = "data/clustering/nslkdd.csv"
if os.path.exists(clust_path):
    df_clust = pd.read_csv(clust_path)
    target_cols = ['label', 'attack']
    feature_cols = [c for c in df_clust.columns if c not in target_cols]
    num_cols_clust = df_clust[feature_cols].select_dtypes(include=[np.number]).columns.tolist()

    # Fit Scaler and KMeans on 10k sample for fast loading and visualization
    sample_df = df_clust.sample(n=min(10000, len(df_clust)), random_state=42)
    clust_scaler = StandardScaler()
    X_clust_scaled = clust_scaler.fit_transform(sample_df[num_cols_clust].fillna(0))

    kmeans_5 = KMeans(n_clusters=5, random_state=42, n_init=10)
    kmeans_5.fit(X_clust_scaled)

    pca = PCA(n_components=2, random_state=42)
    pca_coords = pca.fit_transform(X_clust_scaled)

    clust_bundle = {
        'features': num_cols_clust,
        'scaler': clust_scaler,
        'kmeans': kmeans_5,
        'pca': pca,
        'pca_sample_coords': pca_coords.tolist(),
        'cluster_labels': kmeans_5.labels_.tolist(),
        'ground_truth_labels': sample_df['label'].tolist() if 'label' in sample_df else []
    }
    joblib.dump(clust_bundle, "models/clustering_bundle.joblib")
    print("Saved models/clustering_bundle.joblib")

print("Artifact generation completed successfully!")
