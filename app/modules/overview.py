"""
Section A: Security Overview / Executive SOC Dashboard
"""

import streamlit as st
import pandas as pd
from app.components.kpi_card import render_kpi_card
from app.components.charts import (
    build_threat_distribution_chart,
    build_classification_benchmark_chart,
    build_regression_comparison_chart
)
from app.utils.model_loader import load_benchmarks, load_classification_bundle
from app.config import DATASETS

def render_overview():
    """Renders the Executive SOC Security Overview Page."""
    st.markdown("## 🛡️ Security Operations & Model Intelligence Overview")
    st.markdown(
        "<p style='color: #94a3b8; font-size: 0.9rem; margin-top: -0.5rem;'>"
        "Unified telemetry across three independent Machine Learning tracks: "
        "<b>Regression</b> (UNSW-NB15), <b>Classification</b> (CIC-IDS2017), and <b>Clustering</b> (NSL-KDD)."
        "</p>",
        unsafe_allow_html=True
    )

    benchmarks = load_benchmarks()
    clf_bundle = load_classification_bundle()

    # Row 1: KPI Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_kpi_card(
            title="TOTAL AUDITED RECORDS",
            value="324,053",
            subtext="Across 3 Dedicated Datasets",
            accent="cyan",
            icon="🌐"
        ), unsafe_allow_html=True)
    with col2:
        st.markdown(render_kpi_card(
            title="TOP REGRESSOR (R²)",
            value="0.99967",
            subtext="Random Forest (sloss target)",
            accent="success",
            icon="📈"
        ), unsafe_allow_html=True)
    with col3:
        st.markdown(render_kpi_card(
            title="TOP CLASSIFIER ACC",
            value="89.80%",
            subtext="Logistic Regression & Linear SVC",
            accent="indigo",
            icon="🛡️"
        ), unsafe_allow_html=True)
    with col4:
        st.markdown(render_kpi_card(
            title="UNSUPERVISED ARI",
            value="0.6185",
            subtext="K-Means (K=5) Threat Alignment",
            accent="cyan",
            icon="🧩"
        ), unsafe_allow_html=True)

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

    # Row 2: Charts (Threat distribution + Model Highlights)
    c1, c2 = st.columns([1.1, 1.4])
    with c1:
        st.markdown("#### 🎯 Baseline Threat Landscape (CIC-IDS2017)")
        # Actual class distribution from verified dataset
        actual_class_dist = {
            "BENIGN": 4830,
            "DoS Hulk": 1537,
            "PortScan": 648,
            "DDoS": 363,
            "DoS GoldenEye": 250,
            "FTP-Patator": 129,
            "SSH-Patator": 113,
            "Web Attack": 37,
            "Bot": 33
        }
        fig_donut = build_threat_distribution_chart(actual_class_dist, "Verified Attack Category Distribution")
        st.plotly_chart(fig_donut, use_container_width=True)

    with c2:
        st.markdown("#### 📊 Classification Benchmark (Part A + Part B)")
        df_clf = pd.DataFrame(benchmarks.get("classification", []))
        if not df_clf.empty:
            fig_clf = build_classification_benchmark_chart(df_clf)
            st.plotly_chart(fig_clf, use_container_width=True)
        else:
            st.info("Loading classification benchmark metrics...")

    # Row 3: Readiness Table across the 3 ML Tracks
    st.markdown("#### 🚦 Machine Learning Track Readiness & Operational Scope")
    
    track_summary_data = [
        {
            "ML Track": "1. Regression Track",
            "Dataset": "UNSW-NB15",
            "Target Objective": "sloss (Source Packet Loss)",
            "Audited Flows": "175,341 flows",
            "Algorithms Evaluated": "10 Algorithms (Linear, Ridge, Lasso, ElasticNet, Poly, DT, RF, GB, SVR, KNN)",
            "Best Performance": "Random Forest: R² = 0.999669 | RMSE = 1.3914",
            "Status": "READY (Review 1)"
        },
        {
            "ML Track": "2. Classification Track",
            "Dataset": "CIC-IDS2017",
            "Target Objective": "Label (Multi-Class Intrusion)",
            "Audited Flows": "7,940 clean flows",
            "Algorithms Evaluated": "10 Algorithms (Part A: 5 Baselines, Part B: 5 Ensembles/MLP)",
            "Best Performance": "Logistic Reg / SVC: 89.80% Acc | 0.8637 F1",
            "Status": "READY (Reviews 1 & 2)"
        },
        {
            "ML Track": "3. Clustering Track",
            "Dataset": "NSL-KDD",
            "Target Objective": "Unsupervised Behavioral Grouping",
            "Audited Flows": "140,772 flows (50k sample)",
            "Algorithms Evaluated": "2 Algorithms (K-Means K=5/K=3, Agglomerative Hierarchical K=5)",
            "Best Performance": "K-Means K=5: Silhouette = 0.4600 | ARI = 0.6185",
            "Status": "READY (Review 2)"
        }
    ]
    st.dataframe(pd.DataFrame(track_summary_data), use_container_width=True, hide_index=True)

    # Action Banner
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    col_act1, col_act2 = st.columns([2, 1])
    with col_act1:
        st.markdown(
            """
            <div style="background: rgba(6, 182, 212, 0.08); border: 1px solid rgba(6, 182, 212, 0.25); border-radius: 8px; padding: 1rem 1.25rem;">
                <div style="color: #38bdf8; font-weight: 600; font-size: 0.95rem; margin-bottom: 0.25rem;">
                    🚀 Ready to Test Live Network Traffic Inference?
                </div>
                <div style="color: #94a3b8; font-size: 0.82rem;">
                    Upload an unlabelled network flow CSV or load pre-packaged benchmark traffic flows to run real-time multi-class intrusion detection and QoS risk estimation.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_act2:
        st.markdown("<div style='height: 0.4rem;'></div>", unsafe_allow_html=True)
        if st.button("⚡ Open Traffic Analysis Workspace", use_container_width=True):
            st.session_state.active_nav = "Traffic Analysis & Inference"
            st.rerun()
