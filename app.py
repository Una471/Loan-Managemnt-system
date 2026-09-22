from pathlib import Path
import runpy
import streamlit as st

APP_DIR = Path(__file__).resolve().parent

view = st.query_params.get("view", "software")
if isinstance(view, list):
    view = view[0] if view else "software"
view = "dashboard" if view == "dashboard" else "software"

software_class = "active" if view == "software" else ""
dashboard_class = "active" if view == "dashboard" else ""

entrypoint = "03_dashboard.py" if view == "dashboard" else "04_software.py"
runpy.run_path(str(APP_DIR / entrypoint), run_name="__main__")
