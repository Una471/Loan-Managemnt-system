"""
THEBE CREDIT UNION — LOAN PORTFOLIO DASHBOARD
Simple report for branch managers and executives.
Run: streamlit run 03_dashboard.py --server.port 8501
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Thebe Credit Union | Dashboard", page_icon="🏦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#f8fafc;color:#0f172a;}
.topbar{background:linear-gradient(135deg,#0a2a44,#1e4a6f);color:white;padding:1.4rem 2rem;border-radius:12px;margin-bottom:1.5rem;box-shadow:0 4px 6px rgba(0,0,0,0.1);}
.topbar h1{margin:0;font-size:1.5rem;font-weight:700;color:white;}
.topbar p{margin:.3rem 0 0;opacity:.9;font-size:.85rem;color:#e2e8f0;}
.kcard{background:white;border-radius:12px;padding:1.2rem 1.4rem;box-shadow:0 2px 8px rgba(0,0,0,.07);border-left:5px solid #e0e0e0;margin-bottom:.3rem;color:#0f172a;}
.kcard.red{border-left-color:#b91c1c;} .kcard.orange{border-left-color:#c2410c;}
.kcard.green{border-left-color:#166534;} .kcard.blue{border-left-color:#1e4a6f;}
.kval{font-size:1.9rem;font-weight:700;line-height:1.1;color:#0f172a;}
.klbl{font-size:.72rem;text-transform:uppercase;letter-spacing:1.5px;color:#1e4a6f;margin-top:.3rem;font-weight:700;}
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
section[data-testid="stSidebar"]{background:#0a2a44!important;}
section[data-testid="stSidebar"] *{color:white!important;}
section[data-testid="stSidebar"] .stSelectbox label{color:#e2e8f0!important;}
.st-bb{background-color:transparent;}
#MainMenu,footer,header{visibility:hidden;}
div[data-testid="stDataFrame"]{color:#0f172a;}
.stDataFrame {color:#0f172a;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load():
    return pd.read_csv("loan_data_scored.csv", parse_dates=["disburse_date"])

df = load()

with st.sidebar:
    st.markdown("### 🏦 Thebe Credit Union")
    st.markdown("Loan Portfolio Dashboard")
    st.markdown("---")
    page = st.radio("Go to", [
        "📋  Portfolio Overview",
        "⚠️  At-Risk Accounts",
        "💸  Losses & Collections",
        "🏢  Branch Performance",
        "👤  Customer Insights",
    ])
    st.markdown("---")
    branches = ["All Branches"] + sorted(df["branch"].unique().tolist())
    sel_b    = st.selectbox("Filter: Branch", branches)
    ltypes   = ["All Loan Types"] + sorted(df["loan_type"].unique().tolist())
    sel_l    = st.selectbox("Filter: Loan Type", ltypes)
    st.markdown("---")
    st.caption("Period: Jan 2024 – Jun 2025")

dff = df.copy()
if sel_b != "All Branches":   dff = dff[dff["branch"]    == sel_b]
if sel_l != "All Loan Types": dff = dff[dff["loan_type"] == sel_l]

def kcard(color, val, lbl, sub=""):
    return f'<div class="kcard {color}"><div class="kval">{val}</div><div class="klbl">{lbl}</div>{"<div class=ksub>"+sub+"</div>" if sub else ""}</div>'

def wchart(fig, h=340):
    fig.update_layout(plot_bgcolor="white",paper_bgcolor="white",font_color="#0f172a",
                      height=h,margin=dict(t=15,b=20,l=10,r=10), template="plotly_white")
    return fig

# ════════════════════════════════════════════════════════════════
# PAGE 1 — PORTFOLIO OVERVIEW
# ════════════════════════════════════════════════════════════════
if page == "📋  Portfolio Overview":
    st.markdown('<div class="topbar"><h1>🏦 Loan Portfolio Overview</h1><p>Thebe Credit Union &nbsp;·&nbsp; January 2024 – June 2025</p></div>', unsafe_allow_html=True)

    total_port  = dff["loan_amount_bwp"].sum()
    outstanding = dff["outstanding_balance"].sum()
    total_loss  = dff["expected_loss_bwp"].sum()
    defaulted   = (dff["payment_status"]=="Defaulted").sum()
    late        = (dff["payment_status"]=="Late (30–89 days)").sum()
    current     = (dff["payment_status"]=="Current").sum()

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.markdown(kcard("blue",  f"P{total_port/1e6:.1f}M",    "Total Portfolio",        f"{len(dff):,} loans"), unsafe_allow_html=True)
    c2.markdown(kcard("blue",  f"P{outstanding/1e6:.1f}M",   "Outstanding Balance",    "Still owed by customers"), unsafe_allow_html=True)
    c3.markdown(kcard("red",   f"P{total_loss/1e6:.2f}M",    "Estimated Financial Loss","At risk of not being recovered"), unsafe_allow_html=True)
    c4.markdown(kcard("red",   f"{defaulted:,}",              "Defaulted Accounts",     "Stopped paying"), unsafe_allow_html=True)
    c5.markdown(kcard("green", f"{current:,}",                "Paying on Time",         f"Out of {len(dff):,} total"), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔍 What This Report Found")
    f1,f2,f3 = st.columns(3)
    with f1: st.markdown(f'<div class="ar"><b>🔴 TOO MANY ACCOUNTS ARE FALLING BEHIND</b><br><br><b>{defaulted+late:,} customers</b> ({(defaulted+late)/len(dff)*100:.0f}% of all loans) are either fully defaulted or behind on payments. This is putting <b>P{total_loss/1e6:.1f}M</b> of the credit union\'s money at risk.</div>', unsafe_allow_html=True)
    with f2: st.markdown('<div class="ao"><b>🟠 SOME LOAN TYPES ARE MUCH RISKIER THAN OTHERS</b><br><br>Not all loan types perform the same way. Some categories have far higher default rates than others. Tightening the requirements for the riskiest loan types could significantly reduce losses.</div>', unsafe_allow_html=True)
    with f3: st.markdown('<div class="ao"><b>🟠 BRANCH PERFORMANCE VARIES SIGNIFICANTLY</b><br><br>Some branches have much higher default rates than others. This may reflect differences in how loan applications are being reviewed and approved, or differences in the local customer base.</div>', unsafe_allow_html=True)

    st.markdown("---")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="ccard"><div class="ctitle">Loan Account Status — All Customers</div><div class="csub">Breakdown of how customers are currently managing their repayments</div>', unsafe_allow_html=True)
        status_c = dff["payment_status"].value_counts().reset_index()
        status_c.columns = ["Status","Count"]
        fig = px.pie(status_c, values="Count", names="Status", hole=0.45,
                     color="Status",
                     color_discrete_map={"Current":"#166534","Early (1–29 days)":"#b45309",
                                         "Late (30–89 days)":"#c2410c","Defaulted":"#b91c1c"})
        fig.update_traces(textinfo="percent+label", textfont_color="#0f172a")
        st.plotly_chart(wchart(fig, 360), use_container_width=True)
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

# ════════════════════════════════════════════════════════════════
# PAGE 2 — AT-RISK ACCOUNTS
# ════════════════════════════════════════════════════════════════
elif page == "⚠️  At-Risk Accounts":
    st.markdown('<div class="topbar"><h1>⚠️ High-Risk Loan Accounts</h1><p>Accounts most likely to default — prioritise these for immediate contact</p></div>', unsafe_allow_html=True)

    rc = dff["risk_level"].value_counts()
    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(kcard("red",    f"{rc.get('Critical',0):,}",    "Critical Risk",    "Needs urgent action now"), unsafe_allow_html=True)
    c2.markdown(kcard("orange", f"{rc.get('High Risk',0):,}",   "High Risk",        "Contact this week"), unsafe_allow_html=True)
    c3.markdown(kcard("blue",   f"{rc.get('Medium Risk',0):,}", "Medium Risk",      "Monitor closely"), unsafe_allow_html=True)
    c4.markdown(kcard("green",  f"{rc.get('Low Risk',0):,}",    "Low Risk",         "Paying well"), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📏 What Do the Risk Levels Mean?")
    e1,e2,e3,e4 = st.columns(4)
    with e1: st.markdown('<div class="ar"><b>🔴 CRITICAL</b><br>Very high chance of defaulting. Call this customer immediately. Consider restructuring the loan or demanding collateral.</div>', unsafe_allow_html=True)
    with e2: st.markdown('<div class="ao"><b>🟠 HIGH RISK</b><br>Showing clear warning signs. Must be contacted this week. Early action now is far cheaper than chasing a default later.</div>', unsafe_allow_html=True)
    with e3: st.markdown('<div class="ao"><b>🟡 MEDIUM</b><br>Some risk factors present. Monitor monthly. Send a friendly reminder SMS if payment is approaching.</div>', unsafe_allow_html=True)
    with e4: st.markdown('<div class="ag"><b>🟢 LOW RISK</b><br>Paying reliably. No immediate action needed. Focus resources on the higher risk groups.</div>', unsafe_allow_html=True)

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
    st.markdown("### 🔴 Critical & High Risk Accounts — Needs Immediate Attention")
    st.caption("These customers are most likely to default. Contact them now before the loan deteriorates further.")
    urgent = dff[dff["risk_level"].isin(["Critical","High Risk"])].copy()
    urgent = urgent.sort_values("default_probability", ascending=False)
    urgent["default_probability"] = (urgent["default_probability"]*100).round(1)
    urgent["outstanding_balance"] = urgent["outstanding_balance"].apply(lambda x: f"P{x:,.0f}")
    urgent["monthly_income_bwp"]  = urgent["monthly_income_bwp"].apply(lambda x: f"P{x:,.0f}")
    show = urgent[["customer_id","loan_type","branch","loan_officer","outstanding_balance",
                   "monthly_income_bwp","days_late","risk_level","default_probability",
                   "payment_status","collection_action"]].copy()
    show.columns = ["Customer","Loan Type","Branch","Officer","Outstanding","Income",
                    "Days Late","Risk","Default %","Status","Action Taken"]
    st.dataframe(show.reset_index(drop=True), use_container_width=True)

    csv = show.to_csv(index=False).encode()
    st.download_button("📥 Export At-Risk List", csv, "at_risk_accounts.csv", "text/csv")

# ════════════════════════════════════════════════════════════════
# PAGE 3 — LOSSES & COLLECTIONS
# ════════════════════════════════════════════════════════════════
elif page == "💸  Losses & Collections":
    st.markdown('<div class="topbar"><h1>💸 Financial Losses & Collections</h1><p>Where money is being lost and what collection steps have been taken</p></div>', unsafe_allow_html=True)

    problem = dff[dff["payment_status"].isin(["Defaulted","Late (30–89 days)"])]
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
                      color_discrete_map={"None":"#b91c1c","SMS Sent":"#1e4a6f",
                                          "Called":"#2563eb","Letter Sent":"#3b82f6",
                                          "Home Visit":"#1e3a8a","Legal Notice":"#422006"})
        fig2.update_traces(textposition="outside", textfont_color="#0f172a"); fig2.update_layout(showlegend=False)
        st.plotly_chart(wchart(fig2), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 Late Accounts With NO Collection Action")
    st.caption("These customers are behind on payments and nobody has contacted them yet — priority for outreach")
    if len(no_action) == 0:
        st.success("✅ All late accounts have had at least one collection action.")
    else:
        show = no_action[["customer_id","loan_type","branch","loan_officer",
                           "outstanding_balance","days_late","payment_status","expected_loss_bwp"]].copy()
        show["outstanding_balance"] = show["outstanding_balance"].apply(lambda x:f"P{x:,.0f}")
        show["expected_loss_bwp"]   = show["expected_loss_bwp"].apply(lambda x:f"P{x:,.0f}")
        show.columns = ["Customer","Loan Type","Branch","Officer","Outstanding",
                        "Days Late","Status","Expected Loss"]
        st.dataframe(show.reset_index(drop=True), use_container_width=True)
        csv = show.to_csv(index=False).encode()
        st.download_button("📥 Export No-Action List", csv, "no_action_accounts.csv", "text/csv")
    st.markdown('<div class="ar"><b>💡 Action Needed:</b> Every day a late account goes without contact, recovery becomes harder. Research shows that customers contacted within the first 30 days of being late are 3× more likely to catch up than those contacted after 90 days.</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# PAGE 4 — BRANCH PERFORMANCE
# ════════════════════════════════════════════════════════════════
elif page == "🏢  Branch Performance":
    st.markdown('<div class="topbar"><h1>🏢 Branch Performance Report</h1><p>How each branch is performing on loan quality and defaults</p></div>', unsafe_allow_html=True)

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
        st.markdown('<div class="ccard"><div class="ctitle">Portfolio Size vs Losses by Branch</div><div class="csub">Bigger portfolios are expected to have larger losses — the key is the proportion</div>', unsafe_allow_html=True)
        fig2 = px.scatter(br, x="portfolio", y="losses", size="loans",
                          color="default_rate", color_continuous_scale=["#166534","#b91c1c"],
                          hover_name="branch", text="branch",
                          labels={"portfolio":"Portfolio Value (BWP)","losses":"Expected Losses (BWP)",
                                  "default_rate":"Default Rate %"})
        fig2.update_traces(textposition="top center", textfont_color="#0f172a")
        st.plotly_chart(wchart(fig2), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 Branch Summary Table")
    br_show = br.copy()
    br_show["portfolio"] = br_show["portfolio"].apply(lambda x:f"P{x/1e6:.2f}M")
    br_show["losses"]    = br_show["losses"].apply(lambda x:f"P{x/1e3:.0f}K")
    br_show["avg_credit"]= br_show["avg_credit"].apply(lambda x:f"{x:.0f}")
    br_show.columns      = ["Branch","Loans","Portfolio","Defaults","Est. Losses",
                             "Avg Credit Score","Default Rate %","Loss Rate %"]
    st.dataframe(br_show.reset_index(drop=True), use_container_width=True)

    st.markdown("---")
    st.markdown("### 👔 Loan Officer Default Rates")
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

# ════════════════════════════════════════════════════════════════
# PAGE 5 — CUSTOMER INSIGHTS
# ════════════════════════════════════════════════════════════════
elif page == "👤  Customer Insights":
    st.markdown('<div class="topbar"><h1>👤 Customer Profile Insights</h1><p>Understanding which types of customers carry the most risk</p></div>', unsafe_allow_html=True)

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
        st.markdown('<div class="ccard"><div class="ctitle">Credit Score Distribution</div><div class="csub">Where our customers sit on the credit score scale — lower scores mean higher risk</div>', unsafe_allow_html=True)
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
            labels=["Under P5K","P5K–P10K","P10K–P20K","P20K–P50K","Over P50K"])
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
st.markdown("<div style='text-align:center;color:#475569;font-size:.78rem'>Thebe Credit Union · Loan Portfolio Dashboard · Prepared by Unaswi Leonard · 2026</div>", unsafe_allow_html=True)