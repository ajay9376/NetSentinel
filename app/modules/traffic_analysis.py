"""
Section B: Traffic Analysis & Real-Time Inference Workspace
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
from app.config import SAMPLES_DIR, THREAT_SEVERITY
from app.utils.model_loader import (
    load_classification_bundle,
    run_classification_inference
)
from app.components.charts import build_threat_distribution_chart, build_threat_gauge
from app.components.kpi_card import render_kpi_card

def render_traffic_analysis():
    """Renders the Traffic Analysis & Inference Page."""
    st.markdown("## ⚡ Network Traffic Analysis & Real-Time Inference Engine")
    st.markdown(
        "<p style='color: #94a3b8; font-size: 0.9rem; margin-top: -0.5rem;'>"
        "Upload raw network flow data or load pre-packaged benchmark batches to generate real-time intrusion classifications, "
        "confidence scores, and threat mitigations using fitted zero-leakage scikit-learn models."
        "</p>",
        unsafe_allow_html=True
    )

    clf_bundle = load_classification_bundle()
    if clf_bundle is None:
        st.error("⚠️ Classification model bundle is not loaded. Please verify that 'models/classification_bundle.joblib' exists.")
        return

    expected_features = clf_bundle["features"]
    available_models = list(clf_bundle["models"].keys())

    # Mode Selector: Upload custom CSV or Load Sample Batch
    tab_upload, tab_sample = st.tabs(["📁 Upload Network Flow CSV", "📦 Load Benchmark Sample Batch"])

    df_to_analyze = None
    data_source_name = ""

    with tab_upload:
        st.markdown(
            """
            <div style="font-size: 0.82rem; color: #94a3b8; margin-bottom: 0.75rem;">
                Upload a CSV containing network packet flow telemetry (e.g. CIC-IDS2017 format). 
                If the ground-truth <code>Label</code> column is present in the file, it will be quarantined automatically to prevent target leakage.
            </div>
            """,
            unsafe_allow_html=True
        )
        uploaded_file = st.file_uploader(
            "Drag & drop flow CSV file here",
            type=["csv"],
            help="Accepts CSV files with network flow attributes."
        )
        if uploaded_file is not None:
            try:
                df_to_analyze = pd.read_csv(uploaded_file)
                data_source_name = uploaded_file.name
                st.success(f"Successfully loaded {uploaded_file.name} ({df_to_analyze.shape[0]:,} rows, {df_to_analyze.shape[1]} columns)")
            except Exception as e:
                st.error(f"Error reading CSV file: {e}")

    with tab_sample:
        st.markdown(
            """
            <div style="font-size: 0.82rem; color: #94a3b8; margin-bottom: 0.75rem;">
                Select a verified, real-world network traffic batch from the held-out CIC-IDS2017 test partition for instantaneous demonstration.
            </div>
            """,
            unsafe_allow_html=True
        )
        sample_options = {
            "Mixed Traffic Flow Batch (50 flows)": "sample_mixed_traffic.csv",
            "Targeted Volumetric DoS & DDoS Attack Batch (30 flows)": "sample_dos_attack_flows.csv",
            "Clean Benign Enterprise Traffic Batch (30 flows)": "sample_benign_flows.csv"
        }
        chosen_sample_label = st.selectbox("Select Benchmark Batch", options=list(sample_options.keys()))
        sample_filename = sample_options[chosen_sample_label]
        sample_filepath = os.path.join(SAMPLES_DIR, sample_filename)

        if st.button("📥 Load Selected Sample Batch", use_container_width=False):
            if os.path.exists(sample_filepath):
                df_to_analyze = pd.read_csv(sample_filepath)
                st.session_state["active_flow_df"] = df_to_analyze
                st.session_state["active_flow_name"] = chosen_sample_label
                st.success(f"Loaded '{chosen_sample_label}' into analysis buffer.")
            else:
                st.warning(f"Sample file not found at {sample_filepath}")

    # Fallback to session state if sample was previously loaded
    if df_to_analyze is None and "active_flow_df" in st.session_state:
        df_to_analyze = st.session_state["active_flow_df"]
        data_source_name = st.session_state.get("active_flow_name", "Loaded Batch")

    if df_to_analyze is not None:
        st.markdown("<hr style='border-color: rgba(148,163,184,0.12); margin: 1.5rem 0;'/>", unsafe_allow_html=True)
        st.markdown(f"### 📋 Flow Buffer Inspection: `{data_source_name}`")

        # Feature Validation Audit
        cols_present = [c.strip() for c in df_to_analyze.columns]
        missing_features = [f for f in expected_features if f not in cols_present]
        extra_features = [c for c in cols_present if c not in expected_features and c != "Label"]

        val_col1, val_col2, val_col3, val_col4 = st.columns(4)
        with val_col1:
            st.metric("Total Rows in Buffer", f"{len(df_to_analyze):,}")
        with val_col2:
            st.metric("Total Columns", len(df_to_analyze.columns))
        with val_col3:
            match_pct = (1.0 - (len(missing_features) / len(expected_features))) * 100
            st.metric("Feature Schema Match", f"{match_pct:.1f}%")
        with val_col4:
            leakage_status = "Quarantined" if "Label" in df_to_analyze.columns else "Clean"
            st.metric("Target Leakage Guard", leakage_status)

        if missing_features:
            with st.expander(f"⚠️ {len(missing_features)} Expected Features Missing from Input (Auto-Aligned by Imputer)"):
                st.write(missing_features)

        # Buffer Data Preview with Pagination
        st.markdown("##### Raw Flow Preview (First 5 Rows)")
        st.dataframe(df_to_analyze.head(5), use_container_width=True)

        # Inference Control Panel
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        col_m1, col_m2 = st.columns([1.5, 1])
        with col_m1:
            selected_model = st.selectbox(
                "Select Active Classifier Model",
                options=available_models,
                index=0,
                help="Choose from the verified models trained in Review 1 & 2."
            )
        with col_m2:
            st.markdown("<div style='height: 1.7rem;'></div>", unsafe_allow_html=True)
            run_btn = st.button("🚀 Analyze Traffic & Predict Threats", use_container_width=True, type="primary")

        if run_btn or "last_results_df" in st.session_state:
            if run_btn:
                with st.spinner("Executing pipeline: preprocessing, feature engineering, and inference..."):
                    results_df, summary = run_classification_inference(df_to_analyze, model_name=selected_model)
                    st.session_state["last_results_df"] = results_df
                    st.session_state["last_summary"] = summary
            else:
                results_df = st.session_state["last_results_df"]
                summary = st.session_state["last_summary"]

            st.markdown("<hr style='border-color: rgba(148,163,184,0.12); margin: 1.5rem 0;'/>", unsafe_allow_html=True)
            st.markdown("### 🎯 Inference Telemetry & Classification Results")

            # Result KPIs
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.markdown(render_kpi_card(
                    title="ANALYZED FLOWS",
                    value=f"{summary['total_analyzed']:,}",
                    subtext=f"Model: {summary['model_used']}",
                    accent="cyan"
                ), unsafe_allow_html=True)
            with k2:
                st.markdown(render_kpi_card(
                    title="CLEAN / BENIGN",
                    value=f"{summary['benign_count']:,}",
                    subtext=f"{(summary['benign_count']/summary['total_analyzed'])*100:.1f}% of analyzed batch",
                    accent="success"
                ), unsafe_allow_html=True)
            with k3:
                threat_pct = (summary['threat_count']/summary['total_analyzed'])*100
                st.markdown(render_kpi_card(
                    title="DETECTED THREATS",
                    value=f"{summary['threat_count']:,}",
                    subtext=f"{threat_pct:.1f}% malicious flows flagged",
                    accent="danger" if summary['threat_count'] > 0 else "success"
                ), unsafe_allow_html=True)
            with k4:
                avg_conf = results_df["Confidence (%)"].mean()
                st.markdown(render_kpi_card(
                    title="MEAN CONFIDENCE",
                    value=f"{avg_conf:.1f}%",
                    subtext="Prediction certainty score",
                    accent="indigo"
                ), unsafe_allow_html=True)

            # Chart breakdown
            st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
            c_gauge, c_donut, c_filter = st.columns([1.1, 1.2, 1.7])
            with c_gauge:
                fig_gauge = build_threat_gauge(threat_pct)
                st.plotly_chart(fig_gauge, use_container_width=True)

            with c_donut:
                fig_res = build_threat_distribution_chart(summary["class_counts"], "Category Breakdown")
                st.plotly_chart(fig_res, use_container_width=True)

            with c_filter:
                st.markdown("#### 🔍 Filter & Search Records")
                filter_class = st.multiselect(
                    "Filter by Predicted Threat",
                    options=list(summary["class_counts"].keys()),
                    default=list(summary["class_counts"].keys())
                )
                search_query = st.text_input("Search in features/actions", "")

            # Filter data
            filtered_df = results_df[results_df["Predicted_Threat"].isin(filter_class)]
            if search_query:
                mask = filtered_df.astype(str).apply(lambda row: row.str.contains(search_query, case=False).any(), axis=1)
                filtered_df = filtered_df[mask]

            # Priority column view
            priority_cols = ["Predicted_Threat", "Confidence (%)", "Threat_Level", "Recommended_Action"]
            other_cols = [c for c in filtered_df.columns if c not in priority_cols]
            display_df = filtered_df[priority_cols + other_cols]

            st.markdown(f"##### Results Table ({len(display_df):,} matching flows)")
            st.dataframe(display_df, use_container_width=True)

            # CSV Download Action
            csv_data = display_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Full Prediction Telemetry (CSV)",
                data=csv_data,
                file_name=f"netguard_predictions_{summary['model_used'].lower().replace(' ', '_')}.csv",
                mime="text/csv"
            )
    else:
        st.info("👆 Please upload a network flow CSV file or load a pre-packaged benchmark batch above to begin traffic analysis.")
