"""
Refugee / displaced learner diagnostic.
5 culturally neutral questions reconstruct a knowledge profile so SAGE
can recommend the right starting point without requiring course history.
"""
import json
import logging
import re
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.base import asi1_complete
from app.database import get_db
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/diagnostic", tags=["diagnostic"])
log = logging.getLogger("sage.diagnostic")

# ---------------------------------------------------------------------------
# Static question bank — culturally neutral, no proper-noun knowledge assumed
# ---------------------------------------------------------------------------

_QUESTIONS = [
    {
        "id": "q1",
        "subject": "reading",
        "text": 'Read this sentence and choose the word that fills the blank: "The sun rises in the ___."',
        "options": ["a) west", "b) north", "c) east", "d) south"],
        "answer": "c",
    },
    {
        "id": "q2",
        "subject": "math",
        "text": "What is 15 + 27?",
        "options": ["a) 32", "b) 42", "c) 41", "d) 52"],
        "answer": "b",
    },
    {
        "id": "q3",
        "subject": "science",
        "text": "Which of these is a living thing?",
        "options": ["a) A rock", "b) Water", "c) A tree", "d) The wind"],
        "answer": "c",
    },
    {
        "id": "q4",
        "subject": "language",
        "text": "Which sentence is written correctly?",
        "options": [
            "a) She go to school every day.",
            "b) She goes to school every day.",
            "c) She going to school every day.",
            "d) She gone to school every day.",
        ],
        "answer": "b",
    },
    {
        "id": "q5",
        "subject": "geography",
        "text": "What do we call the large body of salt water that covers most of Earth?",
        "options": ["a) A river", "b) A lake", "c) An ocean", "d) A desert"],
        "answer": "c",
    },
]

_ANSWER_KEY = {q["id"]: q["answer"] for q in _QUESTIONS}

_DIAGNOSTIC_SYSTEM = (
    "You are SAGE's diagnostic agent. Analyse a student's 5-question placement "
    "test answers and produce a concise, encouraging knowledge profile. "
    "Be kind — this student may be a refugee or newcomer who lost access to school. "
    "Return ONLY the JSON object requested. No markdown, no extra text."
)


def _build_prompt(answers: dict[str, str], name: Optional[str]) -> str:
    name_line = f"Student name: {name}" if name else "Student: anonymous"
    rows = "\n".join(
        f"  {qid}: student='{ans}' correct='{_ANSWER_KEY.get(qid, '?')}'"
        for qid, ans in answers.items()
    )
    return f"""{name_line}

Answers vs correct key:
{rows}

Return exactly this JSON (no other text):
{{
  "knowledge_profile": "2-3 sentence description of what the student knows",
  "gaps": ["gap 1", "gap 2"],
  "recommended_start": "which lesson or unit to start with",
  "grade_estimate": "e.g. Grade 3",
  "encouragement": "a warm 1-sentence message for the student"
}}"""


async def _run_llm(answers: dict[str, str], name: Optional[str]) -> dict:
    prompt = _build_prompt(answers, name)
    raw = await asi1_complete(prompt=prompt, system=_DIAGNOSTIC_SYSTEM, max_tokens=512)
    raw = raw.strip()
    match = re.search(r"\{[\s\S]*\}", raw)
    if match:
        raw = match.group(0)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        log.warning("Diagnostic LLM returned non-JSON: %r", raw[:200])
        return {
            "knowledge_profile": "We could not fully analyse your answers at this time.",
            "gaps": [],
            "recommended_start": "Lesson 1 — Foundations",
            "grade_estimate": "Unknown",
            "encouragement": "You are brave for trying — keep going!",
        }


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class DiagnosticQuestion(BaseModel):
    id: str
    text: str
    options: list[str]
    subject: str


class DiagnosticSubmit(BaseModel):
    answers: dict[str, str]
    name: Optional[str] = Field(default=None, max_length=80)


class DiagnosticResult(BaseModel):
    knowledge_profile: str
    gaps: list[str]
    recommended_start: str
    grade_estimate: str
    encouragement: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.get("/questions", response_model=list[DiagnosticQuestion])
async def get_questions() -> list[DiagnosticQuestion]:
    """Return 5 placement questions. Answer key is NOT included in the response."""
    return [
        DiagnosticQuestion(id=q["id"], text=q["text"], options=q["options"], subject=q["subject"])
        for q in _QUESTIONS
    ]


@router.post("/submit", response_model=DiagnosticResult)
async def submit_diagnostic(req: DiagnosticSubmit) -> DiagnosticResult:
    """Anonymous submission — no account required."""
    if not req.answers:
        raise HTTPException(status_code=422, detail="answers must not be empty")
    data = await _run_llm(req.answers, req.name)
    return DiagnosticResult(**data)


@router.post("/submit-for-user", response_model=DiagnosticResult)
async def submit_diagnostic_for_user(
    req: DiagnosticSubmit,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DiagnosticResult:
    """Authenticated — same analysis, plus saves the profile to the user record."""
    if not req.answers:
        raise HTTPException(status_code=422, detail="answers must not be empty")

    data = await _run_llm(req.answers, req.name or user.display_name)

    current: dict = dict(user.accessibility_profile or {})
    current["diagnostic_profile"] = data
    user.accessibility_profile = current
    db.add(user)
    await db.commit()

    return DiagnosticResult(**data)
