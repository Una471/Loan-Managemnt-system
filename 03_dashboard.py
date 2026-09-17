"""
THEBE CREDIT UNION - LOAN PORTFOLIO DASHBOARD
Simple report for branch managers and executives.
Run: streamlit run 03_dashboard.py --server.port 8501
"""

import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

BASE_DIR = Path(__file__).resolve().parent


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@500;600;700;800&family=Stack+Sans+Text:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#f8fafc;color:#0f172a;}
.topbar{background:linear-gradient(135deg,#15151f,#5b8cff);color:white;padding:1.4rem 2rem;border-radius:12px;margin-bottom:1.5rem;box-shadow:0 4px 6px rgba(0,0,0,0.1);}
.topbar h1{margin:0;font-size:1.5rem;font-weight:700;color:white;}
.topbar p{margin:.3rem 0 0;opacity:.9;font-size:.85rem;color:#e2e8f0;}
.kcard{background:white;border-radius:12px;padding:1.2rem 1.4rem;box-shadow:0 2px 8px rgba(0,0,0,.07);border-left:5px solid #2c2c3a;margin-bottom:.3rem;color:#0f172a;}
.kcard.red{border-left-color:#b91c1c;} .kcard.orange{border-left-color:#c2410c;}
.kcard.green{border-left-color:#166534;} .kcard.blue{border-left-color:#5b8cff;}
.kval{font-size:1.9rem;font-weight:700;line-height:1.1;color:#0f172a;}
.klbl{font-size:.72rem;text-transform:uppercase;letter-spacing:1.5px;color:#5b8cff;margin-top:.3rem;font-weight:700;}
.ksub{font-size:.78rem;color:#334155;margin-top:.3rem;}
.ccard{background:white;border-radius:12px;padding:1.2rem 1.4rem;box-shadow:0 2px 8px rgba(0,0,0,.07);margin-bottom:1rem;color:#0f172a;}
.ctitle{font-size:.95rem;font-weight:700;color:#0f172a;margin-bottom:.2rem;}
.csub{font-size:.78rem;color:#334155;margin-bottom:.7rem;}
/* Enhanced contrast for insight boxes */
.ar{background:#fee2e2;border:1px solid #b91c1c;border-radius:8px;padding:.9rem;margin-bottom:.5rem;color:#7f1d1d;}
.ao{background:#ffedd5;border:1px solid #c2410c;border-radius:8px;padding:.9rem;margin-bottom:.5rem;color:#7b341e;}
.ag{background:#dcfce7;border:1px solid #166534;border-radius:8px;padding:.9rem;margin-bottom:.5rem;color:#14532d;}
.ar b, .ao b, .ag b {color:#0f172a !important;}
.ar, .ao, .ag {font-weight:500;}
section[data-testid="stSidebar"]{background:#15151f!important;}
section[data-testid="stSidebar"] *{color:white!important;}
section[data-testid="stSidebar"] .stSelectbox label{color:#e2e8f0!important;}
.st-bb{background-color:transparent;}
#MainMenu,footer,header{visibility:hidden;}
div[data-testid="stDataFrame"]{color:#0f172a;}
.stDataFrame {color:#0f172a;}
/* Professional analytics console */
:root{--dash-bg:#0d0d14;--dash-side:#15151f;--dash-card:#1a1a24;--dash-card-2:#20202c;--dash-line:#2c2c3a;--dash-text:#f5f5f7;--dash-muted:#9a9aaa;--dash-accent:#5b8cff;--dash-soft:#a9c1ff}
html,body,[class*="css"],.stApp{font-family:'Stack Sans Text','Red Hat Display','Segoe UI',sans-serif!important;background:var(--dash-bg)!important;color:var(--dash-text)!important}.stApp{background:radial-gradient(circle at 86% 0%,rgba(91,140,255,.08),transparent 30%),var(--dash-bg)!important}.block-container{max-width:1500px;padding:1.25rem 2rem 3rem!important}h1,h2,h3,h4,p,label,span{color:var(--dash-text)}h1,h2,h3,h4{font-family:'Red Hat Display','Segoe UI',sans-serif!important;letter-spacing:-.025em}
section[data-testid="stSidebar"]{width:228px!important;background:var(--dash-side)!important;border-right:1px solid var(--dash-line)!important}section[data-testid="stSidebar"]>div{padding:1.3rem .85rem!important}section[data-testid="stSidebar"] h3{font-size:1.05rem!important;margin:.2rem .55rem 0!important;color:#fff!important}section[data-testid="stSidebar"] p{color:var(--dash-muted)!important;font-size:.72rem!important}section[data-testid="stSidebar"] hr{border-color:var(--dash-line)!important;margin:1rem 0!important}section[data-testid="stSidebar"] div[role="radiogroup"]{gap:.3rem}section[data-testid="stSidebar"] div[role="radiogroup"] label{padding:.65rem .7rem!important;border-radius:7px!important;background:transparent!important;margin:0!important;transition:background .16s ease}section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{background:var(--dash-card-2)!important}section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){background:var(--dash-accent)!important}section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p{color:#101018!important;font-weight:700!important}section[data-testid="stSidebar"] div[role="radiogroup"] label>div:first-child{display:none}section[data-testid="stSidebar"] [data-baseweb="select"]>div{background:var(--dash-card)!important;border-color:var(--dash-line)!important;color:#fff!important;border-radius:7px!important}section[data-testid="stSidebar"] svg{fill:var(--dash-muted)!important}
.topbar{position:relative;background:transparent!important;border:0!important;border-bottom:1px solid var(--dash-line)!important;border-radius:0!important;box-shadow:none!important;padding:.4rem 0 1rem!important;margin-bottom:1.1rem!important}.topbar:before{content:'ANALYTICS';display:block;color:var(--dash-accent);font-size:.58rem;letter-spacing:.18em;font-weight:700;margin-bottom:.45rem}.topbar h1{font-size:1.65rem!important;color:#fff!important}.topbar p{color:var(--dash-muted)!important;opacity:1!important;font-size:.73rem!important}
.kcard{min-height:118px;background:var(--dash-card)!important;border:1px solid var(--dash-line)!important;border-left:1px solid var(--dash-line)!important;border-top:3px solid var(--dash-accent)!important;border-radius:8px!important;box-shadow:none!important;padding:1rem 1.05rem!important;color:var(--dash-text)!important}.kcard.red{border-top-color:#ff6b6b!important}.kcard.orange{border-top-color:#f4a261!important}.kcard.green{border-top-color:#59d98e!important}.kcard.blue,.kcard.gold{border-top-color:var(--dash-accent)!important}.kval{font-family:'Red Hat Display','Segoe UI',sans-serif!important;font-size:1.75rem!important;color:#fff!important;font-variant-numeric:tabular-nums}.klbl{color:#d7d7df!important;font-size:.62rem!important;letter-spacing:.1em!important}.ksub{color:var(--dash-muted)!important;font-size:.66rem!important}
.ccard{background:var(--dash-card)!important;border:1px solid var(--dash-line)!important;border-radius:8px!important;box-shadow:none!important;padding:1rem!important}.ctitle{color:#fff!important;font-size:.86rem!important}.csub{color:var(--dash-muted)!important;font-size:.68rem!important}.ar,.ao,.ag{background:var(--dash-card)!important;border:1px solid var(--dash-line)!important;border-left:3px solid var(--dash-accent)!important;border-radius:7px!important;color:#dcdce4!important;line-height:1.5!important}.ar{border-left-color:#ff6b6b!important}.ao{border-left-color:#f4a261!important}.ag{border-left-color:#59d98e!important}.ar *,.ao *,.ag *{color:inherit!important}.ar b,.ao b,.ag b{color:#fff!important}
[data-testid="stPlotlyChart"]{background:var(--dash-card)!important;border:1px solid var(--dash-line);border-radius:8px;padding:.35rem}[data-testid="stDataFrame"]{border:1px solid var(--dash-line);border-radius:8px;overflow:hidden}.stSelectbox label p,.stMultiSelect label p,.stSlider label p{color:#d7d7df!important}.stAlert{background:var(--dash-card-2)!important;border-color:var(--dash-line)!important}.stAlert *{color:#eeeef3!important}hr{border-color:var(--dash-line)!important}#MainMenu,footer,header{visibility:hidden}@media(max-width:900px){.block-container{padding:1rem!important}.kcard{min-height:auto}section[data-testid="stSidebar"]{width:250px!important}}
section[data-testid='stSidebar'] h3:before{content:'';display:inline-block;width:9px;height:9px;background:var(--dash-accent);transform:rotate(45deg);margin-right:.55rem;border-radius:2px}.modebar{display:none!important}[data-testid='stPlotlyChart']:hover{border-color:rgba(255,255,255,.2)}[data-testid='stDataFrame']{background:var(--dash-card)!important}
/* Reference dashboard rebuild */
:root{--canvas:#0c0c13;--sidebar:#171720;--panel:#1b1b25;--panel-hover:#20202c;--stroke:#2b2b38;--ink:#f7f7fa;--muted:#a8a8b7}
html,body,.stApp,[class*="css"]{font-family:"Stack Sans Text","Segoe UI",Arial,sans-serif!important}.stApp{background:var(--canvas)!important}.block-container{max-width:1440px!important;padding:1.65rem 2.25rem 3rem!important}
section[data-testid="stSidebar"]{width:205px!important;background:var(--sidebar)!important;border-right:1px solid var(--stroke)!important}section[data-testid="stSidebar"]>div{padding:2.1rem 1rem!important}section[data-testid="stSidebar"] h3{font-family:"Stack Sans Text","Segoe UI",sans-serif!important;font-size:1.12rem!important;font-weight:720!important;line-height:1.18!important;letter-spacing:-.02em!important;margin:1.8rem .45rem .3rem!important}section[data-testid="stSidebar"] h3:before{width:8px!important;height:8px!important;margin-right:.55rem!important;border-radius:1px!important}section[data-testid="stSidebar"] p{font-size:.75rem!important;line-height:1.45!important;color:#aaaaba!important}section[data-testid="stSidebar"] hr{margin:1.15rem .25rem!important;border-color:var(--stroke)!important}section[data-testid="stSidebar"] div[role="radiogroup"]{gap:.28rem!important}section[data-testid="stSidebar"] div[role="radiogroup"] label{min-height:39px!important;padding:.6rem .72rem!important;border-radius:7px!important}section[data-testid="stSidebar"] div[role="radiogroup"] label p{font-size:.76rem!important;line-height:1.15!important;color:#bcbccc!important}section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){background:var(--dash-accent)!important;box-shadow:0 5px 18px color-mix(in srgb,var(--dash-accent) 22%,transparent)!important}section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p{color:#fff!important;font-weight:700!important}section[data-testid="stSidebar"] [data-baseweb="select"]>div{min-height:42px!important;border-radius:7px!important}
.topbar{padding:.1rem 0 1rem!important;margin:0 0 1.2rem!important;border-bottom:1px solid var(--stroke)!important}.topbar:before{display:none!important}.topbar h1{font-family:"Stack Sans Text","Segoe UI",sans-serif!important;font-size:1.65rem!important;font-weight:680!important;letter-spacing:-.035em!important;line-height:1.15!important}.topbar p{font-size:.78rem!important;line-height:1.5!important;margin-top:.5rem!important;color:var(--muted)!important}
[data-testid="stHorizontalBlock"]{gap:.78rem!important}.kcard{min-height:128px!important;display:flex!important;flex-direction:column!important;justify-content:center!important;padding:1.05rem 1.1rem!important;background:var(--panel)!important;border:1px solid var(--stroke)!important;border-top:1px solid var(--stroke)!important;border-radius:9px!important;position:relative!important;overflow:hidden!important}.kcard:before{content:"";position:absolute;inset:0 auto 0 0;width:3px;background:var(--dash-accent)}.kcard.red:before{background:#ff6969}.kcard.orange:before{background:#f0a34a}.kcard.green:before{background:#48cf8b}.kval{font-family:"Stack Sans Text","Segoe UI",sans-serif!important;font-size:1.85rem!important;font-weight:690!important;line-height:1!important;letter-spacing:-.045em!important}.klbl{margin-top:.7rem!important;font-size:.72rem!important;font-weight:680!important;line-height:1.25!important;letter-spacing:0!important;text-transform:none!important;color:#ededf2!important}.ksub{margin-top:.32rem!important;font-size:.68rem!important;line-height:1.35!important;color:var(--muted)!important}
.ccard{padding:1rem 1.05rem!important;margin:0 0 .7rem!important;background:var(--panel)!important;border:1px solid var(--stroke)!important;border-radius:9px 9px 0 0!important}.ctitle{font-size:.88rem!important;font-weight:680!important;line-height:1.3!important;letter-spacing:-.01em!important}.csub{margin-top:.35rem!important;font-size:.7rem!important;line-height:1.4!important;color:var(--muted)!important}[data-testid="stPlotlyChart"]{margin-top:-.72rem!important;padding:.35rem!important;background:var(--panel)!important;border:1px solid var(--stroke)!important;border-top:0!important;border-radius:0 0 9px 9px!important}.modebar{display:none!important}
h1,h2,h3,h4{font-family:"Stack Sans Text","Segoe UI",sans-serif!important}h2{font-size:1.35rem!important;font-weight:680!important;letter-spacing:-.025em!important;margin-top:1.4rem!important}p,li,label,[data-testid="stMarkdownContainer"]{line-height:1.5}.ar,.ao,.ag{padding:1rem!important;border-radius:8px!important;font-size:.76rem!important;line-height:1.55!important;background:var(--panel)!important}.stDataFrame,[data-testid="stDataFrame"]{font-size:.78rem!important;background:var(--panel)!important;border-color:var(--stroke)!important}.stAlert{border-radius:8px!important}.stSelectbox label p,.stMultiSelect label p,.stSlider label p{font-size:.72rem!important;text-transform:none!important;letter-spacing:0!important}
@media(max-width:900px){section[data-testid="stSidebar"]{width:245px!important}.block-container{padding:1rem!important}[data-testid="stHorizontalBlock"]{gap:.55rem!important}.kcard{min-height:105px!important}}
/* Single viewport dashboard proportions */
.block-container{max-width:none!important;padding:.8rem 1.55rem 1.3rem!important}.topbar{padding:0 0 .65rem!important;margin:0 0 .72rem!important}.topbar h1{font-size:1.38rem!important;line-height:1.1!important}.topbar p{font-size:.7rem!important;margin-top:.32rem!important}.topbar a,.topbar svg,a.header-anchor,[data-testid="stHeaderActionElements"]{display:none!important}
[data-testid="stHorizontalBlock"]{gap:.62rem!important}.kcard{min-height:88px!important;padding:.72rem .82rem!important;border-radius:8px!important}.kval{font-size:1.48rem!important}.klbl{font-size:.65rem!important;margin-top:.46rem!important}.ksub{font-size:.59rem!important;margin-top:.2rem!important}.ccard{padding:.68rem .8rem!important;margin:0 0 .55rem!important;min-height:48px!important}.ctitle{font-size:.75rem!important}.csub{font-size:.61rem!important;margin-top:.2rem!important}[data-testid="stPlotlyChart"]{margin-top:-.57rem!important;padding:.15rem!important}h2{font-size:1.12rem!important;margin:.75rem 0 .5rem!important}.ar,.ao,.ag{padding:.68rem .75rem!important;font-size:.67rem!important;line-height:1.4!important;margin-bottom:.35rem!important}hr{margin:.72rem 0!important}
section[data-testid="stSidebar"]{width:184px!important}section[data-testid="stSidebar"]>div{padding:1rem .75rem!important}section[data-testid="stSidebar"] h3{font-size:.93rem!important;margin:1rem .38rem .18rem!important}section[data-testid="stSidebar"] p{font-size:.62rem!important}section[data-testid="stSidebar"] hr{margin:.72rem .2rem!important}section[data-testid="stSidebar"] div[role="radiogroup"]{gap:.16rem!important}section[data-testid="stSidebar"] div[role="radiogroup"] label{min-height:32px!important;padding:.42rem .58rem!important}section[data-testid="stSidebar"] div[role="radiogroup"] label p{font-size:.64rem!important}section[data-testid="stSidebar"] div[role="radiogroup"] label:nth-child(1) p:before{content:"▦";margin-right:.5rem}section[data-testid="stSidebar"] div[role="radiogroup"] label:nth-child(2) p:before{content:"◫";margin-right:.5rem}section[data-testid="stSidebar"] div[role="radiogroup"] label:nth-child(3) p:before{content:"▤";margin-right:.5rem}section[data-testid="stSidebar"] div[role="radiogroup"] label:nth-child(4) p:before{content:"◎";margin-right:.5rem}section[data-testid="stSidebar"] div[role="radiogroup"] label:nth-child(5) p:before{content:"⌁";margin-right:.5rem}section[data-testid="stSidebar"] [data-baseweb="select"]>div{min-height:34px!important;font-size:.65rem!important}
[data-testid="stDataFrame"]{font-size:.68rem!important}@media(max-width:900px){.block-container{padding:.75rem!important}section[data-testid="stSidebar"]{width:235px!important}}
.csub{display:none!important}
/* Reference composition final */
.block-container{padding:1.35rem 2rem 2rem!important}.topbar{padding:.2rem 0 .8rem!important;margin-bottom:1rem!important}.topbar h1{font-size:1.65rem!important}.topbar p{font-size:.78rem!important}.kcard{min-height:112px!important;padding:1rem 1.05rem!important;border:0!important;border-radius:9px!important;background:#1c1c27!important}.kcard:before{display:none!important}.kval{font-size:1.72rem!important}.klbl{font-size:.73rem!important;margin-top:.65rem!important}.ksub{font-size:.66rem!important}.ccard{min-height:auto!important;padding:.85rem 1rem!important;border:0!important;border-radius:9px 9px 0 0!important;background:#1c1c27!important}.ctitle{font-size:.86rem!important}[data-testid="stPlotlyChart"]{border:0!important;border-radius:0 0 9px 9px!important;background:#1c1c27!important;padding:.25rem .6rem!important}section[data-testid="stSidebar"]{width:220px!important}section[data-testid="stSidebar"]>div{padding:1.5rem 1rem!important}section[data-testid="stSidebar"] h3{font-size:1.05rem!important}section[data-testid="stSidebar"] p{font-size:.7rem!important}section[data-testid="stSidebar"] div[role="radiogroup"] label{min-height:38px!important;padding:.58rem .7rem!important}section[data-testid="stSidebar"] div[role="radiogroup"] label p{font-size:.72rem!important}section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){background:#f5f5f7!important;box-shadow:none!important}section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p{color:#14141d!important}div[data-testid="stVerticalBlock"]{gap:.55rem!important}[data-testid="stExpander"]{border:1px solid #2b2b38!important;background:#171720!important;border-radius:8px!important}
/* Accessible colour and interaction */
.kcard{transition:transform .16s ease,background .16s ease!important;border-top:2px solid var(--dash-accent)!important}.kcard:hover{transform:translateY(-2px)!important;background:#22222e!important}.kcard.red{border-top-color:#ff6b72!important}.kcard.orange{border-top-color:#f3b64b!important}.kcard.green{border-top-color:#4fcf91!important}.kcard.blue,.kcard.gold{border-top-color:var(--dash-accent)!important}[data-testid="stPlotlyChart"]{transition:background .16s ease!important}[data-testid="stPlotlyChart"]:hover{background:#1e1e2a!important}.stSelectbox [data-baseweb="select"]>div:focus-within{border-color:var(--dash-accent)!important}
/* Power BI KPI cards */
.kcard{min-height:108px!important;display:flex!important;flex-direction:column!important;justify-content:flex-start!important;background:#191922!important;border:1px solid #30303c!important;border-radius:5px!important;padding:.9rem 1rem .82rem!important;box-shadow:0 1px 2px rgba(0,0,0,.16)!important;transform:none!important;transition:background .12s ease,border-color .12s ease!important}.kcard:hover{transform:none!important;background:#1d1d27!important;border-color:#414152!important}.kcard:before,.kcard:after{display:none!important}.klbl{order:1!important;display:flex!important;align-items:center!important;gap:.48rem!important;margin:0!important;color:#c9c9d3!important;font-size:.7rem!important;font-weight:560!important;line-height:1.25!important;letter-spacing:0!important;text-transform:none!important}.klbl:before{content:"";width:6px;height:6px;flex:0 0 6px;border-radius:50%;background:var(--dash-accent)}.kcard.red .klbl:before{background:#f06b72}.kcard.orange .klbl:before{background:#e9aa49}.kcard.green .klbl:before{background:#4bc589}.kcard.blue .klbl:before,.kcard.gold .klbl:before{background:var(--dash-accent)}.kval{order:2!important;margin:.5rem 0 0!important;color:#f8f8fb!important;font-family:"Stack Sans Text","Segoe UI",sans-serif!important;font-size:1.72rem!important;font-weight:650!important;line-height:1!important;letter-spacing:-.035em!important;font-variant-numeric:tabular-nums!important;white-space:nowrap!important}.ksub{order:3!important;margin-top:auto!important;padding-top:.5rem!important;color:#8f8f9e!important;font-size:.61rem!important;font-weight:450!important;line-height:1.2!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}
.cross-app-link{position:fixed;top:1rem;right:1.7rem;z-index:9999;display:inline-flex;align-items:center;justify-content:center;padding:.55rem .85rem;background:#f5f5f7;color:#15151f!important;border:1px solid #f5f5f7;border-radius:5px;font:600 .72rem "Stack Sans Text","Segoe UI",sans-serif;text-decoration:none!important;box-shadow:0 2px 8px rgba(0,0,0,.18)}.cross-app-link:hover{background:var(--dash-accent);border-color:var(--dash-accent);color:#fff!important}</style>
""", unsafe_allow_html=True)

def load():
    return pd.read_csv(BASE_DIR / "loan_data_scored.csv", parse_dates=["disburse_date"])

df = load()

with st.sidebar:
    st.markdown("###  Thebe Credit Union")
    st.markdown("Loan Portfolio Dashboard")
    st.markdown("---")
    page = st.radio("Go to", [
        "  Portfolio Overview",
        "  At-Risk Accounts",
        "  Losses & Collections",
        "  Branch Performance",
        "  Customer Insights",
    ])
    st.markdown("---")
    branches = ["All Branches"] + sorted(df["branch"].unique().tolist())
    sel_b    = st.selectbox("Filter: Branch", branches)
    ltypes   = ["All Loan Types"] + sorted(df["loan_type"].unique().tolist())
    sel_l    = st.selectbox("Filter: Loan Type", ltypes)
    st.markdown("---")
    st.caption("Period: Jan 2024  to  Jun 2025")

dff = df.copy()
if sel_b != "All Branches":   dff = dff[dff["branch"]    == sel_b]
if sel_l != "All Loan Types": dff = dff[dff["loan_type"] == sel_l]

def kcard(color, val, lbl, sub=""):
    return f'<div class="kcard {color}"><div class="klbl">{lbl}</div><div class="kval">{val}</div>{"<div class=ksub>"+sub+"</div>" if sub else ""}</div>'

def wchart(fig, h=230):
    palette = ['#6C5CE7','#4E8CFF','#F3B63F','#39C98A']
    for i, trace in enumerate(fig.data):
        if trace.type == "bar":
            point_count = len(trace.x) if trace.x is not None else len(trace.y)
            trace.marker.color = ([palette[j % len(palette)] for j in range(point_count)]
                                  if len(fig.data) == 1 else palette[i % len(palette)])
            trace.marker.line = dict(width=0)
            trace.opacity = 0.94
            trace.hovertemplate = "%{x}<br><b>%{y}</b><extra></extra>"
        elif trace.type in ("scatter", "scattergl"):
            trace.line.color = palette[i % len(palette)]
            trace.line.width = 2.5
            if getattr(trace, "marker", None):
                trace.marker.color = palette[i % len(palette)]
                trace.marker.size = 6
        elif trace.type == "pie":
            trace.marker.colors = palette
            trace.textinfo = "percent"
            trace.textposition = "outside"
    fig.update_layout(plot_bgcolor="#1b1b25", paper_bgcolor="#1b1b25", font_color="#d8d8e2",
                      font=dict(family="Stack Sans Text, Segoe UI, sans-serif", size=11), height=h,
                      margin=dict(t=12,b=18,l=8,r=8), coloraxis_showscale=False, hovermode="closest",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                                  font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
                      hoverlabel=dict(bgcolor="#272735", bordercolor="#3a3a4a", font=dict(color="#ffffff",size=12)))
    fig.update_xaxes(showgrid=False, linecolor="#343443", tickfont=dict(color="#a8a8b7",size=10), title=None, automargin=True, zeroline=False)
    fig.update_yaxes(gridcolor="#2b2b38", linecolor="#343443", tickfont=dict(color="#a8a8b7",size=10), title=None, automargin=True, zeroline=False)
    return fig

#
# PAGE 1 - PORTFOLIO OVERVIEW
#
if page == "  Portfolio Overview":
    st.markdown('<div class="topbar"><h1> Loan Portfolio Overview</h1><p>Thebe Credit Union  |  January 2024  to  June 2025</p></div>', unsafe_allow_html=True)

    total_port  = dff["loan_amount_bwp"].sum()
    outstanding = dff["outstanding_balance"].sum()
    total_loss  = dff["expected_loss_bwp"].sum()
    defaulted   = (dff["payment_status"]=="Defaulted").sum()
    late        = (dff["payment_status"]=="Late (30 to 89 days)").sum()
    current     = (dff["payment_status"]=="Current").sum()

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.markdown(kcard("blue",  f"P{total_port/1e6:.1f}M",    "Total Portfolio",        f"{len(dff):,} loans"), unsafe_allow_html=True)
    c2.markdown(kcard("blue",  f"P{outstanding/1e6:.1f}M",   "Outstanding Balance",    "Still owed by customers"), unsafe_allow_html=True)
    c3.markdown(kcard("red",   f"P{total_loss/1e6:.2f}M",    "Estimated Financial Loss","At risk of not being recovered"), unsafe_allow_html=True)
    c4.markdown(kcard("red",   f"{defaulted:,}",              "Defaulted Accounts",     "Stopped paying"), unsafe_allow_html=True)
    c5.markdown(kcard("green", f"{current:,}",                "Paying on Time",         f"Out of {len(dff):,} total"), unsafe_allow_html=True)

    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ccard"><div class="ctitle">Loan Account Status: All Customers</div><div class="csub">Breakdown of how customers are currently managing their repayments</div>', unsafe_allow_html=True)
        status_c = dff["payment_status"].value_counts().reset_index()
        status_c.columns = ["Status","Count"]
        fig = px.pie(status_c, values="Count", names="Status", hole=0.45,
                     color="Status",
                     color_discrete_map={"Current":"#166534","Early (1 to 29 days)":"#b45309",
                                         "Late (30 to 89 days)":"#c2410c","Defaulted":"#b91c1c"})
        fig.update_traces(textinfo="percent+label", textfont_color="#0f172a")
        st.plotly_chart(wchart(fig, 235), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="ccard"><div class="ctitle">Default Rate by Loan Type</div><div class="csub">Which loan types are causing the most losses</div>', unsafe_allow_html=True)
        lt = dff.groupby("loan_type").agg(
            total=("customer_id","count"), defaults=("will_default","sum"),
            loss=("expected_loss_bwp","sum")).reset_index()
        lt["Default Rate %"] = (lt["defaults"]/lt["total"]*100).round(1)
        lt = lt.sort_values("Default Rate %", ascending=True)
        lt["label"] = lt["Default Rate %"].apply(lambda x: f"{x}%")
        fig2 = px.bar(lt, x="Default Rate %", y="loan_type", orientation="h",
                      color="Default Rate %", color_continuous_scale=["#166534","#b91c1c"],
                      text="label", labels={"loan_type":""})
        fig2.update_traces(textposition="outside", textfont_color="#0f172a")
        fig2.update_layout(showlegend=False)
        st.plotly_chart(wchart(fig2), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

#
# PAGE 2 - AT-RISK ACCOUNTS
#
elif page == "  At-Risk Accounts":
    st.markdown('<div class="topbar"><h1> High-Risk Loan Accounts</h1><p>Accounts most likely to default: prioritise these for immediate contact</p></div>', unsafe_allow_html=True)

    active_accounts = dff[dff["outstanding_balance"] > 0].copy()
    rc = active_accounts["risk_level"].value_counts()
    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kcard("red",    f"{rc.get('Critical',0):,}",    "Critical Risk",    "Needs urgent action now"), unsafe_allow_html=True)
    c2.markdown(kcard("orange", f"{rc.get('High Risk',0):,}",   "High Risk",        "Contact this week"), unsafe_allow_html=True)
    c3.markdown(kcard("blue",   f"{rc.get('Medium Risk',0):,}", "Medium Risk",      "Monitor closely"), unsafe_allow_html=True)
    c4.markdown(kcard("green",  f"{rc.get('Low Risk',0):,}",    "Low Risk",         "Paying well"), unsafe_allow_html=True)

    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ccard"><div class="ctitle">Risk Level Distribution</div><div class="csub">How the full loan portfolio is spread across risk categories</div>', unsafe_allow_html=True)
        fig = px.pie(names=rc.index, values=rc.values, hole=0.45,
                     color=rc.index,
                     color_discrete_map={"Critical":"#b91c1c","High Risk":"#c2410c",
                                         "Medium Risk":"#b45309","Low Risk":"#166534"})
        fig.update_traces(textinfo="percent+label", textfont_color="#0f172a")
        st.plotly_chart(wchart(fig, 340), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="ccard"><div class="ctitle">What Puts a Customer at Risk?</div><div class="csub">The factors that separate customers who default from those who pay reliably</div>', unsafe_allow_html=True)
        compare = pd.DataFrame({
            "Factor":          ["Credit Score","Monthly Income (BWP)","Existing Loans","Previous Defaults","Employment Years"],
            "Good Payers":     [dff[dff["will_default"]==0]["credit_score"].mean(),
                                dff[dff["will_default"]==0]["monthly_income_bwp"].mean(),
                                dff[dff["will_default"]==0]["existing_loans"].mean(),
                                dff[dff["will_default"]==0]["prev_defaults"].mean(),
                                dff[dff["will_default"]==0]["employment_tenure_yrs"].mean()],
            "Defaulters":      [dff[dff["will_default"]==1]["credit_score"].mean(),
                                dff[dff["will_default"]==1]["monthly_income_bwp"].mean(),
                                dff[dff["will_default"]==1]["existing_loans"].mean(),
                                dff[dff["will_default"]==1]["prev_defaults"].mean(),
                                dff[dff["will_default"]==1]["employment_tenure_yrs"].mean()],
        })
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Good Payers",x=compare["Factor"],y=compare["Good Payers"],marker_color="#166534"))
        fig2.add_trace(go.Bar(name="Defaulters", x=compare["Factor"],y=compare["Defaulters"], marker_color="#b91c1c"))
        fig2.update_layout(barmode="group",legend=dict(orientation="h",y=1.1), font_color="#0f172a")
        st.plotly_chart(wchart(fig2), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Active recovery queue")
    st.caption("Recoverable high-risk balances, prioritised by follow-up status and default probability.")
    urgent = active_accounts[active_accounts["risk_level"].isin(["Critical", "High Risk"])].copy()
    urgent["collection_action"] = urgent["collection_action"].fillna("None")
    urgent["action_recorded"] = urgent["collection_action"].ne("None")

    def next_action(row):
        action = row["collection_action"]
        if action == "None":
            if row["payment_status"] == "Defaulted" or row["days_late"] >= 90:
                return "Escalate for legal review"
            if row["days_late"] >= 60:
                return "Arrange customer visit"
            return "Call and agree payment plan"
        follow_up = {
            "SMS Sent": "Call if no response",
            "Letter Sent": "Call if no response",
            "Called": "Confirm payment commitment",
            "Home Visit": "Review visit outcome",
            "Legal Notice": "Monitor legal response",
        }
        return follow_up.get(action, "Review case notes")

    urgent["recommended_action"] = urgent.apply(next_action, axis=1)
    urgent = urgent.sort_values(["action_recorded", "default_probability", "outstanding_balance"],
                                ascending=[True, False, False])
    urgent["default_probability"] = (urgent["default_probability"] * 100).round(1)
    urgent["outstanding_display"] = urgent["outstanding_balance"].apply(lambda x: f"P{x:,.0f}")
    urgent["last_action"] = urgent["collection_action"].replace("None", "No action recorded")
    show = urgent[["customer_id", "outstanding_display", "days_late", "risk_level",
                   "default_probability", "last_action", "recommended_action"]].copy()
    show.columns = ["Customer", "Amount Due", "Days Overdue", "Risk", "Default Probability %",
                    "Last Action", "Recommended Next Action"]
    st.dataframe(show.reset_index(drop=True), use_container_width=True, hide_index=True,
                 column_config={"Default Probability %": st.column_config.ProgressColumn(
                     "Default Probability %", min_value=0, max_value=100, format="%.1f%%")})

    export_columns = ["customer_id", "loan_type", "branch", "loan_officer", "outstanding_balance",
                      "monthly_income_bwp", "days_late", "risk_level", "default_probability",
                      "payment_status", "last_action", "recommended_action"]
    csv = urgent[export_columns].to_csv(index=False).encode()
    st.download_button("Export recovery queue", csv, "active_recovery_queue.csv", "text/csv")

#
# PAGE 3 - LOSSES & COLLECTIONS
#
elif page == "  Losses & Collections":
    st.markdown('<div class="topbar"><h1> Financial Losses & Collections</h1><p>Where money is being lost and what collection steps have been taken</p></div>', unsafe_allow_html=True)

    problem = dff[dff["payment_status"].isin(["Defaulted","Late (30 to 89 days)"])]
    no_action = problem[problem["collection_action"]=="None"]

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kcard("red",    f"P{dff['expected_loss_bwp'].sum()/1e6:.2f}M","Total Expected Loss",      "Across all at-risk accounts"), unsafe_allow_html=True)
    c2.markdown(kcard("red",    f"{len(problem):,}",                           "Accounts Behind on Payment","Late or defaulted"), unsafe_allow_html=True)
    c3.markdown(kcard("orange", f"{len(no_action):,}",                         "No Action Taken Yet",      "Late with zero follow-up"), unsafe_allow_html=True)
    c4.markdown(kcard("blue",   f"P{dff[dff['payment_status']=='Defaulted']['expected_loss_bwp'].sum()/1e6:.2f}M","Loss from Full Defaults","Stopped paying entirely"), unsafe_allow_html=True)

    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ccard"><div class="ctitle">Expected Loss by Loan Type</div><div class="csub">Which loan types are causing the biggest financial losses</div>', unsafe_allow_html=True)
        loss_t = dff.groupby("loan_type")["expected_loss_bwp"].sum().sort_values(ascending=True).reset_index()
        loss_t["label"] = loss_t["expected_loss_bwp"].apply(lambda x: f"P{x/1e3:.0f}K")
        fig = px.bar(loss_t, x="expected_loss_bwp", y="loan_type", orientation="h",
                     color="expected_loss_bwp", color_continuous_scale=["#fee2e2","#b91c1c"],
                     text="label", labels={"expected_loss_bwp":"Loss (BWP)","loan_type":""})
        fig.update_traces(textposition="outside", textfont_color="#0f172a"); fig.update_layout(showlegend=False)
        st.plotly_chart(wchart(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="ccard"><div class="ctitle">Collection Actions Taken on Late Accounts</div><div class="csub">What steps have been taken to recover money from customers falling behind</div>', unsafe_allow_html=True)
        ca = problem["collection_action"].value_counts().reset_index()
        ca.columns = ["Action","Count"]
        fig2 = px.bar(ca, x="Action", y="Count", text="Count",
                      color="Action",
                      color_discrete_map={"None":"#b91c1c","SMS Sent":"#5b8cff",
                                          "Called":"#2563eb","Letter Sent":"#3b82f6",
                                          "Home Visit":"#1e3a8a","Legal Notice":"#422006"})
        fig2.update_traces(textposition="outside", textfont_color="#0f172a"); fig2.update_layout(showlegend=False)
        st.plotly_chart(wchart(fig2), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("###  Late Accounts With NO Collection Action")
    st.caption("These customers are behind on payments and nobody has contacted them yet: priority for outreach")
    if len(no_action) == 0:
        st.success(" All late accounts have had at least one collection action.")
    else:
        show = no_action[["customer_id","loan_type","branch","loan_officer",
                           "outstanding_balance","days_late","payment_status","expected_loss_bwp"]].copy()
        show["outstanding_balance"] = show["outstanding_balance"].apply(lambda x:f"P{x:,.0f}")
        show["expected_loss_bwp"]   = show["expected_loss_bwp"].apply(lambda x:f"P{x:,.0f}")
        show.columns = ["Customer","Loan Type","Branch","Officer","Outstanding",
                        "Days Late","Status","Expected Loss"]
        st.dataframe(show.reset_index(drop=True), use_container_width=True)
        csv = show.to_csv(index=False).encode()
        st.download_button(" Export No-Action List", csv, "no_action_accounts.csv", "text/csv")
    st.markdown('<div class="ar"><b> Action Needed:</b> Every day a late account goes without contact, recovery becomes harder. Research shows that customers contacted within the first 30 days of being late are 3× more likely to catch up than those contacted after 90 days.</div>', unsafe_allow_html=True)

#
# PAGE 4 - BRANCH PERFORMANCE
#
elif page == "  Branch Performance":
    st.markdown('<div class="topbar"><h1> Branch Performance Report</h1><p>How each branch is performing on loan quality and defaults</p></div>', unsafe_allow_html=True)

    br = dff.groupby("branch").agg(
        loans=("customer_id","count"),
        portfolio=("loan_amount_bwp","sum"),
        defaults=("will_default","sum"),
        losses=("expected_loss_bwp","sum"),
        avg_credit=("credit_score","mean")
    ).reset_index()
    br["default_rate"]  = (br["defaults"]/br["loans"]*100).round(1)
    br["loss_rate"]     = (br["losses"]/br["portfolio"]*100).round(2)
    br = br.sort_values("default_rate", ascending=False)

    best_br  = br.iloc[-1]
    worst_br = br.iloc[0]

    c1,c2,c3 = st.columns(3)
    c1.markdown(kcard("blue",  f"{len(br)}",              "Total Branches",       ""), unsafe_allow_html=True)
    c2.markdown(kcard("green", best_br["branch"],          "Best Performing",      f"{best_br['default_rate']}% default rate"), unsafe_allow_html=True)
    c3.markdown(kcard("red",   worst_br["branch"],         "Needs Most Attention", f"{worst_br['default_rate']}% default rate"), unsafe_allow_html=True)

    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ccard"><div class="ctitle">Default Rate by Branch</div><div class="csub">Percentage of loans that have defaulted or are seriously behind</div>', unsafe_allow_html=True)
        br_s = br.sort_values("default_rate", ascending=True)
        br_s["label"] = br_s["default_rate"].apply(lambda x:f"{x}%")
        fig = px.bar(br_s, x="default_rate", y="branch", orientation="h",
                     color="default_rate", color_continuous_scale=["#166534","#b91c1c"],
                     text="label", labels={"default_rate":"Default Rate %","branch":""})
        fig.update_traces(textposition="outside", textfont_color="#0f172a"); fig.update_layout(showlegend=False)
        st.plotly_chart(wchart(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="ccard"><div class="ctitle">Portfolio Size vs Losses by Branch</div><div class="csub">Bigger portfolios are expected to have larger losses: the key is the proportion</div>', unsafe_allow_html=True)
        fig2 = px.scatter(br, x="portfolio", y="losses", size="loans",
                          color="default_rate", color_continuous_scale=["#166534","#b91c1c"],
                          hover_name="branch", text="branch",
                          labels={"portfolio":"Portfolio Value (BWP)","losses":"Expected Losses (BWP)",
                                  "default_rate":"Default Rate %"})
        fig2.update_traces(textposition="top center", textfont_color="#0f172a")
        st.plotly_chart(wchart(fig2), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("###  Branch Summary Table")
    br_show = br.copy()
    br_show["portfolio"] = br_show["portfolio"].apply(lambda x:f"P{x/1e6:.2f}M")
    br_show["losses"]    = br_show["losses"].apply(lambda x:f"P{x/1e3:.0f}K")
    br_show["avg_credit"]= br_show["avg_credit"].apply(lambda x:f"{x:.0f}")
    br_show.columns      = ["Branch","Loans","Portfolio","Defaults","Est. Losses",
                             "Avg Credit Score","Default Rate %","Loss Rate %"]
    st.dataframe(br_show.reset_index(drop=True), use_container_width=True)

    st.markdown("---")
    st.markdown("###  Loan Officer Default Rates")
    st.caption("Officers with consistently high default rates may need additional training or supervision")
    lo = dff.groupby("loan_officer").agg(
        loans=("customer_id","count"), defaults=("will_default","sum"),
        loss=("expected_loss_bwp","sum")).reset_index()
    lo["default_rate"] = (lo["defaults"]/lo["loans"]*100).round(1)
    lo = lo.sort_values("default_rate", ascending=False)
    top10 = lo.head(10)
    fig3 = px.bar(top10, x="loan_officer", y="default_rate",
                  color="default_rate", color_continuous_scale=["#ffedd5","#b91c1c"],
                  text=top10["default_rate"].apply(lambda x:f"{x}%"),
                  labels={"default_rate":"Default Rate %","loan_officer":"Loan Officer"})
    fig3.update_traces(textposition="outside", textfont_color="#0f172a"); fig3.update_layout(showlegend=False)
    st.plotly_chart(wchart(fig3,320), use_container_width=True)

#
# PAGE 5 - CUSTOMER INSIGHTS
#
elif page == "  Customer Insights":
    st.markdown('<div class="topbar"><h1> Customer Profile Insights</h1><p>Understanding which types of customers carry the most risk</p></div>', unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ccard"><div class="ctitle">Default Rate by Occupation</div><div class="csub">Which customer occupations carry the highest risk</div>', unsafe_allow_html=True)
        occ = dff.groupby("occupation").agg(count=("customer_id","count"),defaults=("will_default","sum")).reset_index()
        occ["Default Rate %"] = (occ["defaults"]/occ["count"]*100).round(1)
        occ = occ.sort_values("Default Rate %", ascending=True)
        fig = px.bar(occ, x="Default Rate %", y="occupation", orientation="h",
                     color="Default Rate %", color_continuous_scale=["#166534","#b91c1c"],
                     text=occ["Default Rate %"].apply(lambda x:f"{x}%"),
                     labels={"occupation":""})
        fig.update_traces(textposition="outside", textfont_color="#0f172a"); fig.update_layout(showlegend=False)
        st.plotly_chart(wchart(fig), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="ccard"><div class="ctitle">Credit Score Distribution</div><div class="csub">Where our customers sit on the credit score scale: lower scores mean higher risk</div>', unsafe_allow_html=True)
        fig2 = px.histogram(dff, x="credit_score", nbins=30, color="will_default",
                            color_discrete_map={0:"#166534",1:"#b91c1c"},
                            barmode="overlay", opacity=0.75,
                            labels={"credit_score":"Credit Score","will_default":"Defaulted (1=Yes)"},
                            category_orders={"will_default":[0,1]})
        fig2.update_layout(legend=dict(orientation="h",y=1.1), font_color="#0f172a")
        st.plotly_chart(wchart(fig2), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col3,col4 = st.columns(2)
    with col3:
        st.markdown('<div class="ccard"><div class="ctitle">Income Level vs Default Rate</div><div class="csub">Lower-income customers are significantly more likely to default</div>', unsafe_allow_html=True)
        dff["Income Group"] = pd.cut(dff["monthly_income_bwp"],
            bins=[0,5000,10000,20000,50000,999999],
            labels=["Under P5K","P5K to P10K","P10K to P20K","P20K to P50K","Over P50K"])
        ig = dff.groupby("Income Group",observed=True).agg(count=("customer_id","count"),defaults=("will_default","sum")).reset_index()
        ig["Default Rate %"] = (ig["defaults"]/ig["count"]*100).round(1)
        fig3 = px.bar(ig, x="Income Group", y="Default Rate %",
                      color="Default Rate %", color_continuous_scale=["#166534","#b91c1c"],
                      text=ig["Default Rate %"].apply(lambda x:f"{x}%"))
        fig3.update_traces(textposition="outside", textfont_color="#0f172a"); fig3.update_layout(showlegend=False)
        st.plotly_chart(wchart(fig3), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="ccard"><div class="ctitle">Does Collateral Reduce Default Risk?</div><div class="csub">Customers who offered collateral vs those who did not</div>', unsafe_allow_html=True)
        coll = dff.groupby("has_collateral").agg(count=("customer_id","count"),defaults=("will_default","sum")).reset_index()
        coll["has_collateral"] = coll["has_collateral"].map({1:"Has Collateral",0:"No Collateral"})
        coll["Default Rate %"] = (coll["defaults"]/coll["count"]*100).round(1)
        fig4 = px.bar(coll, x="has_collateral", y="Default Rate %",
                      color="has_collateral",
                      color_discrete_map={"Has Collateral":"#166534","No Collateral":"#b91c1c"},
                      text=coll["Default Rate %"].apply(lambda x:f"{x}%"),
                      labels={"has_collateral":""})
        fig4.update_traces(textposition="outside", textfont_color="#0f172a"); fig4.update_layout(showlegend=False)
        st.plotly_chart(wchart(fig4), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align:center;color:#475569;font-size:.78rem'>Thebe Credit Union | Loan Portfolio Dashboard | Prepared by Unaswi Leonard | 2026</div>", unsafe_allow_html=True)
