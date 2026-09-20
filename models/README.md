# NetSentinel Model Registry & Inference Documentation

## Overview
This directory houses the standalone inference utilities, model specifications, and serving architecture for the **NetSentinel** machine learning capstone framework.

---

## Track 1: Regression (QoS Packet Loss Prediction)

### Champion Model Specification
- **Model**: **Random Forest Regressor** (Ensemble Bagging)
- **Primary Objective**: Predict continuous Source Packet Loss (`sloss`) to anticipate buffer overflow and Quality of Service (QoS) degradation in high-throughput enterprise networks.
- **Benchmark Performance (Held-out Test Split - 35,069 records)**:
  - **R² Score**: `0.999496`
  - **Root Mean Squared Error (RMSE)**: `1.7167` packets
  - **Mean Absolute Error (MAE)**: `0.0639` packets
  - **5-Fold Cross-Validation Mean R²**: `0.99897` ($\pm 0.00061$)

### Feature Schema & Pipeline Architecture
1. **Input Exclusions (Leakage Safeguard)**:
   - `id`: Non-predictive identifier.
   - `sloss`: Prediction target variable.
   - `attack_cat`: Intrusion classification label.
   - `label`: Binary intrusion indicator.
2. **Domain Feature Engineering**:
   - `total_bytes = sbytes + dbytes` (Aggregates total bi-directional network traffic volume).
3. **Encoding & Scaling**:
   - Categorical columns (`proto`, `service`, `state`): One-Hot Encoded with unknown category tolerance.
   - Numerical columns (39 features including `spkts`, `sbytes`, `dur`, `rate`): Standardized via `StandardScaler`.

### Standalone Inference Execution
To execute the production inference pipeline on sample network flows:
```bash
python models/regression_inference.py
```

### Operational QoS Health Tiers
The inference engine maps continuous predicted packet loss (`sloss`) into three actionable operational QoS tiers:
- **`Predicted sloss < 1.0`**: Optimal QoS (Negligible packet loss, low latency).
- **`1.0 <= Predicted sloss < 10.0`**: Moderate Degradation (Buffer saturation alert, monitor queue depths).
- **`Predicted sloss >= 10.0`**: Severe Degradation (Critical network congestion, trigger automated flow throttling).
