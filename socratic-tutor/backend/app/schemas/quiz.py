from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, field_validator


VALID_DIFFICULTIES = {"beginner", "intermediate", "advanced", "expert"}


class QuizGenerateRequest(BaseModel):
    lesson_id: str
    difficulty: str = "intermediate"
    num_questions: int = 5

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, v: str) -> str:
        v = v.lower()
        if v not in VALID_DIFFICULTIES:
            raise ValueError(f"difficulty must be one of {VALID_DIFFICULTIES}")
        return v

    @field_validator("num_questions")
    @classmethod
    def validate_num_questions(cls, v: int) -> int:
        if v < 1 or v > 20:
            raise ValueError("num_questions must be between 1 and 20")
        return v


class QuizAnswerRequest(BaseModel):
    question_id: str
    selected_option_id: str


class OptionResponse(BaseModel):
    id: str
    text: str


class QuizQuestionResponse(BaseModel):
    id: str
    order_index: int
    difficulty: str
    question_type: str
    question_text: str
    options: List[OptionResponse]
    hint: str


class QuizAnswerResponse(BaseModel):
    is_correct: bool
    correct_option_id: str
    explanation: str
    correct_count: int
    completed: bool


class QuizSessionResponse(BaseModel):
    id: str
    topic: str
    difficulty: str
    total_questions: int
    correct_count: int
    completed: bool
    created_at: datetime
    questions: List[QuizQuestionResponse]


class QuizSessionSummary(BaseModel):
    id: str
    topic: str
    difficulty: str
    total_questions: int
    correct_count: int
    completed: bool
    created_at: datetime


class QuizTopicResponse(BaseModel):
    lesson_id: str
    lesson_title: str
    module_title: str
    path_title: str
    level: str
    concepts: List[str]
