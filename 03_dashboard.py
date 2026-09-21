
PAGE_TITLE="Thebe Credit Union | Portfolio Analytics"
ACCENT="#0d5a47"; ACCENT_DARK="#073e31"; ACCENT2="#3f6f92"; SOFT="#e8f2ee"
OVERVIEW_URL="https://una471.github.io/portfolio/projects/loan/overview.html"; OVERVIEW_LABEL="Portfolio Overview"; SOFTWARE_URL="https://loan-management-automation.streamlit.app/?view=software"; 
HERO_IMAGE="screenshots/loan-ui.png"; SEARCH_TEXT="Search customers, branches, loan types or reports..."

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import base64

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title=PAGE_TITLE, page_icon=None, layout="wide", initial_sidebar_state="expanded")

def _img_data(name):
    p = ROOT / "assets" / name
    if not p.exists():
        return ""
    mime = "image/webp" if p.suffix.lower()==".webp" else "image/png"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()

HERO = _img_data(HERO_IMAGE)

STYLE = f"""
<style>
:root{{--bg:#e7e8ea;--shell:#f7f7f6;--panel:#fff;--line:#e7e7e5;--ink:#2d2e30;--muted:#85888d;--accent:{ACCENT};--accent2:{ACCENT2};--soft:{SOFT};--danger:#d75555;--warn:#c88a32;--good:#16865c;}}
html,body,[class*="css"],.stApp{{font-family:"Segoe UI Variable","Segoe UI",Arial,sans-serif!important;color:var(--ink)!important}}
.stApp{{background:var(--bg)!important}}
header[data-testid="stHeader"]{{display:none!important}} #MainMenu,footer,[data-testid="stToolbar"]{{display:none!important}}
.block-container{{max-width:1480px!important;margin:18px auto!important;padding:14px 18px 24px!important;background:var(--shell)!important;border:1px solid #d9d9da!important;border-radius:22px!important;box-shadow:0 2px 10px rgba(40,40,45,.06)!important}}
section[data-testid="stSidebar"]{{width:248px!important;background:#f5f5f4!important;border-right:1px solid #dededc!important}}
section[data-testid="stSidebar"]>div{{padding:26px 16px 18px!important}}
section[data-testid="stSidebar"] h2{{font-size:1.02rem!important;margin:.2rem 8px .1rem!important;letter-spacing:-.02em!important}}
section[data-testid="stSidebar"] .stCaption,section[data-testid="stSidebar"] p{{font-size:.71rem!important;color:#85888b!important}}
section[data-testid="stSidebar"] hr{{border:0!important;border-top:1px solid #ddd!important;margin:1rem 8px!important}}
section[data-testid="stSidebar"] div[role="radiogroup"]{{gap:.05rem!important}}
section[data-testid="stSidebar"] div[role="radiogroup"] label{{min-height:38px!important;padding:.56rem .78rem!important;border-radius:8px!important;margin:0!important;background:transparent!important}}
section[data-testid="stSidebar"] div[role="radiogroup"] label>div:first-child{{display:none!important}}
section[data-testid="stSidebar"] div[role="radiogroup"] label p{{font-size:.76rem!important;color:#74777a!important;font-weight:500!important}}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){{background:var(--soft)!important;box-shadow:inset 3px 0 0 var(--accent)!important}}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p{{color:#252726!important;font-weight:700!important}}
section[data-testid="stSidebar"] [data-baseweb="select"]>div{{min-height:39px!important;background:#fff!important;border:1px solid #dededc!important;border-radius:9px!important}}
section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p{{font-size:.68rem!important;color:#85888b!important;font-weight:500!important}}
.utilitybar{{height:58px;display:flex;align-items:center;gap:12px;background:#f0f0ef;border:1px solid #ededeb;border-radius:14px;padding:8px 12px;margin:0 0 10px}}
.searchbox{{width:min(340px,42vw);height:38px;background:#fff;border:1px solid #ececea;border-radius:20px;color:#999b9d;font-size:.72rem;display:flex;align-items:center;padding:0 14px}}
.searchbox:before{{content:'⌕';font-size:1.03rem;color:#717476;margin-right:8px}} .utility-spacer{{flex:1}} .utility-icon{{width:36px;height:36px;background:#fff;border:1px solid #ececea;border-radius:50%;display:grid;place-items:center;color:#6e7270;font-size:.72rem}} .user-chip{{display:flex;align-items:center;gap:8px}} .avatar{{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:var(--accent);color:#fff;font-size:.66rem;font-weight:700}} .user-name{{font-size:.72rem;font-weight:700;color:#2f3130}} .user-role{{font-size:.61rem;color:#949695;margin-top:3px}}
.hero{{position:relative;min-height:110px;overflow:hidden;border:1px solid var(--line);border-radius:14px;background:#fff;margin-bottom:10px;padding:18px 20px}} .hero:after{{content:'';position:absolute;inset:0 0 0 52%;background-image:linear-gradient(90deg,rgba(255,255,255,.98),rgba(255,255,255,.35)),url('{HERO}');background-size:cover;background-position:center;opacity:.42}} .hero>*{{position:relative;z-index:1}} .hero h1{{font-size:1.48rem!important;line-height:1.05!important;letter-spacing:-.035em!important;margin:0!important;color:#2c2e2f!important}} .hero p{{font-size:.74rem!important;color:#85888b!important;margin:.45rem 0 0!important;max-width:670px;line-height:1.35}}
.section-title{{font-size:.82rem;font-weight:700;color:#343637;margin:.2rem 0 .6rem}} .kcard{{height:112px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:.9rem .9rem .75rem;display:flex;flex-direction:column}} .kcard.primary{{background:linear-gradient(145deg,{ACCENT_DARK},{ACCENT});border-color:{ACCENT};}} .klabel{{font-size:.68rem;font-weight:700;color:#3d3f40;line-height:1.15;min-height:26px}} .kcard.primary .klabel{{color:#e8f6f0}} .kvalue{{font-size:1.72rem;font-weight:700;letter-spacing:-.045em;line-height:1;margin-top:.35rem;color:#292b2c;white-space:nowrap}} .kcard.primary .kvalue{{color:#fff}} .ksub{{font-size:.62rem;color:#16865c;margin-top:auto;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}} .kcard.primary .ksub{{color:#d8f5e8}}
.panel-title{{font-size:.79rem;font-weight:700;color:#343637;margin:0 0 .1rem}} .panel-sub{{font-size:.63rem;color:#949698;margin:0 0 .35rem}}
[data-testid="stPlotlyChart"]{{background:#fff!important;border:1px solid var(--line)!important;border-radius:14px!important;padding:.35rem .45rem .2rem!important;box-shadow:none!important}}
[data-testid="stDataFrame"],[data-testid="stTable"]{{border:1px solid var(--line)!important;border-radius:12px!important;overflow:hidden!important;background:#fff!important}}
div[data-testid="stVerticalBlock"]{{gap:.58rem!important}} div[data-testid="stHorizontalBlock"]{{gap:.65rem!important}}
.stButton>button{{height:34px!important;border-radius:18px!important;border:1px solid var(--accent)!important;background:#fff!important;color:var(--accent)!important;font-size:.69rem!important;font-weight:650!important}}
.side-promo{{height:160px;margin:1rem .1rem 0;border-radius:13px;padding:1rem;display:flex;align-items:flex-end;background:linear-gradient(180deg,rgba(15,25,20,.1),rgba(15,25,20,.72)),url('{HERO}');background-size:cover;background-position:center;color:#fff}} .side-promo strong{{display:block;font-size:.9rem;line-height:1.14;margin-bottom:.4rem;color:#fff}} .side-promo span{{font-size:.63rem;color:#e5eee9;line-height:1.3}}
.small-note{{font-size:.64rem;color:#8f9294}} .status-pill{{display:inline-block;padding:.16rem .48rem;border-radius:999px;background:#edf6f1;color:#1a7655;font-size:.62rem;font-weight:700}}
@media(max-width:1000px){{.block-container{{margin:0!important;border-radius:0!important;padding:10px!important}}section[data-testid="stSidebar"]{{width:232px!important}}.hero:after{{display:none}}.kvalue{{font-size:1.45rem}}}}
.sidebar-brand{{display:flex;align-items:center;gap:10px;margin:0 4px 18px;padding:0 4px 17px;border-bottom:1px solid #d9d9d7}}
.sidebar-brand>span{{display:grid;width:36px;height:36px;place-items:center;border-radius:7px;background:var(--accent);color:#fff;font-size:.66rem;font-weight:800;letter-spacing:.02em}}
.sidebar-brand strong{{display:block;color:var(--ink);font-size:.88rem;line-height:1.15}}
.sidebar-brand small{{display:block;margin-top:3px;color:var(--muted);font-size:.61rem}}
div[data-testid="stTextInput"]{{max-width:520px}}
div[data-testid="stTextInput"] input{{height:38px!important;border:1px solid #ececea!important;border-radius:20px!important;background:#fff!important;color:var(--ink)!important;font-size:.72rem!important}}
div[data-testid="stTextInput"] input:focus{{border-color:var(--accent)!important;box-shadow:0 0 0 2px color-mix(in srgb,var(--accent) 18%,transparent)!important}}
.profile-chip{{height:40px;display:flex;align-items:center;justify-content:flex-end;gap:8px;padding-right:4px}}
.profile-chip>span{{display:grid;width:31px;height:31px;place-items:center;border-radius:50%;background:var(--accent);color:#fff;font-size:.61rem;font-weight:800}}
.profile-chip strong{{display:block;font-size:.65rem;color:var(--ink)}}
.profile-chip small{{display:block;margin-top:2px;font-size:.57rem;color:var(--muted)}}
/* Cohesive project-specific dashboard finish */
.stApp{{background:color-mix(in srgb,var(--soft) 46%,#dfe3e5)!important}}
.block-container{{background:color-mix(in srgb,var(--soft) 28%,#f7f7f6)!important;border-color:color-mix(in srgb,var(--accent) 12%,#d9d9da)!important}}
section[data-testid="stSidebar"]{{background:color-mix(in srgb,var(--soft) 72%,#f4f4f2)!important;border-right-color:color-mix(in srgb,var(--accent) 14%,#d8d8d6)!important}}
section[data-testid="stSidebar"] [data-baseweb="select"]>div{{background:color-mix(in srgb,var(--soft) 35%,#fff)!important;border-color:color-mix(in srgb,var(--accent) 18%,#d7d7d5)!important;color:var(--ink)!important}}
section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p{{color:color-mix(in srgb,var(--ink) 70%,var(--muted))!important;font-weight:650!important}}
.hero{{min-height:126px!important;background-image:linear-gradient(90deg,rgba(18,23,22,.86),rgba(18,23,22,.62) 52%,rgba(18,23,22,.25)),url('{HERO}')!important;background-size:cover!important;background-position:center!important;border-color:color-mix(in srgb,var(--accent) 18%,#d6d6d4)!important}}
.hero:after{{display:none!important}}
.hero h1{{color:#fff!important;text-shadow:0 1px 8px rgba(0,0,0,.24)}}
.hero p{{color:rgba(255,255,255,.88)!important}}
.kcard,.kcard.primary{{height:108px!important;background:color-mix(in srgb,var(--soft) 24%,#fff)!important;border:1px solid color-mix(in srgb,var(--accent) 15%,#dededc)!important;border-top:3px solid color-mix(in srgb,var(--accent) 72%,#fff)!important}}
.kcard.primary .klabel,.kcard .klabel{{color:color-mix(in srgb,var(--ink) 82%,var(--accent))!important}}
.kcard.primary .kvalue,.kcard .kvalue{{color:var(--ink)!important}}
.kcard.primary .ksub,.kcard .ksub{{color:color-mix(in srgb,var(--accent) 68%,var(--muted))!important}}
[data-testid="stPlotlyChart"]{{background:color-mix(in srgb,var(--soft) 15%,#fff)!important;border-color:color-mix(in srgb,var(--accent) 12%,#dededc)!important}}
[data-testid="stDataFrame"],[data-testid="stTable"]{{background:color-mix(in srgb,var(--soft) 15%,#fff)!important;border-color:color-mix(in srgb,var(--accent) 12%,#dededc)!important}}
.panel-title{{margin:.48rem 0 .08rem!important;color:var(--ink)!important}}
.panel-sub{{margin:0 0 .42rem!important;color:var(--muted)!important}}
.modebar{{display:none!important}}
.side-promo{{display:none!important}}
.sidebar-brand{{border-bottom-color:color-mix(in srgb,var(--accent) 18%,#d7d7d5)!important}}
.sidebar-brand>span{{background:transparent!important;color:var(--accent)!important;width:38px;height:38px;border-radius:0!important}}
.sidebar-brand.health>span{{position:relative;font-size:0}}
.sidebar-brand.health>span:before,.sidebar-brand.health>span:after{{content:'';position:absolute;width:19px;height:28px;border-radius:100% 0 100% 0;background:var(--accent);transform:rotate(-35deg);left:3px;top:5px}}
.sidebar-brand.health>span:after{{left:16px;transform:scaleX(-1) rotate(-35deg);background:var(--accent2)}}
.sidebar-brand.mining>span{{font-size:0;border-left:3px solid var(--accent2)!important;transform:skewX(-12deg);position:relative}}
.sidebar-brand.mining>span:before{{content:'≡';font-size:2rem;font-weight:900;line-height:1;color:var(--accent2);position:absolute;left:6px;top:0}}
.sidebar-brand.loan>span{{border:2px solid var(--accent)!important;border-radius:50%!important;font-size:.58rem!important;font-weight:800!important}}
.sidebar-brand.retail>span{{display:none!important}}
.sidebar-brand.retail strong{{font-weight:850!important;letter-spacing:.07em!important;text-transform:uppercase}}
.sidebar-brand.tourism>span{{display:none!important}}
.sidebar-brand.tourism>div{{border-left:4px solid var(--accent2);padding-left:10px}}
/* Image-backed navigation and high-contrast light report */
section[data-testid="stSidebar"]>div:first-child{{min-height:100vh!important;padding:10px 14px 18px!important;background-image:linear-gradient(rgba(12,22,20,.78),rgba(12,22,20,.88)),url('{HERO}')!important;background-size:cover!important;background-position:center!important}}
section[data-testid="stSidebar"] h1,section[data-testid="stSidebar"] h2,section[data-testid="stSidebar"] h3,section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] .stCaption{{color:rgba(255,255,255,.88)!important}}
section[data-testid="stSidebar"] hr{{border-top-color:rgba(255,255,255,.22)!important}}
section[data-testid="stSidebar"] div[role="radiogroup"] label p{{color:rgba(255,255,255,.76)!important}}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{{background:rgba(255,255,255,.10)!important}}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked){{background:rgba(255,255,255,.16)!important;box-shadow:inset 3px 0 0 color-mix(in srgb,var(--accent2) 70%,#fff)!important}}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p{{color:#fff!important}}
section[data-testid="stSidebar"] [data-baseweb="select"]>div{{background:rgba(255,255,255,.92)!important;border-color:rgba(255,255,255,.34)!important;color:#202523!important}}
section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p{{color:#fff!important}}
.sidebar-brand{{margin:0 2px 12px!important;padding:0 2px 12px!important;border-bottom-color:rgba(255,255,255,.24)!important}}
.sidebar-brand strong{{color:#fff!important;text-shadow:0 1px 6px rgba(0,0,0,.35)}}
.sidebar-brand small{{color:rgba(255,255,255,.72)!important}}
.sidebar-brand>span{{color:#fff!important}}
.sidebar-brand.loan>span{{border-color:#fff!important}}
.sidebar-brand.health>span:before{{background:#fff!important}}
.sidebar-brand.health>span:after{{background:color-mix(in srgb,var(--accent2) 72%,#fff)!important}}
.sidebar-brand.mining>span{{border-left-color:var(--accent2)!important}}
section[data-testid="stSidebarCollapseButton"] button{{color:#fff!important;background:rgba(0,0,0,.18)!important}}
.kcard,.kcard.primary{{border:0!important;border-top:0!important;background:linear-gradient(140deg,color-mix(in srgb,var(--accent) 88%,#21302b),color-mix(in srgb,var(--accent2) 62%,var(--accent)))!important;box-shadow:0 3px 10px rgba(24,34,31,.12)!important}}
.kcard .klabel,.kcard.primary .klabel{{color:rgba(255,255,255,.84)!important}}
.kcard .kvalue,.kcard.primary .kvalue{{color:#fff!important;text-shadow:0 1px 5px rgba(0,0,0,.18)}}
.kcard .ksub,.kcard.primary .ksub{{color:rgba(255,255,255,.76)!important}}
[data-testid="stPlotlyChart"]{{background:#fff!important;border:1px solid color-mix(in srgb,var(--accent) 10%,#d9dddb)!important}}
[data-testid="stDataFrame"]{{background:#fff!important;border:1px solid color-mix(in srgb,var(--accent) 12%,#d5d9d7)!important}}
[data-testid="stDataFrame"] button{{color:#26312c!important}}
/* Exact software-brand lockup and sidebar action */
section[data-testid="stSidebar"] [data-testid="stSidebarContent"]{{padding-top:0!important}}
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"]{{padding-top:8px!important}}
.sidebar-brand{{margin-top:0!important;align-items:center!important}}
.sidebar-brand.loan>span{{display:none!important}}
.sidebar-brand.loan strong{{font-weight:780!important;letter-spacing:-.02em}}
.sidebar-brand.retail strong{{font-weight:900!important;letter-spacing:.09em!important}}
.sidebar-brand.tourism strong{{letter-spacing:-.025em!important}}
.sidebar-brand.mining>span:before{{content:''!important;position:absolute!important;left:7px!important;top:7px!important;width:28px!important;height:3px!important;background:var(--accent2)!important;box-shadow:-2px 9px 0 var(--accent2),-5px 18px 0 var(--accent2)!important}}
section[data-testid="stSidebar"] .stLinkButton a{{min-height:38px!important;border:1px solid rgba(255,255,255,.55)!important;background:rgba(255,255,255,.15)!important;color:#fff!important;border-radius:7px!important;font-weight:750!important}}
section[data-testid="stSidebar"] .stLinkButton a:hover{{background:#fff!important;color:var(--accent)!important}}
/* Top-aligned identity and report actions */
.sidebar-brand{{position:relative!important;left:-24px!important;top:-6px!important;width:calc(100% + 24px)!important;margin-bottom:2px!important;padding:8px 0 12px 8px!important}}
.report-actions-spacer{{flex:1}}
div[data-testid="stHorizontalBlock"]:has(#top_overview){{margin:0 0 .1rem!important}}
.stButton>button,.stLinkButton>a{{font-weight:700!important}}
</style>
"""
st.markdown(STYLE, unsafe_allow_html=True)

def kcard(label, value, sub="", primary=False):
    return f'<div class="kcard {"primary" if primary else ""}"><div class="klabel">{label}</div><div class="kvalue">{value}</div><div class="ksub">{sub}</div></div>'

def sidebar_brand(mark, name, tag):
    st.markdown(f'<div class="sidebar-brand {mark.lower()}"><span>{mark}</span><div><strong>{name}</strong><small>{tag}</small></div></div>', unsafe_allow_html=True)

def _open_overview():
    st.session_state["active_report_page"] = OVERVIEW_LABEL

def _open_section():
    selected = st.session_state.get("section_nav")
    if selected:
        st.session_state["active_report_page"] = selected

def sidebar_navigation(options):
    st.radio("Go to", options, index=None, key="section_nav", on_change=_open_section, label_visibility="collapsed")
    return st.session_state.get("active_report_page", OVERVIEW_LABEL)

def utilitybar(role):
    spacer, overview_col, software_col = st.columns([6, 1.05, 1.25])
    with overview_col:
        st.link_button("Overview", OVERVIEW_URL, use_container_width=True)
    with software_col:
        st.link_button("Open software", SOFTWARE_URL, use_container_width=True)
    return ""

def apply_search(frame, query):
    if not query or frame.empty:
        return frame
    matches = frame.astype(str).apply(lambda column: column.str.contains(query, case=False, regex=False, na=False)).any(axis=1)
    return frame.loc[matches]


def hero(title, subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)

def panel_head(title, sub=""):
    st.markdown(f'<div class="panel-title">{title}</div><div class="panel-sub">{sub}</div>', unsafe_allow_html=True)

def chart_style(fig, height=270, legend=True):
    fig.update_layout(height=height, margin=dict(l=12,r=12,t=22,b=10), paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", font=dict(family="Segoe UI, Arial",size=11,color="#303634"), showlegend=legend, legend=dict(orientation="h",yanchor="bottom",y=1.01,xanchor="right",x=1,font=dict(size=9)), hoverlabel=dict(bgcolor="#2f3332",font=dict(color="#fff",size=10)), coloraxis_showscale=False)
    fig.update_xaxes(showgrid=False,linecolor="#cfd5d2",tickfont=dict(size=10,color="#424946"),title_font=dict(size=9),zeroline=False)
    fig.update_yaxes(gridcolor="#e2e6e4",linecolor="#cfd5d2",tickfont=dict(size=10,color="#424946"),title_font=dict(size=9),zeroline=False)
    return fig

@st.cache_data
def load_data():
    p=ROOT/"loan_data_scored.csv"
    d=pd.read_csv(p if p.exists() else ROOT/"loan_data.csv",parse_dates=['disburse_date']); return d
loans=load_data()
with st.sidebar:
    sidebar_brand("TCU", "Thebe Credit Union", "Loan Management")
    page=st.radio("Go to",["Portfolio Overview","At-Risk Accounts","Losses & Collections","Branches","Customer Insights"],index=0,label_visibility="collapsed")
    st.divider(); branches=["All Branches"]+sorted(loans.branch.dropna().unique().tolist()); types=["All Loan Types"]+sorted(loans.loan_type.dropna().unique().tolist()); branch_sel=st.selectbox("Branch",branches,index=0); type_sel=st.selectbox("Loan Type",types,index=0)
    st.divider(); st.caption("Portfolio: 2024 to 2025"); st.markdown('<div class="side-promo"><div><strong>Responsible lending. Stronger financial futures.</strong><span>Portfolio quality, collections and customer risk in one view.</span></div></div>',unsafe_allow_html=True)
df=loans.copy()
if branch_sel!="All Branches": df=df[df.branch==branch_sel]
if type_sel!="All Loan Types": df=df[df.loan_type==type_sel]
search_query=utilitybar("Credit Analyst")
df=apply_search(df,search_query)

def money(x): return f"P{x/1e6:.1f}M" if abs(x)>=1e6 else f"P{x/1e3:.0f}K" if abs(x)>=1e3 else f"P{x:,.0f}"

def overview():
    hero("Loan Portfolio Overview","Track portfolio size, repayment quality, expected loss and customer risk across the credit union.")
    portfolio=df.loan_amount_bwp.sum(); out=df.outstanding_balance.sum(); loss=df.expected_loss_bwp.sum(); defaults=int(df.will_default.sum()); default_rate=defaults/max(len(df),1)*100; customers=df.customer_id.nunique(); score=df.credit_score.mean()
    cols=st.columns(7); vals=[("Total Portfolio",money(portfolio),f"{customers:,} customers"),("Outstanding",money(out),"Current balance"),("Expected Loss",money(loss),"Modelled exposure"),("Defaulted Accounts",f"{defaults:,}",f"{default_rate:.1f}% of accounts"),("Avg Credit Score",f"{score:.0f}","Selected portfolio"),("Avg Interest Rate",f"{df.interest_rate_pct.mean():.1f}%","Weighted by accounts"),("Avg Loan Size",money(df.loan_amount_bwp.mean()),"Per account")]
    for i,v in enumerate(vals): cols[i].markdown(kcard(*v,primary=i==0),unsafe_allow_html=True)
    c1,c2,c3=st.columns([1.2,1,1])
    with c1:
        panel_head("Loan Amount by Type","Portfolio composition"); q=df.groupby('loan_type').loan_amount_bwp.sum().sort_values().reset_index(); fig=px.bar(q,x='loan_amount_bwp',y='loan_type',orientation='h',color_discrete_sequence=[ACCENT]); st.plotly_chart(chart_style(fig,255,False),use_container_width=True)
    with c2:
        panel_head("Risk Distribution","Modelled customer risk");
        if 'risk_level' in df.columns: q=df.risk_level.value_counts().reset_index(); q.columns=['risk_level','count']; fig=px.pie(q,names='risk_level',values='count',hole=.58,color='risk_level',color_discrete_map={'Low Risk':ACCENT,'Low':'#5a9b82','Medium':'#d4a35d','High':'#c6674d','Critical':'#9c3f3f'}); st.plotly_chart(chart_style(fig,255,False),use_container_width=True)
        else: st.info("Risk-level field is not available in this file.")
    with c3:
        panel_head("Expected Loss by Branch","Where exposure is concentrated"); q=df.groupby('branch').expected_loss_bwp.sum().sort_values().reset_index(); fig=px.bar(q,x='expected_loss_bwp',y='branch',orientation='h',color_discrete_sequence=[ACCENT2]); st.plotly_chart(chart_style(fig,255,False),use_container_width=True)
    st.markdown('<div class="section-title">Highest-Risk Accounts</div>',unsafe_allow_html=True)
    cols=['customer_id','branch','loan_type','outstanding_balance','payment_status','days_late','expected_loss_bwp']; cols += ['risk_level'] if 'risk_level' in df.columns else []
    q=df.sort_values('expected_loss_bwp',ascending=False)[cols].head(15); st.dataframe(q,use_container_width=True,hide_index=True,height=320)

def risk_page():
    hero("At-Risk Accounts","Focus collections and relationship management on customers with the highest expected loss and delinquency.")
    cols=['customer_id','branch','loan_type','outstanding_balance','payment_status','days_late','missed_payments','expected_loss_bwp']; cols += ['risk_level'] if 'risk_level' in df.columns else []; st.dataframe(df.sort_values(['expected_loss_bwp','days_late'],ascending=False)[cols].head(50),use_container_width=True,hide_index=True,height=540)

def losses_page():
    hero("Losses & Collections","Track expected loss, late accounts and collection actions.")
    q=df.groupby('collection_action').agg(accounts=('customer_id','count'),expected_loss=('expected_loss_bwp','sum'),outstanding=('outstanding_balance','sum')).reset_index(); st.dataframe(q,use_container_width=True,hide_index=True,height=420)

def branch_page():
    hero("Branch Performance","Compare portfolio size, expected loss and repayment risk by branch.")
    q=df.groupby('branch').agg(accounts=('customer_id','count'),portfolio=('loan_amount_bwp','sum'),outstanding=('outstanding_balance','sum'),expected_loss=('expected_loss_bwp','sum'),defaults=('will_default','sum')).reset_index(); q['default_rate_pct']=q.defaults/q.accounts*100; st.dataframe(q,use_container_width=True,hide_index=True,height=500)

def customer_page():
    hero("Customer Insights","Explore income, credit quality, payment burden and loan characteristics.")
    fig=px.scatter(df.sample(min(len(df),1200),random_state=7),x='monthly_income_bwp',y='loan_amount_bwp',color='will_default',opacity=.55,color_discrete_map={0:ACCENT,1:'#c65d51'}); st.plotly_chart(chart_style(fig,420),use_container_width=True)

{"Portfolio Overview":overview,"At-Risk Accounts":risk_page,"Losses & Collections":losses_page,"Branches":branch_page,"Customer Insights":customer_page}[page]()
