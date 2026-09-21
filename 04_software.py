"""
THEBE CREDIT UNION - LOAN MANAGEMENT SYSTEM
The software that solves the problem.
Loan officers use this to: screen applications, review existing accounts,
log collection actions, and track the credit review pipeline.
Run: streamlit run 04_software.py --server.port 8502
"""

import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib, json
from datetime import datetime, date, timedelta

BASE_DIR = Path(__file__).resolve().parent


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Momo+Trust+Display&family=Red+Hat+Display:wght@500;600;700;800&family=Stack+Sans+Text:wght@400;500;600;700&display=swap');
:root{--ink:#0b0b14;--muted:#555966;--panel:#f7f7f9;--line:#dedee5;--blue:#147bd1;--lime:#a9e85a;--purple:#7c24cc;}
html,body,[class*="css"],input,button,textarea,select{font-family:'Poppins',sans-serif!important;color:var(--ink);}
.stApp{background:#fff;}
.block-container{max-width:1180px;padding:2rem 2.5rem 4rem;}
h1,h2,h3,h4,p,label{color:var(--ink);}
h3{font-size:1.45rem!important;font-weight:700!important;letter-spacing:-.04em;margin-top:1.2rem!important;}
h4{font-size:1.08rem!important;font-weight:700!important;letter-spacing:-.025em;}
.app-hero{text-align:center;padding:1.1rem 1rem 2.3rem}.app-hero .brand{font-size:.73rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:#626675;margin-bottom:1.1rem}.app-hero h1{max-width:720px;margin:0 auto;font-size:3.25rem;line-height:1.03;letter-spacing:-.065em;font-weight:800}.app-hero h1 span{color:var(--blue)}.app-hero p{max-width:610px;margin:1rem auto 0;color:#515563;font-size:.95rem;line-height:1.7}
.overview-panel{display:grid;grid-template-columns:1.05fr .95fr;gap:3rem;align-items:center;background:var(--panel);border-radius:30px;padding:2.2rem 2.5rem;margin-bottom:1.2rem;border:1px solid #f0f0f3}.overview-copy .eyebrow{color:var(--blue);font-weight:800;font-size:.76rem;letter-spacing:.12em;text-transform:uppercase}.overview-copy h2{font-size:2rem;line-height:1.08;letter-spacing:-.05em;margin:.55rem 0 .8rem;font-weight:800}.overview-copy p{color:var(--muted);font-size:.86rem;line-height:1.65;margin:0}
.balance-card{position:relative;background:var(--lime);border-radius:24px;padding:1.4rem 1.5rem;transform:rotate(2deg);box-shadow:0 18px 35px rgba(42,50,25,.13);color:#172006}.balance-card small{font-weight:700;color:#26310e}.balance-card strong{display:block;font-size:2rem;letter-spacing:-.05em;margin:.25rem 0;color:#111804}.balance-card p{font-size:.7rem;color:#344214;margin:0}.balance-actions{display:flex;gap:.5rem;position:absolute;right:1.1rem;top:1.15rem}.balance-actions i{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:#fff;color:#111804;font-style:normal;font-weight:800}.mini-chart{height:90px;display:flex;align-items:flex-end;gap:10px;margin:1.2rem .3rem 0}.mini-chart b{display:block;flex:1;border-radius:9px 9px 3px 3px;background:rgba(255,255,255,.68)}.mini-chart b:nth-child(3){background:linear-gradient(#7c24cc,#147bd1,#75bd2c)}
.nav-label{text-align:center;font-size:.7rem;text-transform:uppercase;letter-spacing:.14em;color:#626675;font-weight:800;margin:1.7rem 0 .5rem}div[data-testid="stRadio"]>div{justify-content:center;gap:.35rem;background:#0b0b14;border-radius:999px;padding:.42rem}div[data-testid="stRadio"] label{padding:.62rem .9rem;border-radius:999px;margin:0!important}div[data-testid="stRadio"] label:has(input:checked){background:#fff}div[data-testid="stRadio"] label p{color:#fff!important;font-size:.76rem;font-weight:700;white-space:nowrap}div[data-testid="stRadio"] label:has(input:checked) p{color:#0b0b14!important}div[data-testid="stRadio"] div[role="radiogroup"]>label>div:first-child{display:none}
.topbar{position:relative;overflow:hidden;background:var(--panel);padding:2rem 2.2rem;border-radius:28px;margin-bottom:1.6rem;border:1px solid #f0f0f3;}
.topbar:after{content:"";position:absolute;width:230px;height:230px;right:-60px;top:-105px;border-radius:50%;background:linear-gradient(135deg,var(--purple),#5fa6ff);opacity:.12;}
.topbar h1{position:relative;margin:0;font-size:2rem;color:var(--ink);font-weight:700;letter-spacing:-.05em;z-index:1;}
.topbar h1::first-letter{color:var(--blue);}
.topbar p{position:relative;margin:.6rem 0 0;font-size:.9rem;line-height:1.65;color:var(--muted);z-index:1;}
.kcard{min-height:132px;background:var(--panel);border-radius:22px;padding:1.25rem 1.35rem;border:1px solid #f0f0f3;margin-bottom:.5rem;color:var(--ink);box-shadow:0 12px 30px rgba(13,15,28,.035);}
.kcard.red{background:#fff0ef}.kcard.orange{background:#fff6e9}.kcard.green{background:var(--lime)}.kcard.blue{background:#eaf5ff}
.kval{font-size:1.85rem;font-weight:800;color:var(--ink);letter-spacing:-.045em;}
.klbl{font-size:.68rem;text-transform:uppercase;letter-spacing:1.2px;color:var(--ink);margin-top:.35rem;font-weight:800;}
.ksub{font-size:.74rem;color:#454954;margin-top:.35rem;font-weight:500;}
.result-approve,.result-review,.result-decline{border:0;border-radius:24px;padding:1.8rem;margin:1rem 0;color:var(--ink);box-shadow:0 14px 35px rgba(13,15,28,.06)}
.result-approve{background:var(--lime)}.result-review{background:#efe3ff}.result-decline{background:#ffe8e6}
.result-approve *, .result-review *, .result-decline *{color:var(--ink)!important;}
.flag-box,.action-card{background:var(--panel);border-radius:16px;padding:1rem 1.15rem;margin:.5rem 0;color:var(--ink);border:1px solid var(--line);}
.action-card.done{border-left:5px solid #76c931;opacity:.75}.action-card.pending{border-left:5px solid #ff5b52}
section[data-testid="stSidebar"]{display:none!important;}
.stTextInput input,.stNumberInput input,.stTextArea textarea{background:#fff!important;color:var(--ink)!important;border:1px solid var(--line)!important;border-radius:12px!important;}
.stTextInput label,.stNumberInput label,.stSelectbox label,.stTextArea label,.stCheckbox label{color:var(--ink)!important;font-size:.82rem!important;font-weight:500!important;letter-spacing:-.01em;}
.stSelectbox div[data-baseweb="select"]>div{background:#fff!important;color:var(--ink)!important;border-color:var(--line)!important;border-radius:12px!important;}
input,textarea,select,[contenteditable="true"],div[role="textbox"]{caret-color:var(--ink)!important;}
.stButton>button{background:#0b0b14;color:#fff;border:0;border-radius:999px;padding:.7rem 1.5rem;font-weight:700;width:100%;box-shadow:none;transition:.2s ease;}
.stButton>button p,.stButton>button span,.stButton>button div{color:#fff!important;font-weight:700!important;}
.stButton>button:hover{background:var(--blue);color:#fff;transform:translateY(-1px);}
.stCaptionContainer,.stCaptionContainer p,[data-testid="stCaptionContainer"],[data-testid="stCaptionContainer"] p{color:#454954!important;font-weight:500!important;}
div[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:18px;overflow:hidden;}
div[data-testid="stAlert"]{border-radius:16px;}
hr{border-color:var(--line)!important;margin:1.5rem 0!important;}
#MainMenu,footer,header{visibility:hidden;}
@media(max-width:900px){.overview-panel{grid-template-columns:1fr;gap:1.5rem}.app-hero h1{font-size:2.35rem}div[data-testid="stRadio"]>div{justify-content:flex-start;overflow-x:auto;border-radius:18px}.block-container{padding:1.2rem}.topbar{padding:1.5rem;border-radius:22px}.kcard{min-height:auto}}
/* Portfolio typography: expressive brand, editorial headings, highly legible UI. */
html,body,[class*="css"],p,label,input,button,select,textarea{font-family:'Stack Sans Text','Segoe UI',sans-serif!important}
h1,h2,h3,h4{font-family:'Red Hat Display','Segoe UI',sans-serif!important;letter-spacing:-.035em}
.brand-name,.brand strong,.logo-text{font-family:'Momo Trust Display','Red Hat Display',sans-serif!important}
.hero h1,.hero-copy h1{font-family:'Red Hat Display','Segoe UI',sans-serif!important;font-weight:700;letter-spacing:-.055em}
.metric-value,.kval,[data-testid="stMetricValue"]{font-family:'Red Hat Display','Segoe UI',sans-serif!important;font-variant-numeric:tabular-nums}
button,div[data-testid="stRadio"] label p,.eyebrow,.nav-label{font-family:'Stack Sans Text','Segoe UI',sans-serif!important}
.app-hero{padding:.9rem 1rem 1.15rem}.app-hero .brand{margin-bottom:.55rem}.app-hero h1{font-size:2.5rem;max-width:760px}.app-hero p{max-width:680px;margin-top:.55rem}.overview-panel{display:grid!important;grid-template-columns:1fr .85fr;gap:1.2rem;padding:1.35rem 1.6rem;margin-bottom:.8rem}.overview-panel h2{font-size:1.65rem;margin:.35rem 0}.overview-panel p{font-size:.74rem}.balance-card{min-height:175px;padding:1rem 1.2rem}.balance-card strong{font-size:1.45rem}.mini-chart{height:58px}.nav-label{margin-top:.35rem}.workspace-note{display:flex;justify-content:space-between;gap:1.2rem;align-items:center;background:#eef5fb;border-left:4px solid var(--blue);padding:.8rem 1rem;margin:.2rem 0 .85rem}.workspace-note b{font-size:.78rem}.workspace-note span{font-size:.72rem;color:var(--muted)}div[data-testid="stRadio"]{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.96);padding:.35rem 0;backdrop-filter:blur(10px)}input:focus,button:focus,[data-baseweb="select"]:focus-within{outline:3px solid rgba(20,123,209,.22)!important;outline-offset:2px}.stButton>button{min-height:44px}.stButton>button:disabled{opacity:.55}.field-help{font-size:.72rem;color:var(--muted);margin:-.25rem 0 .75rem}.data-hint{font-size:.72rem;color:var(--muted);margin:.2rem 0 .8rem}@media(max-width:900px){.overview-panel{grid-template-columns:1fr!important}.balance-card{min-height:150px}}
.topbar{border-radius:14px!important;padding:1.35rem 1.6rem!important}.topbar p{max-width:720px!important;font-size:.84rem!important;line-height:1.55!important;color:#4b5563!important}.result-approve *,.result-review *,.result-decline *{color:#111827!important}.flag-box{color:#1f2937!important;background:#fff!important}.kcard *,.workspace-note *{opacity:1!important}.stAlert,.stAlert *{color:#172033!important}.stTextInput label p,.stNumberInput label p,.stSelectbox label p,.stTextArea label p,.stCheckbox label p{color:#202735!important;font-size:.82rem!important}.composition{display:grid;grid-template-columns:160px 1fr;gap:1rem;padding:1rem 1.2rem;background:#f8fafc;border:1px solid #e2e8f0;margin:.8rem 0}.composition b{font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;color:#147bd1}.composition p{margin:0;max-width:760px;color:#4b5563;line-height:1.55;font-size:.82rem}@media(max-width:700px){.composition,.workspace-note{grid-template-columns:1fr;display:grid}}
.workspace-note b{color:#123b66!important;opacity:1!important;font-weight:700!important}.workspace-note span{color:#40514c!important;opacity:1!important}
.cross-app-link{position:fixed;top:1rem;right:1.7rem;z-index:9999;display:inline-flex;align-items:center;justify-content:center;padding:.62rem 1rem;background:#11131a;color:#fff!important;border:1px solid rgba(255,255,255,.18);border-radius:5px;font:650 .78rem "Stack Sans Text","Segoe UI",sans-serif;text-decoration:none!important;box-shadow:0 3px 12px rgba(0,0,0,.18)}.cross-app-link:hover{transform:translateY(-1px);filter:brightness(1.12)}</style>
""", unsafe_allow_html=True)

# ── LOAD ──────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    m  = joblib.load(BASE_DIR / "model.pkl")
    lb = joblib.load(BASE_DIR / "le_branch.pkl")
    ll = joblib.load(BASE_DIR / "le_ltype.pkl")
    lo = joblib.load(BASE_DIR / "le_occ.pkl")
    with open(BASE_DIR / "features.json") as f: feat = json.load(f)
    return m, lb, ll, lo, feat

@st.cache_data
def load_data():
    return pd.read_csv(BASE_DIR / "loan_data_scored.csv", parse_dates=["disburse_date"])

model, le_branch, le_ltype, le_occ, FEATURES = load_model()
df = load_data()

# Session state
if "applications" not in st.session_state: st.session_state.applications = []
if "collection_log" not in st.session_state: st.session_state.collection_log = []

BRANCHES   = sorted(le_branch.classes_.tolist())
LOAN_TYPES = sorted(le_ltype.classes_.tolist())
OCCUPATIONS= sorted(le_occ.classes_.tolist())

def kcard(color, val, lbl, sub=""):
    return f'<div class="kcard {color}"><div class="kval">{val}</div><div class="klbl">{lbl}</div>{"<div class=ksub>"+sub+"</div>" if sub else ""}</div>'

def dchart(fig, h=300):
    fig.update_layout(plot_bgcolor="#f7f7f9", paper_bgcolor="#f7f7f9", font_color="#0b0b14",
                      font_family="Poppins", height=h, margin=dict(t=15,b=10,l=5,r=5),
                      template="plotly_white", colorway=["#147bd1", "#75a832", "#7c24cc", "#11111a"])
    fig.update_xaxes(gridcolor="#e8e8ed", zerolinecolor="#e8e8ed")
    fig.update_yaxes(gridcolor="#e8e8ed", zerolinecolor="#e8e8ed")
    return fig

# ── EDITORIAL APP HEADER + NAVIGATION ─────────────────────────────
pending_apps = len([a for a in st.session_state.applications if a["decision"] == "Under Review"])
crit_accounts = (df["risk_level"] == "Critical").sum()

st.markdown("""
<div class="app-hero">
  <div class="brand">Thebe Credit Union · Loan Management</div>
  <h1><span>Empower</span> Your Lending Decisions</h1>
  <p>Screen applications, understand portfolio risk and manage collections from one intelligent financial workspace.</p>
</div>
<div class="overview-panel">
  <div class="overview-copy">
    <div class="eyebrow">Financial analytics dashboard</div>
    <h2>Clear decisions.<br>Healthier loans.</h2>
    <p>See the information that matters, act on risk early and keep every application moving with confidence.</p>
  </div>
  <div class="balance-card">
    <small>Portfolio overview</small><strong>Live loan health</strong>
    <p>Real-time risk and application monitoring</p>
    <div class="balance-actions"><i>↑</i><i>↓</i><i>↗</i></div>
    <div class="mini-chart"><b style="height:38%"></b><b style="height:58%"></b><b style="height:92%"></b><b style="height:66%"></b><b style="height:48%"></b><b style="height:72%"></b></div>
  </div>
</div>
<div class="nav-label">Choose a workspace</div>
""", unsafe_allow_html=True)

st.markdown('<div class="workspace-note"><b>Operational workspace</b><span>Screen, review and progress individual lending cases here. Use the separate dashboard for portfolio trends and management reporting.</span></div>', unsafe_allow_html=True)
nav = st.radio("Workspace navigation", [
    "Screen application",
    "Review account",
    "Collection log",
    "Application queue",
    "My portfolio",
], horizontal=True, label_visibility="collapsed")

status1, status2, status3 = st.columns([1, 1, 2])
status1.markdown(kcard("red", crit_accounts, "Critical accounts", "Require immediate attention"), unsafe_allow_html=True)
status2.markdown(kcard("blue", pending_apps, "Pending applications", "Currently under review"), unsafe_allow_html=True)
status3.markdown(kcard("green", f"{len(df):,}", "Portfolio records", "Live lending intelligence workspace"), unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE 1 - SCREEN A LOAN APPLICATION
# ════════════════════════════════════════════════════════════════
if nav == "Screen application":

    st.markdown('<div class="topbar"><h1><span style="color:#147bd1">Screen</span> a New Loan Application</h1><p>Enter the applicant details to receive an immediate risk assessment and lending recommendation.</p></div>', unsafe_allow_html=True)

    st.markdown("### Applicant information")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Personal Details**")
        applicant_name = st.text_input("Full Name")
        applicant_id   = st.text_input("National ID / Omang")
        age            = st.number_input("Age", 18, 75, 35)
        occupation     = st.selectbox("Employment Type", OCCUPATIONS)
        emp_tenure     = st.number_input("Years in Current Job", 0.0, 40.0, 3.0, 0.5)
        branch         = st.selectbox("Applying Branch", BRANCHES)

    with col2:
        st.markdown("**Financial Details**")
        monthly_income = st.number_input("Monthly Take-Home Income (BWP)", 1000, 200000, 12000, 500)
        existing_loans = st.number_input("Number of Other Active Loans", 0, 10, 0)
        prev_defaults  = st.number_input("Previous Loan Defaults (ever)", 0, 5, 0)
        credit_score   = st.number_input("Credit Score (if available)", 300, 850, 680)
        st.caption("Leave the credit score at 680 if it has not yet been obtained.")

    with col3:
        st.markdown("**Loan Request**")
        loan_type      = st.selectbox("Loan Type", LOAN_TYPES)
        loan_amount    = st.number_input("Amount Requested (BWP)", 1000, 1000000, 50000, 1000)
        loan_term      = st.selectbox("Repayment Period (months)", [12,24,36,48,60,72,84], index=2)
        interest_rate  = st.number_input("Interest Rate (%)", 8.5, 25.0, 14.0, 0.5)
        has_collateral = st.checkbox("Applicant Has Collateral?")
        collateral_val = st.number_input("Collateral Value (BWP)", 0, 5000000, 0, 5000) if has_collateral else 0

    st.markdown("---")

    r = interest_rate / 100 / 12
    monthly_payment = round(loan_amount * r / (1 - (1+r)**(-loan_term)), 0) if r > 0 else loan_amount / loan_term
    dti = round(monthly_payment / monthly_income, 4)
    months_active   = 0
    outstanding_bal = loan_amount

    st.markdown(f"**Calculated Monthly Payment: P{monthly_payment:,.0f}  |  Debt-to-Income Ratio: {dti*100:.1f}%**")
    if dti > 0.43:
        st.warning(f"Monthly payment is {dti*100:.0f}% of income. The policy limit is 43%.")

    st.markdown("---")

    application_ready = bool(applicant_name.strip() and applicant_id.strip())
    if not application_ready:
        st.caption("Required before assessment: applicant full name and National ID / Omang.")
    if st.button("Assess this application", disabled=not application_ready, use_container_width=True):

        credit_risk_cat  = 4 if credit_score<580 else 3 if credit_score<670 else 2 if credit_score<740 else 1 if credit_score<800 else 0
        dti_high         = 1 if dti > 0.43 else 0
        income_low       = 1 if monthly_income < 5000 else 0
        loan_large       = 1 if loan_amount > df["loan_amount_bwp"].quantile(0.75) else 0
        tenure_short     = 1 if emp_tenure < 2 else 0
        collateral_ratio = min((collateral_val / loan_amount) if loan_amount > 0 else 0, 5)
        payment_burden   = min(monthly_payment / monthly_income if monthly_income > 0 else 2, 2)
        loan_income_ratio= min(loan_amount / monthly_income if monthly_income > 0 else 100, 100)

        try:
            branch_enc = le_branch.transform([branch])[0]
            ltype_enc  = le_ltype.transform([loan_type])[0]
            occ_enc    = le_occ.transform([occupation])[0]
        except:
            branch_enc = ltype_enc = occ_enc = 0

        row = np.array([[
            age, monthly_income, loan_amount, interest_rate,
            loan_term, monthly_payment, months_active, outstanding_bal,
            dti, credit_score, existing_loans, emp_tenure,
            prev_defaults, int(has_collateral), collateral_val,
            branch_enc, ltype_enc, occ_enc,
            credit_risk_cat, dti_high, income_low, loan_large,
            tenure_short, collateral_ratio, payment_burden, loan_income_ratio,
        ]])

        prob = model.predict_proba(row)[0][1] * 100

        if prob < 20 and prev_defaults == 0 and dti < 0.43:
            decision = "APPROVE"
            css      = "result-approve"
            icon     = ""
        elif prob > 60 or prev_defaults >= 2 or dti > 0.65:
            decision = "DECLINE"
            css      = "result-decline"
            icon     = ""
        else:
            decision = "REFER TO CREDIT COMMITTEE"
            css      = "result-review"
            icon     = ""

        name_label = applicant_name if applicant_name else "Applicant"
        st.markdown(f"""
        <div class="{css}">
          <div style="font-size:2rem;font-weight:800;">{decision}</div>
          <div style="margin-top:.5rem;font-size:1.1rem;">
            {name_label} &nbsp;·&nbsp; P{loan_amount:,.0f} {loan_type} &nbsp;·&nbsp;
            Default risk score: <b style="background:rgba(255,255,255,0.2);padding:2px 6px;border-radius:4px">{prob:.0f} / 100</b>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Risk scorecard")
        sc1,sc2,sc3 = st.columns(3)

        def score_item(label, value, good, warning, bad_thresh, higher_is_better=True):
            if isinstance(value, str):
                # For percentage strings like "45.2%", extract the numeric part
                if '%' in value:
                    numeric_value = float(value.replace('%', ''))
                else:
                    # For non-numeric strings like "Yes"/"No", just return a neutral color
                    color = "#147bd1"  # Blue for non-numeric
                    return f'<div style="background:#f7f7f9;border-radius:16px;padding:1rem;margin:.3rem 0;border-left:5px solid {color};color:#0b0b14;"><b style="color:{color}">{label}</b><br><span style="font-size:1.1rem;font-weight:800;color:#0b0b14;">{value}</span></div>'
            else:
                numeric_value = value
            
            if higher_is_better:
                color = "#22c55e" if numeric_value >= good else "#f97316" if numeric_value >= warning else "#ef4444"
            else:
                color = "#22c55e" if numeric_value <= good else "#f97316" if numeric_value <= warning else "#ef4444"
            return f'<div style="background:#f7f7f9;border-radius:16px;padding:1rem;margin:.3rem 0;border-left:5px solid {color};color:#0b0b14;"><b style="color:{color}">{label}</b><br><span style="font-size:1.1rem;font-weight:800;color:#0b0b14;">{value}</span></div>'

        with sc1:
            st.markdown(score_item("Credit Score",        credit_score,      700,  620,  580,  True),  unsafe_allow_html=True)
            st.markdown(score_item("DTI Ratio",           f"{dti*100:.1f}%", 30,   43,   55,   False), unsafe_allow_html=True)
        with sc2:
            st.markdown(score_item("Employment (years)",  emp_tenure,        3,    1,    0.5,  True),  unsafe_allow_html=True)
            st.markdown(score_item("Existing Loans",      existing_loans,    1,    2,    3,    False), unsafe_allow_html=True)
        with sc3:
            st.markdown(score_item("Previous Defaults",   prev_defaults,     0,    1,    2,    False), unsafe_allow_html=True)
            st.markdown(score_item("Collateral",          "Yes" if has_collateral else "No", "Yes","Maybe","No", True), unsafe_allow_html=True)

        flags = []
        if dti > 0.43:          flags.append(f"Monthly payment ({dti*100:.0f}% of income) exceeds the 43% policy limit")
        if prev_defaults >= 1:  flags.append(f"Applicant has {prev_defaults} previous default(s) on record")
        if credit_score < 600:  flags.append(f"Credit score ({credit_score}) is below the acceptable threshold of 600")
        if existing_loans >= 3: flags.append(f"Applicant already has {existing_loans} active loans")
        if emp_tenure < 1:      flags.append(f"Less than 1 year in current job: employment stability concern")
        if monthly_income < 5000: flags.append(f"Income (P{monthly_income:,.0f}/month) is low relative to loan size")
        if not has_collateral and loan_amount > 100000: flags.append("No collateral offered for a loan above P100,000")

        if flags:
            st.markdown("### Risk factors")
            for f in flags:
                c_f = "#ef4444" if decision == "DECLINE" else "#f97316"
                st.markdown(f'<div class="flag-box" style="border-left:5px solid {c_f}">{f}</div>', unsafe_allow_html=True)

        st.markdown("### Officer recommendation")
        if decision == "APPROVE":
            st.markdown("""
            <div class="result-approve">
            <h4 style="margin-top:0">RECOMMENDED FOR APPROVAL</h4>
            <p>This applicant meets all lending criteria. Proceed with standard documentation.</p>
            <ul style="color:#0b0b14;">
              <li>Confirm payslips and bank statements for last 3 months</li>
              <li>Verify employment letter is current and signed</li>
              <li>Confirm no undisclosed loans at other institutions</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        elif decision == "REFER TO CREDIT COMMITTEE":
            st.markdown(f"""
            <div class="result-review">
            <h4 style="margin-top:0">REFER TO CREDIT COMMITTEE</h4>
            <p>This application has risk factors that require senior review. Do NOT approve at branch level.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-decline">
            <h4 style="margin-top:0">RECOMMENDED FOR DECLINE</h4>
            <p>This application does not meet Thebe Credit Union's lending criteria.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Save to application queue")
        st.markdown('<div class="composition"><b>Final decision</b><p>Keep the system recommendation or record an authorised override. Any override requires a reason and the original recommendation remains in the application record.</p></div>', unsafe_allow_html=True)
        decision_options = ["APPROVE", "REFER TO CREDIT COMMITTEE", "DECLINE"]
        recorded_decision = st.selectbox("Recorded decision", decision_options, index=decision_options.index(decision), key="recorded_decision")
        override_reason = st.text_input("Override reason", placeholder="Required when recorded decision differs from recommendation", key="loan_override_reason")
        officer_name = st.text_input("Your Name (Loan Officer)", key="officer_name")
        notes        = st.text_area("Additional Notes", key="app_notes", placeholder="Any other relevant information about this applicant...")
        save_ready = bool(officer_name.strip()) and (recorded_decision == decision or bool(override_reason.strip()))
        if not save_ready:
            st.caption("Enter the responsible officer and provide a reason for any override.")
        if st.button("Save application", key="save_app", disabled=not save_ready, use_container_width=True):
            st.session_state.applications.append({
                "app_id":        f"APP-{len(st.session_state.applications)+1:04d}",
                "date":          str(date.today()),
                "applicant":     applicant_name,
                "national_id":   applicant_id,
                "branch":        branch,
                "loan_type":     loan_type,
                "amount":        f"P{loan_amount:,.0f}",
                "decision":      recorded_decision,
                "system_recommendation": decision,
                "override_reason": override_reason or "No override",
                "risk_score":    f"{prob:.0f}/100",
                "officer":       officer_name,
                "notes":         notes,
                "status":        "Under Review" if recorded_decision == "REFER TO CREDIT COMMITTEE" else recorded_decision.title(),
                "updated_at":    datetime.now().strftime("%d %b %Y, %H:%M"),
            })
            st.success("Application saved. Open the application queue to track it.")

# ════════════════════════════════════════════════════════════════
# PAGE 2 - REVIEW EXISTING ACCOUNT
# ════════════════════════════════════════════════════════════════
elif nav == "Review account":

    st.markdown('<div class="topbar"><h1><span style="color:#147bd1">Review</span> an Existing Account</h1><p>Select a customer account to understand its current loan health and recommended action.</p></div>', unsafe_allow_html=True)

    customer_id = st.selectbox("Select Customer Account", sorted(df["customer_id"].unique()))
    row = df[df["customer_id"] == customer_id].iloc[0]

    c1,c2,c3,c4 = st.columns(4)
    status_color = "red" if row["payment_status"]=="Defaulted" else "orange" if "Late" in row["payment_status"] else "green"
    c1.markdown(kcard("blue",   row["loan_type"],                            "Loan Type",        row["branch"]), unsafe_allow_html=True)
    c2.markdown(kcard("blue",   f"P{row['outstanding_balance']:,.0f}",       "Outstanding",      f"of P{row['loan_amount_bwp']:,.0f} original"), unsafe_allow_html=True)
    c3.markdown(kcard(status_color, row["payment_status"],                   "Payment Status",   f"{row['days_late']} days late" if row["days_late"]>0 else "On time"), unsafe_allow_html=True)
    c4.markdown(kcard("red" if row["risk_level"] in ("Critical","High Risk") else "green",
                      row["risk_level"],                                     "Risk Level",       f"Score: {row['default_probability']*100:.0f}/100"), unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Customer profile")
        profile_items = [
            ("Age",              row["age"]),
            ("Occupation",       row["occupation"]),
            ("Monthly Income",   f"P{row['monthly_income_bwp']:,.0f}"),
            ("Credit Score",     row["credit_score"]),
            ("Employment (yrs)", row["employment_tenure_yrs"]),
            ("Existing Loans",   row["existing_loans"]),
            ("Previous Defaults",row["prev_defaults"]),
            ("Collateral",       "Yes" if row["has_collateral"] else "No"),
            ("Loan Officer",     row["loan_officer"]),
            ("Disbursed",        str(row["disburse_date"])[:10]),
        ]
        for label, val in profile_items:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;padding:.5rem 0;
                         border-bottom:1px solid #e8e8ed;color:#0b0b14;">
              <span style="color:#6f717b">{label}</span>
              <span style="font-weight:700;color:#0b0b14;">{val}</span>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("#### Risk gauge")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=row["default_probability"]*100,
            number={"suffix":"/100","font":{"size":32,"color":"#0b0b14"}},
            gauge={
                "axis":{"range":[0,100],"tickcolor":"#9a9ca5","tickfont":{"color":"#6f717b"}},
                "bar":{"color":"#ef4444" if row["default_probability"]>0.6 else "#f97316" if row["default_probability"]>0.4 else "#22c55e","thickness":.3},
                "steps":[
                    {"range":[0,20], "color":"#dff6bd"},{"range":[20,45],"color":"#fff0ba"},
                    {"range":[45,70],"color":"#ffd8b5"},{"range":[70,100],"color":"#ffc9c5"},
                ],
                "bgcolor":"#f7f7f9","bordercolor":"#e8e8ed",
            }
        ))
        fig.update_layout(height=240,paper_bgcolor="#ffffff",font_color="#0b0b14",font_family="Poppins",margin=dict(t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### Recommended action")

    if row["risk_level"] == "Critical":
        st.markdown(f"""
        <div style="background:#ffe8e6;border:0;border-radius:22px;padding:1.5rem;margin:.5rem 0;">
        <h4 style="color:#b42318;margin-top:0">CRITICAL: Escalate immediately</h4>
        <p style="color:#0b0b14;"><b>Step 1:</b> Call the customer today: do not send SMS only</p>
        <p style="color:#0b0b14;"><b>Step 2:</b> Offer a loan restructure or payment plan if they are genuinely struggling</p>
        <p style="color:#0b0b14;"><b>Expected loss if no action:</b> P{row['expected_loss_bwp']:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    elif row["risk_level"] == "High Risk":
        st.markdown(f"""
        <div style="background:#fff2df;border:0;border-radius:22px;padding:1.5rem;margin:.5rem 0;">
        <h4 style="color:#b54708;margin-top:0">HIGH RISK: Contact within 48 hours</h4>
        <p style="color:#0b0b14;"><b>Step 1:</b> Send a payment reminder SMS today</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Account is currently stable. Follow standard monitoring protocols.")

    st.markdown("---")
    st.markdown("### Log a collection action")
    lc1,lc2,lc3 = st.columns(3)
    with lc1: action_type = st.selectbox("Action Taken", ["Called Customer","SMS Sent","Email Sent","Letter Sent","Home Visit","Payment Plan Agreed","Legal Notice Issued","Restructure Approved"])
    with lc2: action_result = st.selectbox("Outcome", ["Promised to Pay","No Answer","Not Reachable","Dispute Raised","Payment Made","Agreed to Restructure","No Response"])
    with lc3: action_officer = st.text_input("Your Name", key="coll_officer")
    if st.button("Save collection action", key="save_coll"):
        st.session_state.collection_log.append({
            "customer_id": customer_id, "date": str(date.today()), "action": action_type,
            "outcome": action_result, "officer": action_officer,
        })
        st.success("Collection action logged.")

# ════════════════════════════════════════════════════════════════
# PAGE 3 - LOG COLLECTION ACTION
# ════════════════════════════════════════════════════════════════
elif nav == "Collection log":

    st.markdown('<div class="topbar"><h1><span style="color:#147bd1">Collection</span> Action Log</h1><p>Record contact attempts and outcomes for late and defaulted accounts.</p></div>', unsafe_allow_html=True)

    needs_contact = df[df["payment_status"].isin(["Defaulted","Late (30–89 days)"])].copy()
    needs_contact = needs_contact.sort_values("expected_loss_bwp", ascending=False)

    c1,c2,c3 = st.columns(3)
    c1.markdown(kcard("red",    f"{len(needs_contact):,}","Accounts Needing Contact","Late or defaulted"), unsafe_allow_html=True)
    c2.markdown(kcard("orange", f"{(needs_contact['collection_action']=='None').sum():,}","No Action Taken Yet","Priority for outreach"), unsafe_allow_html=True)
    c3.markdown(kcard("blue",   f"P{needs_contact['expected_loss_bwp'].sum()/1e3:.0f}K","At Stake","If not recovered"), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Priority contact list")
    f1, f2, f3 = st.columns([1.4, 1, 1])
    with f1:
        contact_search = st.text_input("Find an account", placeholder="Customer ID", key="collection_search")
    with f2:
        contact_branch = st.multiselect("Branch", sorted(needs_contact["branch"].dropna().unique()), key="collection_branch")
    with f3:
        contact_status = st.multiselect("Payment status", sorted(needs_contact["payment_status"].dropna().unique()), key="collection_status")
    if contact_search:
        needs_contact = needs_contact[needs_contact["customer_id"].astype(str).str.contains(contact_search, case=False, na=False)]
    if contact_branch:
        needs_contact = needs_contact[needs_contact["branch"].isin(contact_branch)]
    if contact_status:
        needs_contact = needs_contact[needs_contact["payment_status"].isin(contact_status)]
    st.markdown(f'<div class="data-hint">Showing {min(len(needs_contact), 50)} of {len(needs_contact)} matching priority accounts, ordered by expected loss.</div>', unsafe_allow_html=True)
    show = needs_contact[["customer_id","loan_type","branch","loan_officer","outstanding_balance","days_late","payment_status","expected_loss_bwp","collection_action"]].head(50).copy()
    show["outstanding_balance"] = show["outstanding_balance"].apply(lambda x:f"P{x:,.0f}")
    show["expected_loss_bwp"]   = show["expected_loss_bwp"].apply(lambda x:f"P{x:,.0f}")
    show.columns = ["Customer","Loan Type","Branch","Officer","Outstanding","Days Late","Status","At Risk","Last Action"]
    st.dataframe(show.reset_index(drop=True), use_container_width=True)

# ════════════════════════════════════════════════════════════════
# PAGE 4 - APPLICATION QUEUE
# ════════════════════════════════════════════════════════════════
elif nav == "Application queue":

    st.markdown('<div class="topbar"><h1><span style="color:#147bd1">Loan</span> Application Queue</h1><p>Review every screened application and follow its progress.</p></div>', unsafe_allow_html=True)

    apps = st.session_state.applications
    if not apps:
        st.info("No applications screened yet.")
    else:
        st.markdown("### All Applications")
        q1, q2 = st.columns([1.4, 1])
        with q1:
            app_search = st.text_input("Find an application", placeholder="Application ID or applicant", key="application_search")
        with q2:
            app_status = st.multiselect("Decision status", sorted({a["status"] for a in apps}), key="application_status")
        visible_apps = apps
        if app_search:
            term = app_search.lower()
            visible_apps = [a for a in visible_apps if term in str(a.get("app_id", "")).lower() or term in str(a.get("applicant", "")).lower()]
        if app_status:
            visible_apps = [a for a in visible_apps if a["status"] in app_status]
        st.markdown(f'<div class="data-hint">Showing {len(visible_apps)} of {len(apps)} screened applications.</div>', unsafe_allow_html=True)
        if not visible_apps:
            st.info("No applications match the current filters.")
        for i, app in enumerate(visible_apps):
            status_c = "#22c55e" if "APPROVE" in app["status"] else "#ef4444" if "DECLINE" in app["status"] else "#f97316"
            st.markdown(f"""
            <div style="background:#f7f7f9;border-radius:18px;padding:1.1rem;margin:.5rem 0;border-left:5px solid {status_c};color:#0b0b14;">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <div><b>{app['app_id']}</b> &nbsp;·&nbsp; {app.get('applicant','Unknown')} &nbsp;·&nbsp; {app['loan_type']}</div>
                <div style="color:{status_c};font-weight:700">{app['status']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            detail_col, status_col = st.columns([2, 1])
            with detail_col:
                with st.expander(f"View {app['app_id']} details"):
                    st.markdown(f"**Applicant:** {app.get('applicant') or 'Not provided'}  \n**National ID:** {app.get('national_id') or 'Not provided'}  \n**Branch:** {app.get('branch')}  \n**Requested:** {app.get('amount')} · {app.get('loan_type')}  \n**System recommendation:** {app.get('system_recommendation', app.get('decision'))}  \n**Recorded decision:** {app.get('decision')}  \n**Override reason:** {app.get('override_reason', 'No override')}  \n**Officer:** {app.get('officer')}  \n**Updated:** {app.get('updated_at', app.get('date'))}")
            with status_col:
                workflow_states = ["Under Review", "Approved", "Declined", "Documents Pending", "Completed"]
                current_status = app["status"] if app["status"] in workflow_states else "Under Review"
                new_app_status = st.selectbox("Workflow status", workflow_states, index=workflow_states.index(current_status), key=f"app_status_{i}")
                if new_app_status != app["status"]:
                    app["status"] = new_app_status
                    app["updated_at"] = datetime.now().strftime("%d %b %Y, %H:%M")
                    st.success(f"{app['app_id']} moved to {new_app_status}.")

# ════════════════════════════════════════════════════════════════
# PAGE 5 - MY PORTFOLIO
# ════════════════════════════════════════════════════════════════
elif nav == "My portfolio":

    st.markdown('<div class="topbar"><h1><span style="color:#147bd1">My</span> Loan Portfolio</h1><p>Understand the health of every loan assigned to you.</p></div>', unsafe_allow_html=True)

    officer = st.selectbox("Select Your Officer ID", sorted(df["loan_officer"].unique()))
    my_loans = df[df["loan_officer"] == officer].copy()

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kcard("blue",   f"{len(my_loans)}",                                "My Total Accounts",    ""), unsafe_allow_html=True)
    c2.markdown(kcard("red",    f"P{my_loans['expected_loss_bwp'].sum():,.0f}",     "My At-Risk Amount",    "Across all my accounts"), unsafe_allow_html=True)
    c3.markdown(kcard("orange", f"{my_loans['will_default'].sum()}",               "Defaulted / Late",     f"{my_loans['will_default'].mean()*100:.1f}% of my portfolio"), unsafe_allow_html=True)
    c4.markdown(kcard("blue",   f"{my_loans['credit_score'].mean():.0f}",          "Avg Credit Score",     "My portfolio average"), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### All my accounts")
    p1, p2 = st.columns([1.4, 1])
    with p1:
        account_search = st.text_input("Find an account", placeholder="Customer ID", key="portfolio_search")
    with p2:
        risk_filter = st.multiselect("Risk level", sorted(my_loans["risk_level"].dropna().unique()), key="portfolio_risk")
    if account_search:
        my_loans = my_loans[my_loans["customer_id"].astype(str).str.contains(account_search, case=False, na=False)]
    if risk_filter:
        my_loans = my_loans[my_loans["risk_level"].isin(risk_filter)]
    st.markdown(f'<div class="data-hint">Showing {len(my_loans)} accounts assigned to {officer}.</div>', unsafe_allow_html=True)
    my_show = my_loans[["customer_id","loan_type","loan_amount_bwp","outstanding_balance","payment_status","risk_level","days_late","credit_score"]].copy()
    my_show["loan_amount_bwp"]   = my_show["loan_amount_bwp"].apply(lambda x:f"P{x:,.0f}")
    my_show["outstanding_balance"]= my_show["outstanding_balance"].apply(lambda x:f"P{x:,.0f}")
    my_show.columns = ["Customer","Loan Type","Loan Amount","Outstanding","Status","Risk","Days Late","Credit Score"]
    st.dataframe(my_show.reset_index(drop=True), use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align:center;color:#64748b;font-size:.78rem'>Thebe Credit Union · Loan Management System · Unaswi Leonard · 2026</div>", unsafe_allow_html=True)
