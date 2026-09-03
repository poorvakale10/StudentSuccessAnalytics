from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class StudentFeatureInput(BaseModel):
    # 1. Academic Performance Features
    tenth_grade_pct: float = Field(default=75.0, ge=0.0, le=100.0, description="10th Grade Marks Percentage (0 - 100%)")
    twelfth_grade_pct: float = Field(default=72.0, ge=0.0, le=100.0, description="12th Grade Marks Percentage (0 - 100%)")
    current_sem_gpa: float = Field(default=7.5, ge=0.0, le=10.0, description="Current Semester GPA (0.0 - 10.0 scale)")
    cgpa: float = Field(default=7.8, ge=0.0, le=10.0, description="Aggregate CGPA until now (0.0 - 10.0 scale)")
    courses_enrolled: int = Field(default=6, ge=0, le=30, description="Number of courses enrolled")
    courses_approved: int = Field(default=5, ge=0, le=30, description="Number of courses approved/passed")
    courses_failed: int = Field(default=1, ge=0, le=30, description="Number of courses failed")
    
    # 2. Attendance / Academic Participation Features
    attendance_pct: float = Field(default=85.0, ge=0.0, le=100.0, description="Attendance Percentage (0 - 100%)")
    evaluation_participation_pct: float = Field(default=80.0, ge=0.0, le=100.0, description="Evaluation Participation (%)")
    assignment_submission_pct: float = Field(default=85.0, ge=0.0, le=100.0, description="Assignment Submission (%)")
    
    # 3. Wellbeing Inputs (1 – 5 Rating Scale)
    stress_level: int = Field(default=3, ge=1, le=5, description="Stress Level (1 = Low, 5 = Severe)")
    anxiety_level: int = Field(default=3, ge=1, le=5, description="Anxiety Level (1 = Low, 5 = Severe)")
    sleep_quality: int = Field(default=3, ge=1, le=5, description="Sleep Quality (1 = Poor, 5 = Excellent)")
    motivation_level: int = Field(default=3, ge=1, le=5, description="Motivation Level (1 = Low, 5 = High)")
    academic_satisfaction: int = Field(default=3, ge=1, le=5, description="Academic Satisfaction (1 = Low, 5 = High)")
    social_support: int = Field(default=3, ge=1, le=5, description="Social Support (1 = Poor, 5 = Strong)")
    study_life_balance: int = Field(default=3, ge=1, le=5, description="Study-Life Balance (1 = Poor, 5 = Great)")
    
    # 4. Financial & Demographic Signals
    debtor: int = Field(default=0, description="Debtor status: 1=Yes, 0=No")
    tuition_up_to_date: int = Field(default=1, description="Tuition fees up to date: 1=Yes, 0=No")
    scholarship_holder: int = Field(default=0, description="Scholarship holder: 1=Yes, 0=No")
    age_at_enrollment: int = Field(default=20, ge=15, le=70, description="Age at enrollment")
    gender: int = Field(default=1, description="Gender: 1=Male, 0=Female")
    displaced: int = Field(default=1, description="Displaced (living away from home): 1=Yes, 0=No")

class FactorExplanation(BaseModel):
    feature: str
    label: str
    value: Any
    shap_value: float
    effect: str
    explanation: str

class PredictionResponse(BaseModel):
    predicted_class: str
    probabilities: Dict[str, float]
    risk_tier: str  # High, Medium, Low
    academic_risk_score: int    # 0 - 100 normalized score
    wellbeing_risk_score: int   # 0 - 100 normalized score
    financial_risk_score: int   # 0 - 100 normalized score
    overall_dropout_prob_pct: int # 0 - 100% overall dropout probability
    top_factors: List[FactorExplanation]
    recommendations: List[str]
