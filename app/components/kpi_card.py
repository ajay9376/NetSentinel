"""
SOC KPI Metric Card Component
"""

import streamlit as st

def render_kpi_card(title: str, value: str, subtext: str = "", accent: str = "cyan", icon: str = ""):
    """
    Renders a styled SOC KPI Card.
    accent options: 'cyan', 'indigo', 'danger', 'success'
    """
    accent_class = f"accent-{accent}" if accent != "cyan" else ""
    icon_html = f"<span style='margin-right: 0.35rem;'>{icon}</span>" if icon else ""

    html = f"""
    <div class="kpi-card {accent_class}">
        <div class="kpi-title">{icon_html}{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-subtext">{subtext}</div>
    </div>
    """
    return html
