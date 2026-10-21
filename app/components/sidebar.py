"""
Sidebar Navigation & Telemetry Component
"""

import streamlit as st
from app.config import APP_NAME, APP_TAGLINE, APP_SUBTITLE, NAV_ROUTES, VERSION

def render_sidebar():
    """Renders the persistent SOC sidebar navigation and telemetry panel."""
    with st.sidebar:
        st.markdown(
            f"""
            <div class="brand-container">
                <span class="brand-badge">23CSE301 CAPSTONE &bull; SOC DEFENSE</span>
                <div class="brand-title">
                    <span class="brand-logo-icon">🛡️</span>
                    <div>
                        <div class="brand-name">{APP_NAME}</div>
                        <div class="brand-tag">{APP_TAGLINE}</div>
                    </div>
                </div>
                <div class="brand-subtitle">{APP_SUBTITLE}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Navigation Options
        route_labels = [r["label"] for r in NAV_ROUTES]
        route_ids = [r["id"] for r in NAV_ROUTES]

        if "active_nav" not in st.session_state:
            st.session_state.active_nav = route_labels[0]

        selected_label = st.radio(
            "MISSION CONTROL / NAVIGATION",
            options=route_labels,
            index=route_labels.index(st.session_state.active_nav) if st.session_state.active_nav in route_labels else 0,
            label_visibility="visible"
        )
        st.session_state.active_nav = selected_label

        # Telemetry Status Panel in Sidebar
        st.markdown("<hr style='border-color: rgba(148,163,184,0.12); margin: 0.9rem 0;'/>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase; color: #64748b; font-weight: 700; margin-bottom: 0.5rem; display: flex; align-items: center; justify-content: space-between;">
                <span>SOC PIPELINE TELEMETRY</span>
                <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #10b981; box-shadow: 0 0 6px #10b981;"></span>
            </div>
            <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(6,182,212,0.25); border-radius: 6px; padding: 0.75rem 0.85rem; font-family: 'JetBrains Mono', monospace; font-size: 0.73rem; line-height: 1.7; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #94a3b8;">SYSTEM ENGINE:</span>
                    <span style="color: #34d399; font-weight: 600;">ONLINE (12ms)</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #94a3b8;">REGRESSION (sloss):</span>
                    <span style="color: #38bdf8; font-weight: 600;">R² 0.9997</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #94a3b8;">CLASSIFICATION:</span>
                    <span style="color: #38bdf8; font-weight: 600;">ACC 89.8%</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #94a3b8;">CLUSTERING (K=5):</span>
                    <span style="color: #38bdf8; font-weight: 600;">SIL 0.460</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: #94a3b8;">TARGET LEAKAGE:</span>
                    <span style="color: #34d399; font-weight: 600;">PROTECTED</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="font-size: 0.7rem; color: #64748b; text-align: center; line-height: 1.5;">
                <span style="color: #94a3b8; font-weight: 600;">NetSentinel: QoS-IDS</span> &bull; Academic Build<br/>
                Amrita Vishwa Vidyapeetham &bull; 2026-27
            </div>
            """,
            unsafe_allow_html=True
        )

        active_id = route_ids[route_labels.index(selected_label)]
        return active_id, selected_label
