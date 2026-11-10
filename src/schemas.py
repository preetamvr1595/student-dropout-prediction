"""Pydantic request/response schemas for the prediction API."""
from pydantic import BaseModel, Field
from typing import Optional


class StudentInput(BaseModel):
    """Input features for a single student prediction."""
    marital_status: int = Field(..., description="Marital status code")
    application_mode: int = Field(..., description="Application mode code")
    course: int = Field(..., description="Course code")
    tuition_fees_up_to_date: int = Field(..., ge=0, le=1)
    scholarship_holder: int = Field(..., ge=0, le=1)
    age_at_enrollment: int = Field(..., ge=15, le=70)
    curricular_units_1st_sem_approved: int = Field(..., ge=0)
    curricular_units_1st_sem_grade: float = Field(..., ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "marital_status": 1,
                "application_mode": 1,
                "course": 9254,
                "tuition_fees_up_to_date": 1,
                "scholarship_holder": 0,
                "age_at_enrollment": 20,
                "curricular_units_1st_sem_approved": 5,
                "curricular_units_1st_sem_grade": 12.5,
            }
        }


class PredictionResult(BaseModel):
    """API response for a single student prediction."""
    dropout_probability: float
    risk_label: str
    threshold: float
    stage: str
