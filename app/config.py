"""
NetSentinel Application Configuration & Constants
"""

import os

# Application Identity
APP_NAME = "NETSENTINEL"
APP_TAGLINE = "QoS INTELLIGENCE"
APP_SUBTITLE = "Comparative Machine Learning Intrusion Detection & QoS Analytics"
COURSE_REF = "23CSE301 Machine Learning Capstone (2026-27)"
VERSION = "v2.4.0-SOC"

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")
SAMPLES_DIR = os.path.join(DATA_DIR, "samples")
BENCHMARKS_PATH = os.path.join(DATA_DIR, "benchmarks_cache.json")

# Dataset File Paths
DATASETS = {
    "regression": {
        "name": "UNSW-NB15",
        "path": os.path.join(DATA_DIR, "regression", "UNSW_NB15_training-set.csv"),
        "target": "sloss",
        "type": "Continuous (Packet Loss)",
        "task": "QoS Degradation & Packet Loss Regression",
        "rows_total": 175341,
        "features_total": 45
    },
    "classification": {
        "name": "CIC-IDS2017",
        "path": os.path.join(DATA_DIR, "classification", "network_traffic_classification.csv"),
        "target": "Label",
        "type": "Multi-Class Intrusion",
        "task": "Network Intrusion Detection & Categorization",
        "rows_total": 7940,
        "features_total": 62
    },
    "clustering": {
        "name": "NSL-KDD",
        "path": os.path.join(DATA_DIR, "clustering", "nslkdd.csv"),
        "target": "None (Unsupervised; post-hoc validation with label/attack)",
        "type": "Unsupervised Behavioral Flows",
        "task": "Unsupervised Traffic Profiling & Threat Discovery",
        "rows_total": 140772,
        "features_total": 41
    }
}

# Threat Severity Mapping for Classification
THREAT_SEVERITY = {
    "BENIGN": {"level": "Benign", "color": "#10b981", "badge": "badge-benign", "action": "Allow Traffic"},
    "DoS Hulk": {"level": "Critical", "color": "#ef4444", "badge": "badge-critical", "action": "Rate Limit & Blacklist IP"},
    "PortScan": {"level": "High", "color": "#f97316", "badge": "badge-high", "action": "Block Port Probe"},
    "DDoS": {"level": "Critical", "color": "#dc2626", "badge": "badge-critical", "action": "Activate Scrubbing Filter"},
    "DoS GoldenEye": {"level": "Critical", "color": "#ef4444", "badge": "badge-critical", "action": "Mitigate HTTP Keep-Alive"},
    "FTP-Patator": {"level": "High", "color": "#f59e0b", "badge": "badge-medium", "action": "Lockout SSH/FTP Credential"},
    "SSH-Patator": {"level": "High", "color": "#f59e0b", "badge": "badge-medium", "action": "Lockout SSH/FTP Credential"},
    "Web Attack  Brute Force": {"level": "Medium", "color": "#ec4899", "badge": "badge-medium", "action": "Challenge WAF CAPTCHA"},
    "Web Attack – Brute Force": {"level": "Medium", "color": "#ec4899", "badge": "badge-medium", "action": "Challenge WAF CAPTCHA"},
    "Bot": {"level": "High", "color": "#8b5cf6", "badge": "badge-high", "action": "Quarantine C2 Channel"}
}

# Colors for Charts
PALETTE = {
    "cyan": "#06b6d4",
    "indigo": "#6366f1",
    "violet": "#8b5cf6",
    "emerald": "#10b981",
    "amber": "#f59e0b",
    "rose": "#f43f5e",
    "red": "#ef4444",
    "slate_dark": "#0f172a",
    "slate_card": "#131c31",
    "grid_color": "rgba(148, 163, 184, 0.12)"
}

# Navigation Items
NAV_ROUTES = [
    {"id": "overview", "label": "Security Overview", "icon": "shield-check"},
    {"id": "traffic_analysis", "label": "Traffic Analysis & Inference", "icon": "cpu"},
    {"id": "threat_intel", "label": "Threat Intelligence", "icon": "crosshair"},
    {"id": "regression_lab", "label": "Regression Analytics (UNSW-NB15)", "icon": "activity"},
    {"id": "classification_lab", "label": "Classification Model Lab (CIC-IDS2017)", "icon": "grid"},
    {"id": "clustering_studio", "label": "Clustering Studio (NSL-KDD)", "icon": "disc"},
    {"id": "dataset_explorer", "label": "Dataset & Model Explorer", "icon": "database"}
]
