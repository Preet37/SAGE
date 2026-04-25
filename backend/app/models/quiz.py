from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from cuid2 import cuid_wrapper

cuid = cuid_wrapper()

DIFFICULTY_LEVELS = ("beginner", "intermediate", "advanced", "expert")


class QuizSession(SQLModel, table=True):
    __tablename__ = "quizsession"

    id: str = Field(default_factory=cuid, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    lesson_id: Optional[str] = Field(default=None, foreign_key="lesson.id")
    topic: str
    difficulty: str = "intermediate"
    total_questions: int = 5
    correct_count: int = 0
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    questions: List["QuizQuestion"] = Relationship(back_populates="session")
    answers: List["QuizAnswer"] = Relationship(back_populates="session")


class QuizQuestion(SQLModel, table=True):
    __tablename__ = "quizquestion"

    id: str = Field(default_factory=cuid, primary_key=True)
    session_id: str = Field(foreign_key="quizsession.id", index=True)
    order_index: int
    difficulty: str = "intermediate"
    question_type: str = "multiple_choice"
    question_text: str
    options: str  # JSON: [{"id": "a", "text": "..."}, ...]
    correct_option_id: str
    hint: str = ""
    explanation: str = ""

    session: Optional[QuizSession] = Relationship(back_populates="questions")
    answers: List["QuizAnswer"] = Relationship(back_populates="question")


class QuizAnswer(SQLModel, table=True):
    __tablename__ = "quizanswer"

    id: str = Field(default_factory=cuid, primary_key=True)
    question_id: str = Field(foreign_key="quizquestion.id", index=True)
    session_id: str = Field(foreign_key="quizsession.id", index=True)
    selected_option_id: str
    is_correct: bool
    answered_at: datetime = Field(default_factory=datetime.utcnow)

    question: Optional[QuizQuestion] = Relationship(back_populates="answers")
    session: Optional[QuizSession] = Relationship(back_populates="answers")
