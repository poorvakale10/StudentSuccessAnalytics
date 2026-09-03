from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class StudentFeatureInput(BaseModel):
    # Academic Inputs (Validated Ranges)
    tenth_grade_pct: float = Field(default=75.0, ge=0.0, le=100.0, description="10th Grade Marks Percentage (0 - 100%)")
    twelfth_grade_pct: float = Field(default=72.0, ge=0.0, le=100.0, description="12th Grade Marks Percentage (0 - 100%)")
    current_sem_gpa: float = Field(default=7.5, ge=0.0, le=10.0, description="Current Semester GPA (0 - 10 scale)")
    cgpa: float = Field(default=7.8, ge=0.0, le=10.0, description="Aggregate CGPA until now (0 - 10 scale)")
    first_sem_approval_rate: float = Field(default=0.8, ge=0.0, le=1.0, description="1st semester approval rate (0.0 - 1.0)")
    
    # Financial Inputs
    debtor: int = Field(default=0, description="Debtor status: 1=Yes, 0=No")
    tuition_up_to_date: int = Field(default=1, description="Tuition fees up to date: 1=Yes, 0=No")
    scholarship_holder: int = Field(default=0, description="Scholarship holder: 1=Yes, 0=No")
    
    # Demographic Inputs
    age_at_enrollment: int = Field(default=20, ge=15, le=70, description="Age at enrollment")
    gender: int = Field(default=1, description="Gender: 1=Male, 0=Female")
    marital_status: int = Field(default=1, description="Marital status: 1=Single, 2=Married, etc.")
    displaced: int = Field(default=1, description="Displaced (living away from home): 1=Yes, 0=No")
    
    # Mental Health & Lifestyle Inputs
    stress_level: int = Field(default=5, ge=1, le=10, description="Perceived Stress Level (1 to 10 scale)")
    screen_time_hours: float = Field(default=4.0, ge=0.0, le=24.0, description="Daily Screen Time in Hours")
    sleep_hours: float = Field(default=7.0, ge=0.0, le=12.0, description="Nightly Sleep in Hours")
    study_hours: float = Field(default=15.0, ge=0.0, le=100.0, description="Weekly Independent Study Hours")

    # Optional / Legacy Fallback Fields (Defaults so validation never fails)
    mother_qualification: Optional[int] = 1
    father_qualification: Optional[int] = 1
    application_mode: Optional[int] = 1
    course: Optional[int] = 9254
    unemployment_rate: Optional[float] = 10.8
    gdp: Optional[float] = 1.74
    previous_qualification_grade: Optional[float] = None
    first_sem_grade: Optional[float] = None
    attendance_type: Optional[int] = 1

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
    top_factors: List[FactorExplanation]
    recommendations: List[str]
