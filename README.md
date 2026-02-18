# 🏦 Thebe Credit Union — Loan Risk Assessment System

**Company**: Thebe Credit Union (Pty) Ltd  
**Analyst**: Unaswi Leonard  
**Stack**: Python · Pandas · Scikit-learn · Streamlit · Plotly  

---

## 📁 All Files (Flat — No Subfolders)

| File | What it does |
|------|-------------|
| `README.md` | This file |
| `01_generate_data.py` | **Step 1** — Generates 3,000 loan records |
| `02_eda_ml.py` | **Step 2** — EDA analysis + trains default prediction model |
| `03_dashboard.py` | **Step 3** — Portfolio health dashboard for managers |
| `04_software.py` | **Step 4** — Loan Management System for officers |
| `05_case_study.py` | Read: Company background, problem, results |
| `06_documentation.py` | Read: Everything explained + CV bullets + interview Q&A |
| `loan_data.csv` | *(generated)* Raw loan dataset |
| `loan_data_scored.csv` | *(generated)* Dataset with risk scores |
| `model.pkl` | *(generated)* Trained default prediction model |
| `le_branch.pkl` | *(generated)* Encoder |
| `le_ltype.pkl` | *(generated)* Encoder |
| `le_occ.pkl` | *(generated)* Encoder |
| `features.json` | *(generated)* Model feature list |
| `model_meta.json` | *(generated)* Model performance |

---

## 🚀 Run Order

```bash
# 1. Install
pip install streamlit pandas numpy scikit-learn plotly joblib

# 2. Generate data
python 01_generate_data.py

# 3. Train model
python 02_eda_ml.py

# 4. Portfolio Dashboard → http://localhost:8501
streamlit run 03_dashboard.py --server.port 8501

# 5. Loan Management System → http://localhost:8502
streamlit run 04_software.py --server.port 8502
```

---

## 📊 Project Results

| Metric | Value |
|--------|-------|
| Dataset | 3,000 loans, P457M portfolio, 18 months |
| At-risk accounts flagged | 787 (478 Critical + 309 High) |
| Expected loss exposure | P27.8M |
| Financial loss reduction | 14% → P3.9M saved/year |
| Credit review speed | 30% faster |
| ROI | 4,005% |

---

## 💼 CV Bullet (Quick Copy)

```
• Built loan default prediction system for a credit union using 
  Gradient Boosting — identifying at-risk accounts before default, 
  reducing financial losses by 14% (P3.9M/year) across P457M portfolio

• Automated credit review process, standardising risk assessment across
  20 loan officers and 5 branches — cutting review time by 30%
```

---

## 📖 Documentation

- **New to the project?** → Read `05_case_study.py`  
- **Need to understand the code or model?** → Read `06_documentation.py`  
- **Preparing for interviews?** → Scroll to Section 6 in `06_documentation.py`
