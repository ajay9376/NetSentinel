"""
SOC Top Navigation Bar Component
"""

import streamlit as st
from app.config import APP_NAME, APP_TAGLINE, VERSION, COURSE_REF

def render_navbar(active_route_label: str):
    """Renders the top cybersecurity SOC navigation bar."""
    st.markdown(
        f"""
        <div class="soc-navbar">
            <div class="soc-nav-left">
                <span class="status-indicator">
                    <span class="status-dot"></span>
                    SOC INFERENCE ONLINE
                </span>
                <span style="color: #475569; font-size: 0.85rem;">/</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #94a3b8;">
                    {COURSE_REF}
                </span>
                <span style="color: #475569; font-size: 0.85rem;">/</span>
                <span style="color: #38bdf8; font-weight: 700; font-size: 0.82rem; letter-spacing: 0.02em;">
                    {active_route_label}
                </span>
            </div>
            <div class="soc-nav-right">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #38bdf8; background: rgba(6,182,212,0.1); border: 1px solid rgba(6,182,212,0.3); padding: 0.2rem 0.55rem; border-radius: 4px;">
                    DEFCON-4 SECURE
                </span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #64748b; background: rgba(15,23,42,0.85); padding: 0.2rem 0.55rem; border-radius: 4px; border: 1px solid rgba(148,163,184,0.15);">
                    BUILD {VERSION}
                </span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.73rem; color: #34d399; background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.25); padding: 0.2rem 0.55rem; border-radius: 4px;">
                    ZERO-LEAKAGE PIPELINE
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
