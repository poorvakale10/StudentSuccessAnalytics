from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class StudentFeatureInput(BaseModel):
    # New Academic Inputs
    tenth_grade_pct: float = Field(..., example=85.0, description="10th Grade Marks Percentage (0 - 100%)")
    twelfth_grade_pct: float = Field(..., example=80.0, description="12th Grade Marks Percentage (0 - 100%)")
    current_sem_gpa: float = Field(..., example=8.2, description="Current Semester GPA (0 - 10 scale)")
    cgpa: float = Field(..., example=8.5, description="Aggregate CGPA until now (0 - 10 scale)")
    first_sem_approval_rate: float = Field(..., example=0.83, description="1st semester approval rate (0.0 - 1.0)")
    
    # Financial Inputs
    debtor: int = Field(..., example=0, description="Debtor status: 1=Yes, 0=No")
    tuition_up_to_date: int = Field(..., example=1, description="Tuition fees up to date: 1=Yes, 0=No")
    scholarship_holder: int = Field(..., example=0, description="Scholarship holder: 1=Yes, 0=No")
    
    # Demographic Inputs
    age_at_enrollment: int = Field(..., example=20, description="Age at enrollment")
    gender: int = Field(..., example=1, description="Gender: 1=Male, 0=Female")
    marital_status: int = Field(..., example=1, description="Marital status: 1=Single, 2=Married, etc.")
    displaced: int = Field(..., example=1, description="Displaced (living away from home): 1=Yes, 0=No")
    
    # Family & Context Inputs
    mother_qualification: int = Field(..., example=1, description="Mother's qualification code")
    father_qualification: int = Field(..., example=1, description="Father's qualification code")
    application_mode: int = Field(..., example=1, description="Application mode code")
    course: int = Field(..., example=9254, description="Course code")
    unemployment_rate: float = Field(..., example=10.8, description="Unemployment rate (%)")
    gdp: float = Field(..., example=1.74, description="GDP rate (%)")

    # Optional internal mapping overrides if direct 18-feature raw dict is provided
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
