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

st.session_state["_suite_launcher"] = True
entrypoint = "03_dashboard.py" if view == "dashboard" else "04_software.py"
runpy.run_path(str(APP_DIR / entrypoint), run_name="__main__")

st.markdown(
    f'''<style>
    :root{{--suite-accent:#6C5CE7}}
    .suite-switch{{position:fixed;top:.8rem;right:1.4rem;z-index:100000;display:flex;gap:3px;padding:4px;background:#15151e;border:1px solid #30303c;border-radius:7px;box-shadow:0 5px 18px rgba(0,0,0,.22)}}
    .suite-switch a{{display:block;padding:.48rem .75rem;border-radius:4px;color:#b9b9c7!important;text-decoration:none!important;font:650 .72rem "Stack Sans Text","Segoe UI",sans-serif}}
    .suite-switch a:hover{{color:#fff!important;background:#242430}}
    .suite-switch a.active{{background:var(--suite-accent);color:#fff!important}}
    @media(max-width:700px){{.suite-switch{{right:.65rem;top:.55rem}}.suite-switch a{{padding:.42rem .58rem;font-size:.66rem}}}}
    </style>
    <nav class="suite-switch" aria-label="Project workspace">
      <a class="{{software_class}}" href="?view=software" target="_self">Software</a>
      <a class="{{dashboard_class}}" href="?view=dashboard" target="_self">Dashboard</a>
    </nav>''',
    unsafe_allow_html=True,
)
