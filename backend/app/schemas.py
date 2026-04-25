from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ----- Auth ----------------------------------------------------------------


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


# ----- Courses / Lessons ---------------------------------------------------


class LessonCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    subject: str = Field("", max_length=80)
    objective: str = Field("", max_length=20_000)


class LessonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner_id: int
    title: str
    subject: str
    objective: str
    created_at: datetime


# ----- Sessions / Tutor ----------------------------------------------------


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
    message: str = Field(..., min_length=1, max_length=4_000)


class TutorReply(BaseModel):
    agent: str
    reply: str


# ----- Concept Map ---------------------------------------------------------


class ConceptOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    session_id: int
    label: str
    summary: str
    mastery: float
    parent_id: int | None


class MasteryUpdate(BaseModel):
    delta: float = Field(..., ge=-1.0, le=1.0)


# ----- Replay --------------------------------------------------------------


class ReplaySessionOut(BaseModel):
    session_id: int
    lesson_id: int | None
    status: str
    started_at: datetime
    ended_at: datetime | None
    transcript: str
    concepts: list[ConceptOut]


# ----- Notes ---------------------------------------------------------------


class NotesIn(BaseModel):
    text: str = Field(..., max_length=20_000)


class NotesOut(BaseModel):
    session_id: int
    markdown: str
    summary: str
    gaps: list[str]
    suggestions: list[str]


# ----- Network -------------------------------------------------------------


class PeerMatchRequest(BaseModel):
    concept: str | None = None
    lesson_id: int | None = None


class PeerMatchResponse(BaseModel):
    state: str  # "waiting" | "matched"
    room_token: str
    peer: str | None = None


class NetworkStatus(BaseModel):
    waiting: int
    active_rooms: int
    hot_concepts: list[str]


# ----- Dashboard -----------------------------------------------------------


class DashboardOut(BaseModel):
    user: UserOut
    courses: int
    sessions: int
    messages: int
    concepts_total: int
    concepts_mastered: int
    grounded_rate: float
    recent_sessions: list[SessionOut]
