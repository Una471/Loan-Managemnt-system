"""
THEBE CREDIT UNION — LOAN MANAGEMENT SYSTEM
The software that solves the problem.
Loan officers use this to: screen applications, review existing accounts,
log collection actions, and track the credit review pipeline.
Run: streamlit run 04_software.py --server.port 8502
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib, json
from datetime import datetime, date, timedelta

st.set_page_config(page_title="Thebe Credit Union | Loan System", page_icon="🏦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#0f172a;color:#f1f5f9;}
.topbar{background:linear-gradient(135deg,#0a2a44,#1a3a5f);padding:1.2rem 1.5rem;
         border-radius:12px;margin-bottom:1.2rem;border:1px solid #2d4b6e;box-shadow:0 4px 6px rgba(0,0,0,0.3);}
.topbar h1{margin:0;font-size:1.4rem;color:white;}
.topbar p{margin:.2rem 0 0;opacity:.9;font-size:.82rem;color:#e2e8f0;}
.kcard{background:#1e293b;border-radius:10px;padding:1.1rem 1.3rem;border:1px solid #334155;margin-bottom:.3rem;color:#f1f5f9;}
.kcard.red   {border-top:3px solid #ef4444;} .kcard.orange{border-top:3px solid #f97316;}
.kcard.green {border-top:3px solid #22c55e;} .kcard.blue  {border-top:3px solid #3b82f6;}
.kval{font-size:1.8rem;font-weight:700;color:white;} 
.klbl{font-size:.7rem;text-transform:uppercase;letter-spacing:1.5px;color:#60a5fa;margin-top:.3rem;font-weight:600;} 
.ksub{font-size:.76rem;color:#cbd5e1;margin-top:.3rem;}
/* Enhanced result banner contrast - much brighter text */
.result-approve{background:#052e16;border:2px solid #22c55e;border-radius:12px;padding:1.8rem;margin:1rem 0;}
.result-review {background:#422006;border:2px solid #f97316;border-radius:12px;padding:1.8rem;margin:1rem 0;}
.result-decline{background:#450a0a;border:2px solid #ef4444;border-radius:12px;padding:1.8rem;margin:1rem 0;}
.result-approve, .result-approve * {color:white !important;}
.result-review, .result-review * {color:white !important;}
.result-decline, .result-decline * {color:white !important;}
.result-approve h4, .result-review h4, .result-decline h4 {color:white !important; font-weight:700;}
.flag-box{background:#1e293b;border-left:4px solid #f97316;border-radius:8px;padding:.85rem;margin:.4rem 0;color:#f1f5f9;}
.action-card{background:#1e293b;border-radius:10px;padding:1rem 1.2rem;border:1px solid #2d3748;margin:.5rem 0;color:#f1f5f9;}
.action-card.done{border-left:4px solid #22c55e;opacity:.7;}
.action-card.pending{border-left:4px solid #ef4444;}
section[data-testid="stSidebar"]{background:#0a2a44!important;border-right:1px solid #1e3a5f;}
section[data-testid="stSidebar"] *{color:#f1f5f9!important;}
section[data-testid="stSidebar"] .stSelectbox label{color:#e2e8f0!important;}
.stTextInput input,.stNumberInput input,.stSelectbox select{background:#1e293b!important;color:white!important;border:1px solid #334155!important;}
.stTextInput label,.stNumberInput label,.stSelectbox label{color:#030203!important;}
.stButton>button{background:#3b82f6;color:white;border:none;border-radius:8px;padding:.6rem 1.5rem;font-weight:600;width:100%;}
.stButton>button:hover{background:#2563eb;}
.st-bb{background-color:transparent;}
.st-cb{color:#f1f5f9;}
div[data-testid="stDataFrame"]{color:#f1f5f9;}
.stDataFrame {color:#f1f5f9;}
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── LOAD ──────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    m  = joblib.load("model.pkl")
    lb = joblib.load("le_branch.pkl")
    ll = joblib.load("le_ltype.pkl")
    lo = joblib.load("le_occ.pkl")
    with open("features.json") as f: feat = json.load(f)
    return m, lb, ll, lo, feat

@st.cache_data
def load_data():
    return pd.read_csv("loan_data_scored.csv", parse_dates=["disburse_date"])

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
    fig.update_layout(plot_bgcolor="#0f172a",paper_bgcolor="#0f172a",font_color="white",
                      height=h,margin=dict(t=15,b=10,l=5,r=5), template="plotly_dark")
    return fig

# ── SIDEBAR ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏦 Loan Management System")
    st.markdown("*Thebe Credit Union*")
    st.markdown("---")
    nav = st.radio("Go to", [
        "📝  Screen a Loan Application",
        "🔍  Review Existing Account",
        "📞  Log Collection Action",
        "📋  Application Queue",
        "📊  My Portfolio (Officer View)",
    ])
    st.markdown("---")
    pending_apps = len([a for a in st.session_state.applications if a["decision"] == "Under Review"])
    crit_accounts = (df["risk_level"] == "Critical").sum()
    st.markdown(f"🔴 **Critical accounts:** {crit_accounts}")
    st.markdown(f"📋 **Pending applications:** {pending_apps}")

# ════════════════════════════════════════════════════════════════
# PAGE 1 — SCREEN A LOAN APPLICATION
# ════════════════════════════════════════════════════════════════
if nav == "📝  Screen a Loan Application":

    st.markdown('<div class="topbar"><h1>📝 New Loan Application Screener</h1><p>Fill in the applicant\'s details to get an instant risk assessment and lending recommendation</p></div>', unsafe_allow_html=True)

    st.markdown("### 👤 Applicant Information")
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
        st.caption("💡 Leave credit score at 680 if not yet obtained")

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
        st.warning(f"⚠️ Monthly payment is {dti*100:.0f}% of income. Policy limit is 43%. This is a concern.")

    st.markdown("---")

    if st.button("🔍  ASSESS THIS APPLICATION NOW"):

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
            icon     = "✅"
        elif prob > 60 or prev_defaults >= 2 or dti > 0.65:
            decision = "DECLINE"
            css      = "result-decline"
            icon     = "❌"
        else:
            decision = "REFER TO CREDIT COMMITTEE"
            css      = "result-review"
            icon     = "⚠️"

        name_label = applicant_name if applicant_name else "Applicant"
        st.markdown(f"""
        <div class="{css}">
          <div style="font-size:2.5rem;margin-bottom:.5rem">{icon}</div>
          <div style="font-size:2rem;font-weight:800;">{decision}</div>
          <div style="margin-top:.5rem;font-size:1.1rem;">
            {name_label} &nbsp;·&nbsp; P{loan_amount:,.0f} {loan_type} &nbsp;·&nbsp;
            Default risk score: <b style="background:rgba(255,255,255,0.2);padding:2px 6px;border-radius:4px">{prob:.0f} / 100</b>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📊 Risk Scorecard")
        sc1,sc2,sc3 = st.columns(3)

        def score_item(label, value, good, warning, bad_thresh, higher_is_better=True):
            if isinstance(value, str):
                # For percentage strings like "45.2%", extract the numeric part
                if '%' in value:
                    numeric_value = float(value.replace('%', ''))
                else:
                    # For non-numeric strings like "Yes"/"No", just return a neutral color
                    color = "#3b82f6"  # Blue for non-numeric
                    return f'<div style="background:#1e293b;border-radius:8px;padding:.8rem;margin:.3rem 0;border-left:4px solid {color};color:white;"><b style="color:{color}">{label}</b><br><span style="font-size:1.1rem;font-weight:700;color:white;">{value}</span></div>'
            else:
                numeric_value = value
            
            if higher_is_better:
                color = "#22c55e" if numeric_value >= good else "#f97316" if numeric_value >= warning else "#ef4444"
            else:
                color = "#22c55e" if numeric_value <= good else "#f97316" if numeric_value <= warning else "#ef4444"
            return f'<div style="background:#1e293b;border-radius:8px;padding:.8rem;margin:.3rem 0;border-left:4px solid {color};color:white;"><b style="color:{color}">{label}</b><br><span style="font-size:1.1rem;font-weight:700;color:white;">{value}</span></div>'

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
        if emp_tenure < 1:      flags.append(f"Less than 1 year in current job — employment stability concern")
        if monthly_income < 5000: flags.append(f"Income (P{monthly_income:,.0f}/month) is low relative to loan size")
        if not has_collateral and loan_amount > 100000: flags.append("No collateral offered for a loan above P100,000")

        if flags:
            st.markdown("### 🚩 Red Flags Found")
            for f in flags:
                c_f = "#ef4444" if decision == "DECLINE" else "#f97316"
                st.markdown(f'<div class="flag-box"><span style="color:{c_f}">⚠️</span> {f}</div>', unsafe_allow_html=True)

        st.markdown("### 📋 Officer Recommendations")
        if decision == "APPROVE":
            st.markdown("""
            <div class="result-approve">
            <h4 style="margin-top:0">✅ RECOMMENDED FOR APPROVAL</h4>
            <p>This applicant meets all lending criteria. Proceed with standard documentation.</p>
            <ul style="color:white;">
              <li>Confirm payslips and bank statements for last 3 months</li>
              <li>Verify employment letter is current and signed</li>
              <li>Confirm no undisclosed loans at other institutions</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        elif decision == "REFER TO CREDIT COMMITTEE":
            st.markdown(f"""
            <div class="result-review">
            <h4 style="margin-top:0">⚠️ REFER TO CREDIT COMMITTEE</h4>
            <p>This application has risk factors that require senior review. Do NOT approve at branch level.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-decline">
            <h4 style="margin-top:0">❌ RECOMMENDED FOR DECLINE</h4>
            <p>This application does not meet Thebe Credit Union's lending criteria.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 💾 Save to Application Queue")
        officer_name = st.text_input("Your Name (Loan Officer)", key="officer_name")
        notes        = st.text_area("Additional Notes", key="app_notes", placeholder="Any other relevant information about this applicant...")
        if st.button("💾  Save This Application", key="save_app"):
            st.session_state.applications.append({
                "app_id":        f"APP-{len(st.session_state.applications)+1:04d}",
                "date":          str(date.today()),
                "applicant":     applicant_name,
                "national_id":   applicant_id,
                "branch":        branch,
                "loan_type":     loan_type,
                "amount":        f"P{loan_amount:,.0f}",
                "decision":      decision,
                "risk_score":    f"{prob:.0f}/100",
                "officer":       officer_name,
                "notes":         notes,
                "status":        "Under Review" if decision == "REFER TO CREDIT COMMITTEE" else decision,
            })
            st.success(f"✅ Application saved! Go to **Application Queue** to track it.")

# ════════════════════════════════════════════════════════════════
# PAGE 2 — REVIEW EXISTING ACCOUNT
# ════════════════════════════════════════════════════════════════
elif nav == "🔍  Review Existing Account":

    st.markdown('<div class="topbar"><h1>🔍 Existing Account Review</h1><p>Look up any customer account to see their loan health and recommended action</p></div>', unsafe_allow_html=True)

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
        st.markdown("#### 👤 Customer Profile")
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
                         border-bottom:1px solid #334155;color:white;">
              <span style="color:#cbd5e1">{label}</span>
              <span style="font-weight:600;color:white;">{val}</span>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("#### ⚡ Risk Gauge")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=row["default_probability"]*100,
            number={"suffix":"/100","font":{"size":32,"color":"white"}},
            gauge={
                "axis":{"range":[0,100],"tickcolor":"white","tickfont":{"color":"white"}},
                "bar":{"color":"#ef4444" if row["default_probability"]>0.6 else "#f97316" if row["default_probability"]>0.4 else "#22c55e","thickness":.3},
                "steps":[
                    {"range":[0,20], "color":"#166534"},{"range":[20,45],"color":"#b45309"},
                    {"range":[45,70],"color":"#c2410c"},{"range":[70,100],"color":"#b91c1c"},
                ],
                "bgcolor":"#1e293b","bordercolor":"#334155",
            }
        ))
        fig.update_layout(height=240,paper_bgcolor="#0f172a",font_color="white",margin=dict(t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📋 Recommended Action for This Account")

    if row["risk_level"] == "Critical":
        st.markdown(f"""
        <div style="background:#450a0a;border:2px solid #ef4444;border-radius:10px;padding:1.4rem;margin:.5rem 0;">
        <h4 style="color:#fecaca;margin-top:0">🔴 CRITICAL — Escalate Immediately</h4>
        <p style="color:white;"><b>Step 1:</b> Call the customer today — do not send SMS only</p>
        <p style="color:white;"><b>Step 2:</b> Offer a loan restructure or payment plan if they are genuinely struggling</p>
        <p style="color:white;"><b>Expected loss if no action:</b> P{row['expected_loss_bwp']:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    elif row["risk_level"] == "High Risk":
        st.markdown(f"""
        <div style="background:#422006;border:2px solid #f97316;border-radius:10px;padding:1.4rem;margin:.5rem 0;">
        <h4 style="color:#fed7aa;margin-top:0">🟠 HIGH RISK — Contact Within 48 Hours</h4>
        <p style="color:white;"><b>Step 1:</b> Send a payment reminder SMS today</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Account is currently stable. Follow standard monitoring protocols.")

    st.markdown("---")
    st.markdown("### 📞 Log a Collection Action")
    lc1,lc2,lc3 = st.columns(3)
    with lc1: action_type = st.selectbox("Action Taken", ["Called Customer","SMS Sent","Email Sent","Letter Sent","Home Visit","Payment Plan Agreed","Legal Notice Issued","Restructure Approved"])
    with lc2: action_result = st.selectbox("Outcome", ["Promised to Pay","No Answer","Not Reachable","Dispute Raised","Payment Made","Agreed to Restructure","No Response"])
    with lc3: action_officer = st.text_input("Your Name", key="coll_officer")
    if st.button("💾  Save Collection Action", key="save_coll"):
        st.session_state.collection_log.append({
            "customer_id": customer_id, "date": str(date.today()), "action": action_type,
            "outcome": action_result, "officer": action_officer,
        })
        st.success("✅ Collection action logged!")

# ════════════════════════════════════════════════════════════════
# PAGE 3 — LOG COLLECTION ACTION
# ════════════════════════════════════════════════════════════════
elif nav == "📞  Log Collection Action":

    st.markdown('<div class="topbar"><h1>📞 Collection Action Log</h1><p>Record all contact attempts and outcomes for late and defaulted accounts</p></div>', unsafe_allow_html=True)

    needs_contact = df[df["payment_status"].isin(["Defaulted","Late (30–89 days)"])].copy()
    needs_contact = needs_contact.sort_values("expected_loss_bwp", ascending=False)

    c1,c2,c3 = st.columns(3)
    c1.markdown(kcard("red",    f"{len(needs_contact):,}","Accounts Needing Contact","Late or defaulted"), unsafe_allow_html=True)
    c2.markdown(kcard("orange", f"{(needs_contact['collection_action']=='None').sum():,}","No Action Taken Yet","Priority for outreach"), unsafe_allow_html=True)
    c3.markdown(kcard("blue",   f"P{needs_contact['expected_loss_bwp'].sum()/1e3:.0f}K","At Stake","If not recovered"), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 Priority Contact List")
    show = needs_contact[["customer_id","loan_type","branch","loan_officer","outstanding_balance","days_late","payment_status","expected_loss_bwp","collection_action"]].head(50).copy()
    show["outstanding_balance"] = show["outstanding_balance"].apply(lambda x:f"P{x:,.0f}")
    show["expected_loss_bwp"]   = show["expected_loss_bwp"].apply(lambda x:f"P{x:,.0f}")
    show.columns = ["Customer","Loan Type","Branch","Officer","Outstanding","Days Late","Status","At Risk","Last Action"]
    st.dataframe(show.reset_index(drop=True), use_container_width=True)

# ════════════════════════════════════════════════════════════════
# PAGE 4 — APPLICATION QUEUE
# ════════════════════════════════════════════════════════════════
elif nav == "📋  Application Queue":

    st.markdown('<div class="topbar"><h1>📋 Loan Application Queue</h1><p>All applications screened through this system — track their progress</p></div>', unsafe_allow_html=True)

    apps = st.session_state.applications
    if not apps:
        st.info("No applications screened yet.")
    else:
        st.markdown("### All Applications")
        for i, app in enumerate(apps):
            status_c = "#22c55e" if "APPROVE" in app["status"] else "#ef4444" if "DECLINE" in app["status"] else "#f97316"
            st.markdown(f"""
            <div style="background:#1e293b;border-radius:10px;padding:1rem;margin:.4rem 0;border-left:4px solid {status_c};color:white;">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <div><b>{app['app_id']}</b> &nbsp;·&nbsp; {app.get('applicant','Unknown')} &nbsp;·&nbsp; {app['loan_type']}</div>
                <div style="color:{status_c};font-weight:700">{app['status']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE 5 — MY PORTFOLIO
# ════════════════════════════════════════════════════════════════
elif nav == "📊  My Portfolio (Officer View)":

    st.markdown('<div class="topbar"><h1>📊 My Loan Portfolio</h1><p>See the health of all loans assigned to you as a loan officer</p></div>', unsafe_allow_html=True)

    officer = st.selectbox("Select Your Officer ID", sorted(df["loan_officer"].unique()))
    my_loans = df[df["loan_officer"] == officer].copy()

    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kcard("blue",   f"{len(my_loans)}",                                "My Total Accounts",    ""), unsafe_allow_html=True)
    c2.markdown(kcard("red",    f"P{my_loans['expected_loss_bwp'].sum():,.0f}",     "My At-Risk Amount",    "Across all my accounts"), unsafe_allow_html=True)
    c3.markdown(kcard("orange", f"{my_loans['will_default'].sum()}",               "Defaulted / Late",     f"{my_loans['will_default'].mean()*100:.1f}% of my portfolio"), unsafe_allow_html=True)
    c4.markdown(kcard("blue",   f"{my_loans['credit_score'].mean():.0f}",          "Avg Credit Score",     "My portfolio average"), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 All My Accounts")
    my_show = my_loans[["customer_id","loan_type","loan_amount_bwp","outstanding_balance","payment_status","risk_level","days_late","credit_score"]].copy()
    my_show["loan_amount_bwp"]   = my_show["loan_amount_bwp"].apply(lambda x:f"P{x:,.0f}")
    my_show["outstanding_balance"]= my_show["outstanding_balance"].apply(lambda x:f"P{x:,.0f}")
    my_show.columns = ["Customer","Loan Type","Loan Amount","Outstanding","Status","Risk","Days Late","Credit Score"]
    st.dataframe(my_show.reset_index(drop=True), use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align:center;color:#64748b;font-size:.78rem'>Thebe Credit Union · Loan Management System · Unaswi Leonard · 2026</div>", unsafe_allow_html=True)
