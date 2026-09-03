from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class StudentFeatureInput(BaseModel):
    previous_qualification_grade: float = Field(..., example=130.0, description="Previous qualification grade (0-200)")
    admission_grade: float = Field(..., example=125.0, description="Admission grade (0-200)")
    first_sem_grade: float = Field(..., example=12.5, description="1st semester average grade (0-20)")
    first_sem_approval_rate: float = Field(..., example=0.83, description="1st semester approval rate (0.0 - 1.0)")
    attendance_type: int = Field(..., example=1, description="Attendance type: 1=Daytime, 0=Evening")
    debtor: int = Field(..., example=0, description="Debtor status: 1=Yes, 0=No")
    tuition_up_to_date: int = Field(..., example=1, description="Tuition fees up to date: 1=Yes, 0=No")
    scholarship_holder: int = Field(..., example=0, description="Scholarship holder: 1=Yes, 0=No")
    age_at_enrollment: int = Field(..., example=20, description="Age at enrollment")
    gender: int = Field(..., example=1, description="Gender: 1=Male, 0=Female")
    marital_status: int = Field(..., example=1, description="Marital status: 1=Single, 2=Married, etc.")
    displaced: int = Field(..., example=1, description="Displaced (living away from home): 1=Yes, 0=No")
    mother_qualification: int = Field(..., example=1, description="Mother's qualification code")
    father_qualification: int = Field(..., example=1, description="Father's qualification code")
    application_mode: int = Field(..., example=1, description="Application mode code")
    course: int = Field(..., example=9254, description="Course code")
    unemployment_rate: float = Field(..., example=10.8, description="Unemployment rate (%)")
    gdp: float = Field(..., example=1.74, description="GDP rate (%)")

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
