# DropoutSense — Student Dropout Risk Predictor

DropoutSense is a full-stack web application designed to predict student dropout risk and provide actionable, SHAP-explained insights using classical machine learning trained on the UCI "Predict Students' Dropout and Academic Success" dataset.

---

## 🚀 System Features

- **18 Curated Feature Signals**: Curated from the original 36-column UCI dataset across Academic, Financial, Demographic, Family, and Macroeconomic categories.
- **Engineered Academic Signals**: Raw per-unit breakdowns consolidated into 1st Semester Average Grade & Approval Rate (`approved / enrolled`).
- **Multiclass ML Engine**: Trains and compares **Logistic Regression, Random Forest, XGBoost, and Support Vector Machines (SVM)**. Winning model: **Random Forest** (**71.5% Accuracy**, **0.6681 Macro F1**).
- **SHAP Explainability**: Natural language explanation cards highlighting top positive and negative contributing factors for every prediction.
- **Interactive Dark-Themed Frontend**: Built with React, Tailwind CSS v4, and Recharts. Includes Landing page animated stat counters, filterable analytics dashboard, multi-step risk prediction form with instant profile presets, and model benchmark comparisons.

---

## 🛠️ Architecture & Tech Stack

- **Backend**: Python 3.14, FastAPI, Scikit-learn, XGBoost, SHAP, Pydantic, Uvicorn.
- **Frontend**: React 19, Vite, Tailwind CSS v4, Recharts, Lucide Icons.

```
DropoutSense/
├── backend/
│   ├── main.py              # FastAPI server (predict, metrics, dataset-insights)
│   ├── schemas.py           # Pydantic request/response validation schemas
│   ├── artifacts/           # Trained models, metrics JSON, dataset insights
│   └── ml/
│       └── train_model.py   # Machine learning training & evaluation pipeline
├── frontend/                # Vite + React + Tailwind CSS web application
│   ├── src/
│   │   ├── components/      # Navbar, Landing, Dashboard, Risk Predictor, Performance
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
└── data/
    └── data.csv             # UCI Student Dataset (4,424 records)
```

---

## 💻 Quickstart

### 1. Install Backend Dependencies & Train ML Models
```bash
pip install -r requirements.txt
python backend/ml/train_model.py
```

### 2. Launch FastAPI Backend Server
```bash
python -m uvicorn backend.main:app --port 8000 --reload
```
API Documentation available at: `http://127.0.0.1:8000/docs`

### 3. Launch React Frontend
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173/` in your browser.

---

## 📊 REST API Endpoints

- `POST /api/predict`: Evaluates 18 feature inputs -> returns predicted target class (`Dropout`, `Enrolled`, `Graduate`), confidence gauge, risk tier (`High`, `Medium`, `Low`), SHAP factors, and advisor next steps.
- `GET /api/model-metrics`: Model benchmark comparison statistics across LR, RF, XGB, SVM, and confusion matrix.
- `GET /api/dataset-insights`: Aggregate stats for dashboard visualizations (course dropout rates, financial status impact, grade distributions).

---

## 📜 License
MIT License
