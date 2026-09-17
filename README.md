# NetGuard-QoS-IDS

## Project Title
**NetGuard: QoS-Aware Network Intrusion Detection Using Comparative Machine Learning**

## Course
**23CSE301 Machine Learning Capstone**

---

## Overview

Modern computer networks require robust automated systems capable of monitoring performance degradation and detecting sophisticated cyber attacks. **NetGuard-QoS-IDS** is a comprehensive machine learning framework designed to evaluate network traffic behavior, maintain Quality of Service (QoS), and classify network intrusions.

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
NetGuard-QoS-IDS/
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

## Setup & Environment

### Prerequisites
- Python 3.9+ (Python 3.10 or 3.11 recommended)
- `pip` package manager
- Recommended: A dedicated virtual environment (`venv` or `conda`)

### Installation

1. Clone or navigate to the repository directory:
   ```bash
   git clone https://github.com/ajay9376/NetSentinel.git NetGuard-QoS-IDS
   cd NetGuard-QoS-IDS
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
