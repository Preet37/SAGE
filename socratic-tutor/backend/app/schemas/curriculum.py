from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class CurriculumGenerateRequest(BaseModel):
    learning_goals: str = Field(..., min_length=1, max_length=5000)


class LessonRef(BaseModel):
    id: str
    title: str
    summary: str
    course_title: str
    path_slug: str = ""
    completed: bool = False


class PhaseResponse(BaseModel):
    order: int
    title: str
    level: str
    estimated_hours: float
    description: str
    lessons: List[LessonRef]
    milestone_title: str
    milestone_skills: List[str]


class GapResponse(BaseModel):
    topic: str
    description: str
    explore_query: str


class CurriculumResponse(BaseModel):
    id: str
    title: str
    level_range: str
    estimated_hours: float
    personalization_note: str
    phases: List[PhaseResponse]
    gaps: List[GapResponse]
    learning_goals: str
    created_at: datetime


class CurriculumSummaryResponse(BaseModel):
    id: str
    title: str
    level_range: str
    created_at: datetime
