# Classification Track Dataset Documentation

## Dataset Name
**CIC-IDS2017 (Canadian Institute for Cybersecurity Intrusion Detection System 2017)**

## Track
**Track 2: Classification Track (Multiclass Network Threat Detection)**

## Objective
To categorize enterprise network communication flows into multi-class intrusion profiles (such as DoS Hulk, DDoS, PortScan, DoS GoldenEye, FTP-Patator, SSH-Patator, Web Attacks, and Botnet activity) as well as benign baseline traffic, rigorously evaluating classification accuracy, precision, recall, weighted F1-score, and multiclass ROC-AUC.

## Dataset Source & Attribution
- **Provider**: Canadian Institute for Cybersecurity (CIC), University of New Brunswick (UNB)
- **Official Portal**: [https://www.unb.ca/cic/datasets/ids-2017.html](https://www.unb.ca/cic/datasets/ids-2017.html)
- **Reference**: Sharafaldin, I., Lashkari, A. H., & Ghorbani, A. A. (2018). *Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization*. ICISSP.

---

## Active Local Dataset File

The capstone team has provisioned the consolidated and representative classification dataset:

- **File Name**: `network_traffic_classification.csv`
- **File Location**: `data/classification/network_traffic_classification.csv`
- **File Size**: ~7.15 MB (7,153,194 bytes)
- **Total Dimensions**: 8,000 observations × 79 attributes (78 features + 1 target variable)
- **Data Integrity**: Raw dataset is strictly preserved without external replacement or tampering.

---

## Target Variable & Class Distribution

The dataset target column is **`Label`**, which represents a **Multiclass Classification** problem containing 9 distinct network flow classes:

| Class Name | Flow Type | Count | Percentage (%) |
| :--- | :--- | :---: | :---: |
| **BENIGN** | Legitimate Normal Traffic | 4,859 | 60.74% |
| **DoS Hulk** | Denial of Service (HULK) | 1,552 | 19.40% |
| **PortScan** | Network Reconnaissance / Port Scan | 653 | 8.16% |
| **DDoS** | Distributed Denial of Service | 367 | 4.59% |
| **DoS GoldenEye** | Denial of Service (GoldenEye) | 254 | 3.18% |
| **FTP-Patator** | Brute-force Authentication (FTP) | 130 | 1.62% |
| **SSH-Patator** | Brute-force Authentication (SSH) | 114 | 1.42% |
| **Web Attack – Brute Force** | Web Application Attack | 38 | 0.48% |
| **Bot** | Botnet C&C Traffic | 33 | 0.41% |
| **Total** | | **8,000** | **100.00%** |

### Class Imbalance Analysis
The dataset exhibits significant class imbalance typical of real-world operational security monitoring:
- Benign traffic dominates at ~60.7% of all flows.
- High-volume attack vectors (DoS Hulk, PortScan, DDoS) represent the majority of threat flows (~32.1%).
- Low-frequency, stealthy threat vectors (Web Attack, Botnet, Patator brute-force) constitute minority classes (<2% each).
- **Modeling Requirement**: Stratified data partitioning (`stratify=y`) and weighted classification metrics (`average='weighted'`) are mandatory across all 10 algorithms to prevent minority class omission.

---

## Feature Architecture

The 78 input features encompass bidirectional statistical flow metrics extracted by CICFlowMeter, including:
1. **Time Attributes**: `Flow Duration`, `Flow IAT Mean`, `Flow IAT Std`, `Flow IAT Max`, `Flow IAT Min`, `Fwd IAT Total`, `Bwd IAT Total`, `Active Mean`, `Idle Mean`.
2. **Packet Volumetrics**: `Total Fwd Packets`, `Total Backward Packets`, `Total Length of Fwd Packets`, `Total Length of Bwd Packets`.
3. **Payload Statistics**: `Fwd Packet Length Max/Min/Mean/Std`, `Bwd Packet Length Max/Min/Mean/Std`, `Packet Length Mean/Std/Variance`.
4. **Flow Rate Metrics**: `Flow Bytes/s`, `Flow Packets/s`, `Fwd Packets/s`, `Bwd Packets/s`.
5. **Protocol Flags**: `FIN Flag Count`, `SYN Flag Count`, `RST Flag Count`, `PSH Flag Count`, `ACK Flag Count`, `URG Flag Count`.
6. **TCP Window & Subflow Features**: `Init_Win_bytes_forward`, `Init_Win_bytes_backward`, `Subflow Fwd Packets`, `Subflow Fwd Bytes`.

---

## Data Cleaning & Preprocessing Rules

1. **Infinite & Missing Values**:
   - Division-by-zero occurrences during flow capture (flows with 0 duration) produce infinite values in `Flow Bytes/s` (10 inf) and `Flow Packets/s` (10 inf), along with 20 missing values each.
   - Rows containing `NaN` or `Inf` (60 rows, <0.75% of total dataset) are cleanly pruned, yielding a pristine set of 7,940 samples across all 9 classes.
2. **Feature Engineering**:
   - `Fwd_to_Total_Packets_Ratio`: Measures directional traffic asymmetry, capturing the ratio of forward request packets to total exchange packets without leaking class labels.
3. **Partitioning**:
   - Single stratified 80:20 split (`random_state=42`, `stratify=y`) shared across all 10 classification algorithms.
4. **Leakage Prevention**:
   - Feature scalers (`StandardScaler`) and label encoders are fitted exclusively on `X_train` and applied to `X_test`.

---

## Validation Protocol & Explainability Standards

1. **5-Fold Stratified Cross-Validation**:
   - Baseline models are cross-validated on the training split using `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` to ensure stable generalization ($\sigma < 0.01$) and rule out fold-level overfitting.
2. **Evaluation Metrics**:
   - In addition to standard Accuracy and Weighted F1, Macro F1 is tracked to provide unweighted sensitivity for rare attack classes (`Bot`, `Web Attack`, `Patator`).
3. **Feature Importance Explainability**:
   - Tree-based feature importances highlight directional payload attributes (`Total Length of Bwd Packets`, `Subflow Fwd Bytes`, `Bwd Header Length`) as dominant signatures for network anomaly categorization.
