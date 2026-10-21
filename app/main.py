"""
NETSENTINEL | QoS INTELLIGENCE
Main Streamlit Application Entrypoint
"""

import os
import sys
import streamlit as st

# Configure Path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.config import APP_NAME, APP_TAGLINE, APP_SUBTITLE, VERSION, COURSE_REF
from app.components.navbar import render_navbar
from app.components.sidebar import render_sidebar
from app.modules.overview import render_overview
from app.modules.traffic_analysis import render_traffic_analysis
from app.modules.threat_intel import render_threat_intel
from app.modules.regression_lab import render_regression_lab
from app.modules.classification_lab import render_classification_lab
from app.modules.clustering_studio import render_clustering_studio
from app.modules.dataset_explorer import render_dataset_explorer

# Set Streamlit Page Configuration
st.set_page_config(
    page_title=f"{APP_NAME} | {APP_TAGLINE}",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom CSS Stylesheet
def inject_custom_css():
    css_path = os.path.join(CURRENT_DIR, "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

inject_custom_css()

# Render Persistent Sidebar
active_id, active_label = render_sidebar()

# Render SOC Top Navigation Bar
render_navbar(active_label)

# Main Application Router
router = {
    "overview": render_overview,
    "traffic_analysis": render_traffic_analysis,
    "threat_intel": render_threat_intel,
    "regression_lab": render_regression_lab,
    "classification_lab": render_classification_lab,
    "clustering_studio": render_clustering_studio,
    "dataset_explorer": render_dataset_explorer
}

view_function = router.get(active_id, render_overview)
view_function()

# SOC Application Footer
st.markdown(
    f"""
    <div class="soc-footer">
        <div>
            <b>{APP_NAME} &bull; {APP_TAGLINE}</b> &bull; {APP_SUBTITLE}
        </div>
        <div>
            {COURSE_REF} &bull; <a href="https://github.com/ajay9376/NetSentinel" target="_blank">GitHub Repository</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
