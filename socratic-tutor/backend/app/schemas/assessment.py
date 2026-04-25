from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class AssessRequest(BaseModel):
    background_text: str = Field(..., min_length=1, max_length=5000)


class SkillDimensionResponse(BaseModel):
    name: str
    level: str
    score: int
    max_score: int
    description: str


class AssessmentResponse(BaseModel):
    id: str
    overall_level: str
    overall_summary: str
    skill_dimensions: List[SkillDimensionResponse]
    strengths: List[str]
    gaps: List[str]
    recommended_module_id: Optional[str]
    recommendation_text: str
    background_text: str
    created_at: datetime


class AssessmentSummaryResponse(BaseModel):
    id: str
    overall_level: str
    created_at: datetime
