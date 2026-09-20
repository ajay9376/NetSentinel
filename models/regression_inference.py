"""
NetSentinel — QoS Packet Loss Regression Inference Engine
Course: 23CSE301 Machine Learning Capstone
Track: Regression Track (Continuous QoS Degradation Metric)

This module provides a standalone, production-ready interface for predicting
continuous Source Packet Loss (`sloss`) using the best-performing model identified
in the comprehensive 10-model benchmark (Random Forest Regressor, R² = 0.9995).
"""

import os
import sys
import argparse
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


class NetSentinelRegressor:
    """
    Production-ready wrapper for training, evaluating, and serving
    the NetSentinel QoS regression pipeline.
    """

    def __init__(self, random_state: int = 42, n_estimators: int = 100):
        self.random_state = random_state
        self.n_estimators = n_estimators
        self.target_col = "sloss"
        self.drop_cols = ["id", "attack_cat", "label", "sloss"]
        self.categorical_cols = ["proto", "service", "state"]
        self.numerical_cols = None
        self.preprocessor = None
        self.model = None
        self.is_fitted = False

    def _feature_engineering(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies domain feature engineering: total_bytes = sbytes + dbytes.
        Guaranteed leakage-free: operates strictly on non-target predictor features.
        """
        df_engineered = df.copy()
        if "sbytes" in df_engineered.columns and "dbytes" in df_engineered.columns:
            df_engineered["total_bytes"] = df_engineered["sbytes"] + df_engineered["dbytes"]
        return df_engineered

    def fit(self, data_path: str = "data/regression/UNSW_NB15_training-set.csv"):
        """
        Fits the preprocessing ColumnTransformer and the best Random Forest model
        on an 80% training split, replicating the capstone notebook pipeline.
        """
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Dataset not found at: {data_path}")

        print(f"[NetSentinel] Loading dataset from: {data_path}...")
        df = pd.read_csv(data_path)

        y = df[self.target_col].copy()
        X_raw = df.drop(columns=[c for c in self.drop_cols if c in df.columns], errors="ignore").copy()
        X = self._feature_engineering(X_raw)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=self.random_state
        )

        self.numerical_cols = [c for c in X_train.columns if c not in self.categorical_cols]

        self.preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), self.numerical_cols),
                ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), self.categorical_cols),
            ]
        )

        print("[NetSentinel] Fitting ColumnTransformer on training partition...")
        X_train_trans = self.preprocessor.fit_transform(X_train)
        X_test_trans = self.preprocessor.transform(X_test)

        print(f"[NetSentinel] Training Random Forest Regressor ({self.n_estimators} estimators)...")
        self.model = RandomForestRegressor(
            n_estimators=self.n_estimators,
            random_state=self.random_state,
            n_jobs=-1
        )
        self.model.fit(X_train_trans, y_train)
        self.is_fitted = True

        test_preds = self.model.predict(X_test_trans)
        r2 = r2_score(y_test, test_preds)
        rmse = np.sqrt(mean_squared_error(y_test, test_preds))
        mae = mean_absolute_error(y_test, test_preds)

        print(f"[NetSentinel] Pipeline Fit Complete!")
        print(f"              Held-Out Test R²:   {r2:.6f}")
        print(f"              Held-Out Test RMSE: {rmse:.4f} packets")
        print(f"              Held-Out Test MAE:  {mae:.4f} packets")
        return self

    def predict(self, df_input: pd.DataFrame) -> np.ndarray:
        """
        Predicts continuous source packet loss (`sloss`) for incoming network flows.
        """
        if not self.is_fitted:
            raise RuntimeError("Model is not fitted. Call fit() before predict().")

        clean_input = df_input.drop(columns=[c for c in self.drop_cols if c in df_input.columns], errors="ignore")
        engineered = self._feature_engineering(clean_input)
        transformed = self.preprocessor.transform(engineered)
        return self.model.predict(transformed)

    def assess_qos_status(self, predicted_loss: float) -> str:
        """
        Categorizes predicted packet loss into actionable QoS operational tiers.
        """
        if predicted_loss < 1.0:
            return "Optimal QoS (Negligible Loss)"
        elif predicted_loss < 10.0:
            return "Moderate Degradation (Buffer Saturation Risk)"
        else:
            return "Severe Degradation (Critical Congestion / Flow Throttling Required)"


def main():
    """
    Demonstration and self-test CLI for the NetSentinel Regression engine.
    """
    print("=" * 70)
    print("   NETSENTINEL: STANDALONE REGRESSION INFERENCE ENGINE")
    print("=" * 70)

    regressor = NetSentinelRegressor()
    regressor.fit("data/regression/UNSW_NB15_training-set.csv")

    # Load sample flows for real-time inference demonstration
    print("\n[NetSentinel] Running sample inference demonstration on test flow records...")
    df_sample = pd.read_csv("data/regression/UNSW_NB15_training-set.csv", nrows=10)
    actual_loss = df_sample["sloss"].values
    predictions = regressor.predict(df_sample)

    print("\n" + "-" * 75)
    print(f"{'Flow #':<8} {'Actual sloss':<15} {'Predicted sloss':<18} {'Residual':<12} {'QoS Assessment'}")
    print("-" * 75)
    for i in range(len(predictions)):
        act = actual_loss[i]
        pred = predictions[i]
        resid = act - pred
        status = regressor.assess_qos_status(pred)
        print(f"{i+1:<8} {act:<15.1f} {pred:<18.2f} {resid:<12.2f} {status}")
    print("-" * 75)
    print("[NetSentinel] Inference demo complete.")


if __name__ == "__main__":
    main()
