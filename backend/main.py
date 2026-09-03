import os
import pickle
import json
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.schemas import StudentFeatureInput, PredictionResponse, FactorExplanation

app = FastAPI(
    title="DropoutSense API",
    description="Student Dropout Risk Predictor backend API using UCI dataset machine learning model and SHAP explainability.",
    version="1.0.0"
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
MODEL_PKL_PATH = os.path.join(ARTIFACTS_DIR, "model_artifacts.pkl")
METRICS_JSON_PATH = os.path.join(ARTIFACTS_DIR, "model_metrics.json")
INSIGHTS_JSON_PATH = os.path.join(ARTIFACTS_DIR, "dataset_insights.json")

# Global state for loaded artifacts
artifacts = None
metrics_data = None
insights_data = None

FEATURE_LABELS = {
    'previous_qualification_grade': "Previous Qualification Grade",
    'admission_grade': "Admission Grade",
    'first_sem_grade': "1st Sem Average Grade",
    'first_sem_approval_rate': "1st Sem Approval Rate",
    'attendance_type': "Attendance Type",
    'debtor': "Debtor Status",
    'tuition_up_to_date': "Tuition Fees Status",
    'scholarship_holder': "Scholarship Status",
    'age_at_enrollment': "Age at Enrollment",
    'gender': "Gender",
    'marital_status': "Marital Status",
    'displaced': "Displaced Status",
    'mother_qualification': "Mother's Qualification",
    'father_qualification': "Father's Qualification",
    'application_mode': "Application Mode",
    'course': "Course",
    'unemployment_rate': "Unemployment Rate",
    'gdp': "GDP Rate"
}

COURSE_MAP = {
    33: "Biofuel Production Technologies",
    171: "Animation and Multimedia Design",
    8014: "Social Service (Evening)",
    9003: "Agronomy",
    9070: "Communication Design",
    9085: "Veterinary Nursing",
    9119: "Informatics Engineering",
    9130: "Equiniculture",
    9147: "Management",
    9238: "Social Service (Day)",
    9254: "Tourism",
    9500: "Nursing",
    9556: "Oral Hygiene",
    9670: "Advertising & Marketing",
    9773: "Journalism & Communication",
    9853: "Basic Education",
    9991: "Management (Evening)"
}

@app.on_event("startup")
def load_resources():
    global artifacts, metrics_data, insights_data

    if os.path.exists(MODEL_PKL_PATH):
        with open(MODEL_PKL_PATH, "rb") as f:
            artifacts = pickle.load(f)
        print("Loaded ML model artifacts successfully.")
    else:
        print("Warning: ML model artifacts pickle not found.")

    if os.path.exists(METRICS_JSON_PATH):
        with open(METRICS_JSON_PATH, "r") as f:
            metrics_data = json.load(f)
        print("Loaded model metrics JSON successfully.")

    if os.path.exists(INSIGHTS_JSON_PATH):
        with open(INSIGHTS_JSON_PATH, "r") as f:
            insights_data = json.load(f)
        print("Loaded dataset insights JSON successfully.")

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "model_loaded": artifacts is not None,
        "metrics_loaded": metrics_data is not None,
        "insights_loaded": insights_data is not None
    }

@app.get("/api/model-metrics")
def get_model_metrics():
    if metrics_data is None:
        raise HTTPException(status_code=500, detail="Model metrics not loaded.")
    return metrics_data

@app.get("/api/dataset-insights")
def get_dataset_insights():
    if insights_data is None:
        raise HTTPException(status_code=500, detail="Dataset insights not loaded.")
    return insights_data

def format_feature_explanation(feat: str, val: Any, shap_val: float) -> str:
    lbl = FEATURE_LABELS.get(feat, feat)
    
    if feat == 'first_sem_approval_rate':
        pct = int(val * 100)
        if shap_val > 0:
            return f"Low approval rate of {pct}% in 1st semester courses significantly raises dropout risk."
        else:
            return f"Strong course completion rate ({pct}%) in 1st semester reinforces academic persistence."

    elif feat == 'first_sem_grade':
        if shap_val > 0:
            return f"1st semester average grade ({val:.1f}/20) is below academic stability benchmark."
        else:
            return f"High 1st semester GPA ({val:.1f}/20) acts as a strong protective academic factor."

    elif feat == 'tuition_up_to_date':
        if val == 0:
            return "Tuition fees are overdue, creating immediate financial risk of administrative drop."
        else:
            return "Tuition payments are up to date, eliminating administrative financial hold."

    elif feat == 'debtor':
        if val == 1:
            return "Student is flagged as a debtor with outstanding institutional balances."
        else:
            return "Student has no outstanding debt with the institution."

    elif feat == 'scholarship_holder':
        if val == 1:
            return "Scholarship funding provides crucial financial stability and lowers risk."
        else:
            return "Lack of scholarship grant means higher self-funded financial burden."

    elif feat == 'age_at_enrollment':
        if val > 24:
            return f"Age at enrollment ({val} years) is higher than traditional student entry age."
        else:
            return f"Enrollment at age {val} aligns with traditional academic progression."

    elif feat == 'attendance_type':
        if val == 0:
            return "Evening attendance often overlaps with full-time employment commitments."
        else:
            return "Daytime attendance provides full access to campus resources and study groups."

    elif feat == 'admission_grade':
        if shap_val > 0:
            return f"Lower entry admission score ({val:.1f}/200) indicates initial preparation gap."
        else:
            return f"Strong entry admission score ({val:.1f}/200) reflects solid high school foundation."

    elif feat == 'previous_qualification_grade':
        if shap_val > 0:
            return f"Prior qualification score ({val:.1f}/200) contributes to risk profile."
        else:
            return f"Solid prior qualification score ({val:.1f}/200) supports learning readiness."

    elif feat == 'course':
        course_name = COURSE_MAP.get(int(val), f"Course {val}")
        return f"Enrolled in {course_name}, which has specific historical completion trends."

    elif feat == 'displaced':
        if val == 1:
            return "Living away from home may introduce social dislocation or housing stress."
        else:
            return "Living locally provides family and community proximity."

    else:
        direction = "increases" if shap_val > 0 else "decreases"
        return f"{lbl} (value: {val}) {direction} overall dropout probability."

@app.post("/api/predict", response_model=PredictionResponse)
def predict_student_risk(input_data: StudentFeatureInput):
    if artifacts is None:
        raise HTTPException(status_code=500, detail="ML model artifacts not initialized.")

    best_model = artifacts['best_model']
    best_model_name = artifacts['best_model_name']
    scaler = artifacts['scaler']
    feature_names = artifacts['feature_names']
    target_names = artifacts['target_names']
    explainer = artifacts['explainer']

    # Convert input pydantic object to feature dictionary
    input_dict = input_data.model_dump()
    df_single = pd.DataFrame([input_dict])[feature_names]

    # Predict probabilities
    if best_model_name in ['Logistic Regression', 'SVM']:
        df_scaled = scaler.transform(df_single)
        probs = best_model.predict_proba(df_scaled)[0]
    else:
        probs = best_model.predict_proba(df_single)[0]

    prob_dict = {
        'Dropout': round(float(probs[0]), 4),
        'Enrolled': round(float(probs[1]), 4),
        'Graduate': round(float(probs[2]), 4)
    }

    dropout_prob = prob_dict['Dropout']
    enrolled_prob = prob_dict['Enrolled']
    grad_prob = prob_dict['Graduate']

    # Predicted class (argmax)
    pred_idx = int(np.argmax(probs))
    predicted_class = target_names[pred_idx]

    # Assign Risk Tier
    if dropout_prob >= 0.45 or predicted_class == 'Dropout':
        risk_tier = 'High'
    elif dropout_prob >= 0.22 or enrolled_prob >= 0.35:
        risk_tier = 'Medium'
    else:
        risk_tier = 'Low'

    # SHAP Explainability
    # For multiclass, explainer output handles class 0 (Dropout)
    try:
        if best_model_name in ['Random Forest', 'XGBoost']:
            shap_values = explainer.shap_values(df_single)
            if isinstance(shap_values, list):
                # List of arrays per class, pick class 0 (Dropout)
                shap_class0 = shap_values[0][0]
            elif len(shap_values.shape) == 3:
                # Shape: (1, num_features, 3) or (1, 3, num_features)
                if shap_values.shape[2] == 3:
                    shap_class0 = shap_values[0, :, 0]
                else:
                    shap_class0 = shap_values[0, 0, :]
            else:
                shap_class0 = shap_values[0]
        else:
            # Kernel/Linear explainer
            shap_obj = explainer(df_single)
            shap_class0 = shap_obj.values[0, :, 0] if len(shap_obj.values.shape) == 3 else shap_obj.values[0]

    except Exception as e:
        print(f"SHAP calculation fallback: {e}")
        # Fallback to feature importance proxy if SHAP encounters format edge case
        if hasattr(best_model, 'feature_importances_'):
            shap_class0 = best_model.feature_importances_
        else:
            shap_class0 = np.ones(len(feature_names))

    # Top contributing factors for Dropout Risk (Class 0)
    top_indices = np.argsort(np.abs(shap_class0))[::-1][:5]
    
    top_factors = []
    for idx in top_indices:
        feat = feature_names[idx]
        val = input_dict[feat]
        s_val = float(shap_class0[idx])

        if s_val > 0:
            effect = "Increases Dropout Risk"
        else:
            effect = "Decreases Dropout Risk"

        explanation_text = format_feature_explanation(feat, val, s_val)

        # Human friendly format for UI value display
        val_display = val
        if feat == 'course':
            val_display = COURSE_MAP.get(int(val), f"Code {val}")
        elif feat == 'first_sem_approval_rate':
            val_display = f"{int(val * 100)}%"
        elif feat in ['debtor', 'tuition_up_to_date', 'scholarship_holder', 'displaced', 'attendance_type', 'gender']:
            val_display = "Yes" if val == 1 else "No"
            if feat == 'attendance_type':
                val_display = "Daytime" if val == 1 else "Evening"
            elif feat == 'gender':
                val_display = "Male" if val == 1 else "Female"

        top_factors.append(FactorExplanation(
            feature=feat,
            label=FEATURE_LABELS.get(feat, feat),
            value=val_display,
            shap_value=round(s_val, 4),
            effect=effect,
            explanation=explanation_text
        ))

    # Actionable Recommendations based on risk profile
    recommendations = []
    if input_dict['tuition_up_to_date'] == 0 or input_dict['debtor'] == 1:
        recommendations.append("Connect student with Student Financial Services for emergency micro-grants or tuition payment deferral plans.")
    
    if input_dict['first_sem_approval_rate'] < 0.6 or input_dict['first_sem_grade'] < 11.5:
        recommendations.append("Assign an academic peer tutor and schedule mandatory bi-weekly academic progress reviews.")

    if input_dict['displaced'] == 1 and risk_tier in ['High', 'Medium']:
        recommendations.append("Provide campus housing and social integration advisory support to mitigate student dislocation.")

    if input_dict['attendance_type'] == 0:
        recommendations.append("Offer flexible online learning modules and evening tutoring office hours.")

    if risk_tier == 'High' and len(recommendations) < 3:
        recommendations.append("Schedule an urgent 1-on-1 counselor intervention within 5 business days.")

    if risk_tier == 'Low':
        recommendations.append("Recommend student for peer mentorship opportunities and undergraduate research programs.")

    return PredictionResponse(
        predicted_class=predicted_class,
        probabilities=prob_dict,
        risk_tier=risk_tier,
        top_factors=top_factors,
        recommendations=recommendations
    )
