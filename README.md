# Student Success Analytics - Early Warning & Academic Risk Intelligence

A modern SaaS analytics web platform and machine learning decision-support tool for identifying higher education students at risk of academic dropout at the end of their first semester.

---

## 📌 Project Overview
Higher education institutions face significant challenges with student attrition. This system leverages classical machine learning models trained on student background demographics, socioeconomic factors, admission qualifications, and **first-semester academic performance** to estimate student outcome probabilities (`Graduate`, `Dropout`, `Enrolled`).

---

## 🏆 Key Machine Learning Highlights

- **Dataset:** UCI Predict Students' Dropout and Academic Success (`4,424` student records).
- **Target Outcome Classes:** 
  - `Graduate`: 2,209 (49.93%)
  - `Dropout`: 1,421 (32.12%)
  - `Enrolled`: 794 (17.95%)
- **Selected Model:** **Random Forest (Balanced)**
- **Primary Selection Metric:** **Macro F1 = 0.6898** (Chosen over accuracy due to multiclass imbalance).
- **Overall Model Accuracy:** **73.90%**
- **Multiclass ROC-AUC:** **0.8650**
- **Strict Data Leakage Guard:** Excludes all 6 second-semester features (`Curricular units 2nd sem...`) to preserve realistic early warning capability at the end of the first semester.

---

## 🛠️ Technology Stack
- **Language:** Python 3.14
- **Data & ML Pipelines:** Pandas, NumPy, Scikit-learn, XGBoost, Joblib
- **Interactive Visualizations:** Plotly, Matplotlib, Seaborn
- **Web Application Framework:** Streamlit

---

## 🚀 Quickstart Guide

### 1. Clone Repository
```bash
git clone https://github.com/poorvakale10/StudentSuccessAnalytics.git
cd StudentSuccessAnalytics
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Streamlit Dashboard
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 👥 Project Team
- **Atharva Damale** — 23102C0004
- **Poorva Kale** — 23102C0015
- **Shreya Sathish** — 23102C0019
- **Raj Yadav** — 23102C0031
