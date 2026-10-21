"""
NetSentinel: Streamlit Cloud Deployment Entrypoint
Dispatches execution seamlessly to app/main.py.
"""
import runpy
import sys
from pathlib import Path

# Add project root and app to sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

app_main = root_dir / "app" / "main.py"
runpy.run_path(str(app_main), run_name="__main__")
