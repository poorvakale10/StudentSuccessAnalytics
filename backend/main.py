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
    description="Student Dropout Risk Predictor backend API using machine learning model, sub-risk scoring (Academic, Wellbeing, Financial), and SHAP explainability.",
    version="2.0.0"
)

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

artifacts = None
metrics_data = None
insights_data = None

FEATURE_LABELS = {
    'tenth_grade_pct': '10th Grade Marks (%)',
    'twelfth_grade_pct': '12th Grade Marks (%)',
    'current_sem_gpa': 'Current Semester GPA',
    'cgpa': 'Aggregate CGPA',
    'courses_enrolled': 'Enrolled Courses',
    'courses_approved': 'Approved Courses',
    'courses_failed': 'Failed Courses',
    'attendance_pct': 'Attendance (%)',
    'evaluation_participation_pct': 'Evaluation Participation (%)',
    'assignment_submission_pct': 'Assignment Submission (%)',
    'stress_level': 'Stress Level (1-5)',
    'anxiety_level': 'Anxiety Level (1-5)',
    'sleep_quality': 'Sleep Quality (1-5)',
    'motivation_level': 'Motivation Level (1-5)',
    'academic_satisfaction': 'Academic Satisfaction (1-5)',
    'social_support': 'Social Support (1-5)',
    'study_life_balance': 'Study-Life Balance (1-5)',
    'debtor': 'Debtor Status',
    'tuition_up_to_date': 'Tuition Status',
    'scholarship_holder': 'Scholarship Status',
    'age_at_enrollment': 'Age at Enrollment',
    'gender': 'Gender',
    'displaced': 'Displaced Status'
}

@app.on_event("startup")
def load_resources():
    global artifacts, metrics_data, insights_data

    if os.path.exists(MODEL_PKL_PATH):
        with open(MODEL_PKL_PATH, "rb") as f:
            artifacts = pickle.load(f)
        print("Loaded ML model artifacts successfully.")

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

def format_explanation(feat: str, val: Any, shap_val: float) -> str:
    lbl = FEATURE_LABELS.get(feat, feat)
    
    if feat == 'courses_failed':
        if val > 0:
            return f"Failed {val} course(s), which directly escalates academic risk profile."
        else:
            return "Zero course failures, maintaining clean academic completion record."

    elif feat == 'assignment_submission_pct':
        if val < 70:
            return f"Low assignment submission rate ({val}%) indicates academic disengagement."
        else:
            return f"High assignment submission rate ({val}%) demonstrates strong continuous evaluation effort."

    elif feat == 'attendance_pct':
        if val < 75:
            return f"Class attendance ({val}%) is below mandatory academic participation benchmark."
        else:
            return f"Consistent class attendance ({val}%) supports learning continuity."

    elif feat == 'stress_level':
        if val >= 4:
            return f"Elevated stress level ({val}/5) creates acute psychological pressure."
        else:
            return f"Low/Manageable stress rating ({val}/5) supports mental wellness."

    elif feat == 'anxiety_level':
        if val >= 4:
            return f"High anxiety rating ({val}/5) impacts exam performance and focus."
        else:
            return f"Low anxiety score ({val}/5) aids cognitive focus."

    elif feat == 'sleep_quality':
        if val <= 2:
            return f"Poor sleep quality rating ({val}/5) contributes to fatigue and burnout."
        else:
            return f"Good sleep quality rating ({val}/5) provides cognitive restoration."

    elif feat == 'motivation_level':
        if val <= 2:
            return f"Low motivation score ({val}/5) signals disinterest or loss of direction."
        else:
            return f"Strong motivation rating ({val}/5) drives academic goal commitment."

    elif feat == 'tuition_up_to_date':
        if val == 0:
            return "Tuition fees are overdue, creating immediate financial hold risk."
        else:
            return "Tuition payments are up to date, eliminating administrative financial hold."

    elif feat == 'debtor':
        if val == 1:
            return "Student is flagged as a debtor with outstanding financial balances."
        else:
            return "Student has no outstanding debt with the institution."

    else:
        direction = "increases" if shap_val > 0 else "decreases"
        return f"{lbl} ({val}) {direction} overall dropout probability."

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

    feature_dict = {
        'tenth_grade_pct': float(input_data.tenth_grade_pct),
        'twelfth_grade_pct': float(input_data.twelfth_grade_pct),
        'current_sem_gpa': float(input_data.current_sem_gpa),
        'cgpa': float(input_data.cgpa),
        'courses_enrolled': int(input_data.courses_enrolled),
        'courses_approved': int(input_data.courses_approved),
        'courses_failed': int(input_data.courses_failed),
        'attendance_pct': float(input_data.attendance_pct),
        'evaluation_participation_pct': float(input_data.evaluation_participation_pct),
        'assignment_submission_pct': float(input_data.assignment_submission_pct),
        'stress_level': int(input_data.stress_level),
        'anxiety_level': int(input_data.anxiety_level),
        'sleep_quality': int(input_data.sleep_quality),
        'motivation_level': int(input_data.motivation_level),
        'academic_satisfaction': int(input_data.academic_satisfaction),
        'social_support': int(input_data.social_support),
        'study_life_balance': int(input_data.study_life_balance),
        'debtor': int(input_data.debtor),
        'tuition_up_to_date': int(input_data.tuition_up_to_date),
        'scholarship_holder': int(input_data.scholarship_holder),
        'age_at_enrollment': int(input_data.age_at_enrollment),
        'gender': int(input_data.gender),
        'displaced': int(input_data.displaced)
    }

    df_single = pd.DataFrame([feature_dict])[feature_names]

    # Predict Probabilities using ML model
    if best_model_name in ['Logistic Regression', 'SVM']:
        df_scaled = pd.DataFrame(scaler.transform(df_single), columns=feature_names)
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
    overall_dropout_pct = int(round(dropout_prob * 100))

    pred_idx = int(np.argmax(probs))
    predicted_class = target_names[pred_idx]

    if dropout_prob >= 0.45 or predicted_class == 'Dropout':
        risk_tier = 'High'
    elif dropout_prob >= 0.22 or enrolled_prob >= 0.35:
        risk_tier = 'Medium'
    else:
        risk_tier = 'Low'

    # Compute Normalized Sub-Risk Scores (0 - 100)
    enrolled_cnt = max(1, input_data.courses_enrolled)
    fail_factor = min(1.0, input_data.courses_failed / enrolled_cnt)
    approval_factor = 1.0 - (input_data.courses_approved / enrolled_cnt)
    gpa_factor = 1.0 - (input_data.current_sem_gpa / 10.0)
    assign_factor = 1.0 - (input_data.assignment_submission_pct / 100.0)
    acad_risk_raw = (fail_factor * 0.35 + approval_factor * 0.35 + gpa_factor * 0.15 + assign_factor * 0.15) * 100
    academic_risk_score = int(np.clip(round(acad_risk_raw), 0, 100))

    stress_w = (input_data.stress_level - 1) / 4.0
    anxiety_w = (input_data.anxiety_level - 1) / 4.0
    sleep_w = 1.0 - (input_data.sleep_quality - 1) / 4.0
    motivation_w = 1.0 - (input_data.motivation_level - 1) / 4.0
    satisfaction_w = 1.0 - (input_data.academic_satisfaction - 1) / 4.0
    support_w = 1.0 - (input_data.social_support - 1) / 4.0
    balance_w = 1.0 - (input_data.study_life_balance - 1) / 4.0
    well_risk_raw = (stress_w * 0.20 + anxiety_w * 0.20 + sleep_w * 0.15 + motivation_w * 0.15 + satisfaction_w * 0.10 + support_w * 0.10 + balance_w * 0.10) * 100
    wellbeing_risk_score = int(np.clip(round(well_risk_raw), 0, 100))

    tuition_f = 0.50 if input_data.tuition_up_to_date == 0 else 0.0
    debtor_f = 0.35 if input_data.debtor == 1 else 0.0
    scholarship_f = 0.15 if input_data.scholarship_holder == 0 else 0.0
    financial_risk_score = int(np.clip(round((tuition_f + debtor_f + scholarship_f) * 100), 0, 100))

    # SHAP Explainability
    try:
        if best_model_name in ['Random Forest', 'XGBoost']:
            shap_values = explainer.shap_values(df_single)
            if isinstance(shap_values, list):
                shap_class0 = shap_values[0][0]
            elif len(shap_values.shape) == 3:
                if shap_values.shape[2] == 3:
                    shap_class0 = shap_values[0, :, 0]
                else:
                    shap_class0 = shap_values[0, 0, :]
            else:
                shap_class0 = shap_values[0]
        else:
            shap_obj = explainer(df_single)
            shap_class0 = shap_obj.values[0, :, 0] if len(shap_obj.values.shape) == 3 else shap_obj.values[0]

    except Exception as e:
        print(f"SHAP calculation fallback: {e}")
        if hasattr(best_model, 'feature_importances_'):
            shap_class0 = best_model.feature_importances_
        else:
            shap_class0 = np.ones(len(feature_names))

    top_indices = np.argsort(np.abs(shap_class0))[::-1][:5]
    
    top_factors = []
    for idx in top_indices:
        feat = feature_names[idx]
        val = feature_dict[feat]
        s_val = float(shap_class0[idx])

        effect = "Increases Dropout Risk" if s_val > 0 else "Decreases Dropout Risk"
        explanation_text = format_explanation(feat, val, s_val)

        val_display = val
        if feat in ['attendance_pct', 'evaluation_participation_pct', 'assignment_submission_pct', 'tenth_grade_pct', 'twelfth_grade_pct']:
            val_display = f"{val}%"
        elif feat in ['stress_level', 'anxiety_level', 'sleep_quality', 'motivation_level', 'academic_satisfaction', 'social_support', 'study_life_balance']:
            val_display = f"{val} / 5"
        elif feat in ['debtor', 'tuition_up_to_date', 'scholarship_holder', 'displaced', 'gender']:
            val_display = "Yes" if val == 1 else "No"
            if feat == 'gender':
                val_display = "Male" if val == 1 else "Female"

        top_factors.append(FactorExplanation(
            feature=feat,
            label=FEATURE_LABELS.get(feat, feat),
            value=val_display,
            shap_value=round(s_val, 4),
            effect=effect,
            explanation=explanation_text
        ))

    recommendations = []
    if academic_risk_score > 50:
        recommendations.append("Assign an academic peer tutor and schedule mandatory course remediation counseling.")
    
    if wellbeing_risk_score > 50:
        recommendations.append("Refer student to Student Psychological Counseling Services for stress, anxiety, and burnout support.")

    if financial_risk_score > 40:
        recommendations.append("Connect student with Financial Aid Office for emergency micro-grants or flexible fee installment plans.")

    if input_data.attendance_pct < 75.0:
        recommendations.append("Provide attendance monitoring and outreach through student success advisors.")

    if risk_tier == 'Low' and len(recommendations) == 0:
        recommendations.append("Recommend student for peer mentorship opportunities and undergraduate research programs.")

    return PredictionResponse(
        predicted_class=predicted_class,
        probabilities=prob_dict,
        risk_tier=risk_tier,
        academic_risk_score=academic_risk_score,
        wellbeing_risk_score=wellbeing_risk_score,
        financial_risk_score=financial_risk_score,
        overall_dropout_prob_pct=overall_dropout_pct,
        top_factors=top_factors,
        recommendations=recommendations
    )
