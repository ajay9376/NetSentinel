# NetSentinel

## Project Title
**NetSentinel: QoS-Aware Network Intrusion Detection Using Comparative Machine Learning**

## Course
**23CSE301 Machine Learning Capstone**

---

## Overview

Modern computer networks require robust automated systems capable of monitoring performance degradation and detecting sophisticated cyber attacks. **NetSentinel** is a comprehensive machine learning framework designed to evaluate network traffic behavior, maintain Quality of Service (QoS), and classify network intrusions.

The project is structured into three independent, modular machine learning tracks:
1. **Regression Track**: Continuous prediction of network QoS degradation and source packet loss from flow features.
2. **Classification Track**: Multi-class detection and categorization of network intrusions, distinguishing benign network traffic from diverse attack vectors.
3. **Clustering Track**: Unsupervised behavioral grouping, profiling, and anomaly discovery across network communication flows.

Each track operates independently using a dedicated, domain-standard benchmark dataset.

---

## Dataset Plan

To ensure rigorous evaluation across varied network environments, each track utilizes a distinct, specialized dataset:

| Track | Target Task | Dataset | Source / Reference |
| :--- | :--- | :--- | :--- |
| **1. Regression** | QoS & Packet Loss Degradation Prediction | **UNSW-NB15** | Australian Centre for Cyber Security (ACCS) |
| **2. Classification** | Network Intrusion & Threat Vector Classification | **CIC-IDS2017** | Canadian Institute for Cybersecurity (CIC / UNB) |
| **3. Clustering** | Unsupervised Traffic Profiling & Anomaly Grouping | **CTU-13** | Stratosphere IPS Project / CTU University |

> [!NOTE]
> Raw dataset files are not bundled in the initial repository setup. Users must obtain the datasets from their respective official repositories and place them into the corresponding `data/<track>/` directory as outlined in each folder's documentation.

---

## Project Structure

```text
NetSentinel/
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── regression/
│   │   └── README.md
│   ├── classification/
│   │   └── README.md
│   └── clustering/
│       └── README.md
│
├── notebooks/
│   ├── regression.ipynb
│   ├── classification.ipynb
│   └── clustering.ipynb
│
├── models/
│   └── .gitkeep
│
└── app/
    └── .gitkeep
```


---

## Regression Track: Benchmark Results & Evaluation

### Track Summary
- **Objective**: Continuous prediction of network Quality of Service (QoS) degradation and Source Packet Loss (`sloss`) using flow telemetry.
- **Dataset**: UNSW-NB15 (`data/regression/UNSW_NB15_training-set.csv`, 175,341 flow records).
- **Leakage Safeguards**: Excluded non-predictive/leakage columns (`id`, `attack_cat`, `label`, `sloss`).
- **Domain Feature Engineering**: `total_bytes = sbytes + dbytes`.
- **Single Standardized Partition**: 80:20 train-test split (`random_state=42`) with `StandardScaler` and `OneHotEncoder` fitted strictly on training data.
- **Team Responsibilities**:
  - **Member 1**: Baseline pipeline, data auditing, EDA, domain feature engineering, preprocessing setup, and Models 1–5 (Linear, Ridge, Lasso, ElasticNet, Polynomial).
  - **Member 2 (Karthik)**: Models 6–10 (Decision Tree, Random Forest, Gradient Boosting, SVR, KNN), complete 10-model benchmark ranking, hyperparameter tuning via `GridSearchCV`, 5-fold cross-validation, and diagnostic visualizations.

### Complete 10-Model Benchmark Comparison Table

All 10 regression algorithms were evaluated on the exact same held-out test split (35,069 network flow records) and ranked strictly by test $R^2$ score in descending order:

| Rank | Algorithm | Model Family | Test $R^2$ | RMSE (packets) | MAE (packets) | Contributor |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| 1 | **Random Forest Regressor** | Ensemble Bagging | **0.999496** | **1.7167** | **0.0639** | Member 2 |
| 2 | **K-Nearest Neighbors Regressor** | Instance-Based Learning | **0.999395** | **1.8821** | **0.2876** | Member 2 |
| 3 | **Gradient Boosting Regressor** | Sequential Boosting | **0.999262** | **2.0776** | **0.3283** | Member 2 |
| 4 | **Decision Tree Regressor** | Non-Parametric Tree | **0.999101** | **2.2940** | **0.0753** | Member 2 |
| 5 | **Polynomial Regression (Degree 2)** | Non-Linear Transform | **0.997748** | **3.6302** | **1.2262** | Member 1 |
| 6 | **Ridge Regression** | L2 Regularization | **0.997720** | **3.6524** | **0.8512** | Member 1 |
| 7 | **Linear Regression (OLS)** | Linear Baseline | **0.997717** | **3.6551** | **0.8528** | Member 1 |
| 8 | **Support Vector Regressor (SVR)** | Linear Margin Epsilon | **0.997593** | **3.7525** | **0.5065** | Member 2 |
| 9 | **Lasso Regression** | L1 Regularization | **0.997447** | **3.8649** | **0.8501** | Member 1 |
| 10 | **ElasticNet Regression** | Combined L1 + L2 | **0.996063** | **4.7991** | **1.3064** | Member 1 |

### Hyperparameter Tuning Analysis

Hyperparameter optimization was performed using `GridSearchCV` exclusively on the training partition (`X_train_preprocessed`, `y_train`) using 3-fold cross-validation:

| Model | Variant | Optimal Parameters | Best CV $R^2$ | Test $R^2$ | Test RMSE (packets) | Test MAE (packets) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Decision Tree** | Default | `max_depth=None, min_samples_split=2` | — | 0.99910 | 2.2940 | 0.0753 |
| **Decision Tree** | **Tuned** | `{'max_depth': 15, 'min_samples_split': 5}` | 0.99746 | 0.99537 | 5.2037 | 0.1190 |
| **Ridge Regression** | Default | `alpha=1.0` | — | 0.99772 | 3.6524 | 0.8512 |
| **Ridge Regression** | **Tuned** | `{'alpha': 10.0}` | 0.99684 | **0.99775** | **3.6321** | **0.8402** |

### 5-Fold Cross-Validation (Top 2 Models)

Programmatically identified top 2 models evaluated via 5-fold cross-validation on the training set:

| Model | Fold 1 $R^2$ | Fold 2 $R^2$ | Fold 3 $R^2$ | Fold 4 $R^2$ | Fold 5 $R^2$ | Mean CV $R^2$ | Std Dev ($\sigma$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Random Forest Regressor** | 0.99959 | 0.99942 | 0.99918 | 0.99881 | 0.99787 | **0.99897** | 0.00061 |
| **K-Nearest Neighbors Regressor** | 0.99796 | 0.99853 | 0.99792 | 0.99702 | 0.99872 | **0.99803** | 0.00060 |

### Final Diagnostic Visualizations

![NetSentinel Regression Diagnostics](notebooks/final_regression_diagnostics.png)

- **Plot 1 (Model Comparison)**: Tree-based ensemble models (Random Forest, Gradient Boosting) and instance-based KNN establish top predictive accuracy, exceeding linear models.
- **Plot 2 (Actual vs. Predicted)**: Predictions from the best model (Random Forest) cluster tightly along the diagonal ($y=x$) line across all loss ranges.
- **Plot 3 (Residual Distribution)**: Residuals ($y_{test} - \hat{y}$) remain symmetrically distributed around zero with minimal variance.
- **Plot 4 (Feature Importances)**: Gini importance confirms `total_bytes`, `sbytes`, and `spkts` as the primary physical flow drivers of packet loss.

---

## Setup & Environment

### Prerequisites
- Python 3.9+ (Python 3.10 or 3.11 recommended)
- `pip` package manager
- Recommended: A dedicated virtual environment (`venv` or `conda`)

### Installation

1. Clone or navigate to the repository directory:
   ```bash
   git clone https://github.com/ajay9376/NetSentinel.git
   cd NetSentinel
   ```

2. Create and activate a virtual environment:
   - On Windows:
     ```powershell
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - On Linux/macOS:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch Jupyter Notebook / JupyterLab:
   ```bash
   jupyter notebook
   ```

---

## Workflow & Development Guidelines
- Each ML track has an independent notebook located under the `notebooks/` directory.
- Model artifacts generated during training should be saved to the `models/` directory (ignored by Git, keeping the repository lightweight).
- Any application or dashboard interface will be organized under the `app/` directory.
