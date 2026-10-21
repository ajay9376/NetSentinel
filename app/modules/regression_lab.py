"""
Section D: Regression Analytics Workspace (UNSW-NB15 — Target: sloss)
"""

import streamlit as st
import pandas as pd
import numpy as np
from app.components.charts import (
    build_regression_comparison_chart,
    build_actual_vs_predicted_chart,
    build_residual_plot,
    build_feature_importance_chart,
    build_qos_health_gauge
)
from app.utils.model_loader import load_benchmarks, load_regression_bundle, run_regression_inference
from app.components.kpi_card import render_kpi_card

def render_regression_lab():
    """Renders the Regression Analytics Workspace."""
    st.markdown("## 📉 Regression Analytics & QoS Degradation Modeling")
    st.markdown(
        "<p style='color: #94a3b8; font-size: 0.9rem; margin-top: -0.5rem;'>"
        "Comparative evaluation across all 10 mandated regression algorithms on the <b>UNSW-NB15</b> dataset, "
        "predicting continuous source packet loss (<code>sloss</code>) to quantify Quality-of-Service (QoS) degradation."
        "</p>",
        unsafe_allow_html=True
    )

    benchmarks = load_benchmarks()
    reg_bundle = load_regression_bundle()
    df_reg = pd.DataFrame(benchmarks.get("regression", []))

    # KPI Banner
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(render_kpi_card(
            title="TARGET OBJECTIVE",
            value="sloss",
            subtext="Source Packet Loss (UNSW-NB15)",
            accent="cyan",
            icon="🎯"
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(render_kpi_card(
            title="TOP TEST R²",
            value="0.99967",
            subtext="Random Forest Regressor",
            accent="success",
            icon="🏆"
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(render_kpi_card(
            title="LOWEST RMSE",
            value="1.3914",
            subtext="Random Forest vs Baseline 3.655",
            accent="indigo",
            icon="📉"
        ), unsafe_allow_html=True)
    with c4:
        st.markdown(render_kpi_card(
            title="5-FOLD CV R²",
            value="0.99917",
            subtext="Tuned Gradient Boosting",
            accent="cyan",
            icon="🔄"
        ), unsafe_allow_html=True)

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

    tab_table, tab_diag, tab_importance, tab_calc = st.tabs([
        "📋 10-Algorithm Comparison Table",
        "🔬 Diagnostics & Residual Plots",
        "🌲 Feature Importance & Tuning",
        "⚡ Interactive QoS Packet Loss Calculator"
    ])

    with tab_table:
        st.markdown("#### Official 10-Algorithm Regression Benchmark Table (Ranked by R²)")
        if not df_reg.empty:
            st.dataframe(df_reg, use_container_width=True, hide_index=True)
            fig_bar = build_regression_comparison_chart(df_reg)
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Regression benchmark table is loading...")

        st.markdown(
            """
            <div style="background: rgba(15,23,42,0.7); border: 1px solid rgba(148,163,184,0.12); border-radius: 6px; padding: 0.85rem 1.1rem; margin-top: 1rem; font-size: 0.82rem; line-height: 1.6; color: #cbd5e1;">
                <b>📌 Evaluation Summary & Model Selection:</b><br/>
                &bull; <b>Top Performer</b>: <b>Random Forest Regressor</b> achieved the highest test R² (<code>0.999669</code>) and lowest RMSE (<code>1.3914</code>), capturing non-linear flow dynamics.<br/>
                &bull; <b>Cross-Validation Generalization</b>: 5-Fold cross-validation on the top models verified high out-of-sample stability, with Tuned Gradient Boosting reaching <code>0.999170</code> CV R².<br/>
                &bull; <b>Linear Baselines</b>: Linear and Ridge Regression both demonstrated excellent baseline fit (R² ~ <code>0.9977</code>) due to the strong physical correlation between total transmitted packets (<code>spkts</code>) and loss (<code>sloss</code>).
            </div>
            """,
            unsafe_allow_html=True
        )

    with tab_diag:
        c_diag1, c_diag2 = st.columns(2)
        with c_diag1:
            st.markdown("#### Actual vs. Predicted Source Packet Loss (`sloss`)")
            st.markdown("<span style='font-size: 0.78rem; color: #94a3b8;'>Close alignment to red diagonal verifies near-perfect predictive capability across dynamic ranges.</span>", unsafe_allow_html=True)
            fig_avp = build_actual_vs_predicted_chart()
            st.plotly_chart(fig_avp, use_container_width=True)

        with c_diag2:
            st.markdown("#### Residual Plot (ŷ vs Residuals)")
            st.markdown("<span style='font-size: 0.78rem; color: #94a3b8;'>Residuals cluster tightly around 0 without catastrophic heteroscedastic fan-out.</span>", unsafe_allow_html=True)
            fig_res = build_residual_plot()
            st.plotly_chart(fig_res, use_container_width=True)

    with tab_importance:
        col_imp1, col_imp2 = st.columns([1.3, 1.2])
        with col_imp1:
            st.markdown("#### Random Forest Top Predictor Feature Importance")
            if reg_bundle and "top_features" in reg_bundle:
                fig_imp = build_feature_importance_chart(reg_bundle["top_features"], "Feature Importance (Gini Impurity Reduction)")
                st.plotly_chart(fig_imp, use_container_width=True)
            else:
                st.info("Feature importance data loading...")

        with col_imp2:
            st.markdown("#### Hyperparameter Tuning (GridSearchCV)")
            tuning_summary = [
                {
                    "Model": "Random Forest Regressor",
                    "Tuned Parameter Grid": "n_estimators: [50, 100], max_depth: [10, 15, 20]",
                    "Optimal Parameters": "n_estimators=100, max_depth=15, min_samples_split=5",
                    "MAE Improvement": "0.0683 → 0.0586 (14.2% error reduction)"
                },
                {
                    "Model": "Gradient Boosting Regressor",
                    "Tuned Parameter Grid": "learning_rate: [0.05, 0.1], n_estimators: [100, 150]",
                    "Optimal Parameters": "learning_rate=0.1, n_estimators=150, max_depth=5",
                    "CV R² Improvement": "0.999087 → 0.999170 (Best Generalization)"
                },
                {
                    "Model": "Ridge Regression",
                    "Tuned Parameter Grid": "alpha: [0.01, 0.1, 1.0, 10.0, 100.0]",
                    "Optimal Parameters": "alpha=1.0 (Optimal L2 penalty)",
                    "Stability": "Prevents collinearity explosion between spkts & sbytes"
                }
            ]
            st.dataframe(pd.DataFrame(tuning_summary), use_container_width=True, hide_index=True)

    with tab_calc:
        st.markdown("#### Interactive QoS Source Packet Loss (`sloss`) Estimator")
        st.markdown(
            "<span style='font-size: 0.82rem; color: #94a3b8;'>"
            "Input single-flow transmission attributes below to compute real-time predicted packet loss and QoS degradation tier."
            "</span>",
            unsafe_allow_html=True
        )

        calc_c1, calc_c2, calc_c3, calc_c4 = st.columns(4)
        with calc_c1:
            in_spkts = st.number_input("Source Packets (spkts)", min_value=1, max_value=10000, value=64, step=5)
            in_dpkts = st.number_input("Destination Packets (dpkts)", min_value=0, max_value=10000, value=58, step=5)
        with calc_c2:
            in_sbytes = st.number_input("Source Bytes (sbytes)", min_value=1, max_value=5000000, value=8540, step=500)
            in_dbytes = st.number_input("Destination Bytes (dbytes)", min_value=0, max_value=5000000, value=6420, step=500)
        with calc_c3:
            in_dur = st.number_input("Flow Duration in Sec (dur)", min_value=0.0001, max_value=100.0, value=0.152, step=0.01)
            in_rate = st.number_input("Flow Rate packets/sec (rate)", min_value=0.0, max_value=100000.0, value=802.6, step=50.0)
        with calc_c4:
            in_proto = st.selectbox("Transport Protocol (proto)", ["tcp", "udp", "unas", "arp", "ospf"])
            in_state = st.selectbox("Flow State (state)", ["FIN", "CON", "INT", "REQ", "RST"])

        if st.button("📊 Calculate Predicted QoS Degradation"):
            sample_row = pd.DataFrame([{
                "dur": in_dur, "proto": in_proto, "service": "-", "state": in_state,
                "spkts": in_spkts, "dpkts": in_dpkts, "sbytes": in_sbytes, "dbytes": in_dbytes,
                "rate": in_rate, "sttl": 62, "dttl": 252, "sload": 449473.0, "dload": 337894.0,
                "sloss": 0, "dloss": 0, "sinpkt": 2.41, "dinpkt": 2.62, "sjit": 10.5, "djit": 8.4,
                "swin": 255, "stcpb": 1000, "dtcpb": 1000, "dwin": 255, "tcprtt": 0.05, "synack": 0.02,
                "ackdat": 0.03, "smean": 133, "dmean": 110, "trans_depth": 0, "response_body_len": 0,
                "ct_srv_src": 2, "ct_state_ttl": 1, "ct_dst_ltm": 2, "ct_src_dport_ltm": 1,
                "ct_dst_sport_ltm": 1, "ct_dst_src_ltm": 2, "is_ftp_login": 0, "ct_ftp_cmd": 0,
                "ct_flw_http_mthd": 0, "ct_src_ltm": 2, "ct_srv_dst": 2, "is_sm_ips_ports": 0
            }])

            try:
                res_df, pred_loss = run_regression_inference(sample_row)
                predicted_val = pred_loss[0]
                qos_tier = "Optimal / Healthy" if predicted_val < 2 else ("Degraded QoS" if predicted_val < 10 else "Severe Packet Loss")
                tier_color = "#10b981" if predicted_val < 2 else ("#f59e0b" if predicted_val < 10 else "#ef4444")

                c_res1, c_res2 = st.columns([1.3, 1.2])
                with c_res1:
                    st.markdown(
                        f"""
                        <div style="background: rgba(19, 28, 49, 0.9); border: 1px solid rgba(6, 182, 212, 0.4); border-radius: 8px; padding: 1.25rem; margin-top: 0.5rem; height: 190px; display: flex; flex-direction: column; justify-content: center;">
                            <div>
                                <span style="font-size: 0.78rem; text-transform: uppercase; color: #94a3b8; font-weight: 600;">Predicted Source Packet Loss (sloss):</span>
                                <div style="font-family: 'JetBrains Mono', monospace; font-size: 2.4rem; font-weight: 800; color: #38bdf8; margin: 0.2rem 0;">
                                    {predicted_val:.2f} <span style="font-size: 1.1rem; color: #94a3b8; font-weight: 500;">packets</span>
                                </div>
                            </div>
                            <div style="margin-top: 0.4rem; border-top: 1px solid rgba(148,163,184,0.1); padding-top: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 0.78rem; text-transform: uppercase; color: #94a3b8;">QoS Degradation Tier:</span>
                                <span style="font-size: 1.05rem; font-weight: 700; color: {tier_color};">
                                    {qos_tier}
                                </span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with c_res2:
                    fig_qos = build_qos_health_gauge(predicted_val)
                    st.plotly_chart(fig_qos, use_container_width=True)
            except Exception as e:
                st.error(f"Error computing regression inference: {e}")
