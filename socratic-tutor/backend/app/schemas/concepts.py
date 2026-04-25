from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class ConceptSearchRequest(BaseModel):
    topic: str


class MisconceptionItem(BaseModel):
    text: str
    is_correct: bool


class ConceptPageResponse(BaseModel):
    id: str
    topic: str
    level: str
    simple_definition: str
    why_it_matters: str
    detailed_explanation: str
    analogy: str
    real_world_example: str
    misconceptions: List[MisconceptionItem]
    key_takeaways: List[str]
    related_concepts: List[str]
    further_reading: List[str]
    lesson_id: Optional[str]
    created_at: datetime


class ConceptSuggestion(BaseModel):
    label: str
    lesson_id: Optional[str] = None
