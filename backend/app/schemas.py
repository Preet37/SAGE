from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field("", max_length=120)
    password: str = Field(..., min_length=8, max_length=1024)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    name: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LessonCreate(BaseModel):
    title: str
    subject: str = ""
    objective: str = ""


class LessonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner_id: int
    title: str
    subject: str
    objective: str
    created_at: datetime


class SessionCreate(BaseModel):
    lesson_id: int | None = None


class SessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    lesson_id: int | None
    status: str
    started_at: datetime
    ended_at: datetime | None


class TutorTurn(BaseModel):
    session_id: int
    message: str


class TutorReply(BaseModel):
    agent: str
    reply: str


class ConceptOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    session_id: int
    label: str
    summary: str
    mastery: float
    parent_id: int | None
