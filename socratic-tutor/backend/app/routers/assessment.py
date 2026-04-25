import json
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from openai import AsyncOpenAI
from sqlmodel import Session, select

from ..db import get_session
from ..deps import get_current_user
from ..models.user import User
from ..models.learning import LearningPath, Module, Lesson
from ..models.progress import UserLessonProgress
from ..models.quiz import QuizSession
from ..models.assessment import SkillAssessment
from ..schemas.assessment import (
    AssessRequest,
    AssessmentResponse,
    AssessmentSummaryResponse,
    SkillDimensionResponse,
)
from ..agent.system_prompt_assessment import build_assessment_prompt
from ..config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/assess", tags=["assessment"])

_async_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _async_client
    if _async_client is None:
        settings = get_settings()
        _async_client = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
        )
    return _async_client


def _assessment_to_response(a: SkillAssessment) -> AssessmentResponse:
    def _parse(raw: str, default):
        try:
            return json.loads(raw)
        except Exception:
            return default

    dims_raw = _parse(a.skill_dimensions, [])
    dims = [
        SkillDimensionResponse(
            name=d.get("name", ""),
            level=d.get("level", "beginner"),
            score=d.get("score", 0),
            max_score=d.get("max_score", 10),
            description=d.get("description", ""),
        )
        for d in dims_raw
        if isinstance(d, dict)
    ]

    return AssessmentResponse(
        id=a.id,
        overall_level=a.overall_level,
        overall_summary=a.overall_summary,
        skill_dimensions=dims,
        strengths=_parse(a.strengths, []),
        gaps=_parse(a.gaps, []),
        recommended_module_id=a.recommended_module_id,
        recommendation_text=a.recommendation_text,
        background_text=a.background_text,
        created_at=a.created_at,
    )


def _gather_curriculum(session: Session) -> list[dict]:
    """Build a flat list of module dicts with their lessons."""
    paths = session.exec(select(LearningPath)).all()
    modules_out: list[dict] = []
    for path in paths:
        mods = session.exec(
            select(Module)
            .where(Module.learning_path_id == path.id)
            .order_by(Module.order_index)
        ).all()
        for mod in mods:
            lessons = session.exec(
                select(Lesson)
                .where(Lesson.module_id == mod.id)
                .order_by(Lesson.order_index)
            ).all()
            modules_out.append({
                "id": mod.id,
                "title": mod.title,
                "lessons": [{"id": l.id, "title": l.title} for l in lessons],
            })
    return modules_out


def _gather_completed_lessons(user_id: str, session: Session) -> list[str]:
    rows = session.exec(
        select(UserLessonProgress)
        .where(UserLessonProgress.user_id == user_id)
        .where(UserLessonProgress.completed == True)
    ).all()
    return [r.lesson_id for r in rows]


def _gather_quiz_scores(user_id: str, session: Session) -> list[dict]:
    quizzes = session.exec(
        select(QuizSession)
        .where(QuizSession.user_id == user_id)
        .where(QuizSession.completed == True)
    ).all()
    return [
        {
            "topic": q.topic,
            "correct": q.correct_count,
            "total": q.total_questions,
            "difficulty": q.difficulty,
        }
        for q in quizzes
    ]


# ── POST /assess ──────────────────────────────────────────────────────────────

@router.post("", response_model=AssessmentResponse)
async def create_assessment(
    req: AssessRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    modules = _gather_curriculum(session)
    if not modules:
        raise HTTPException(status_code=400, detail="No curriculum available for assessment")

    completed_lessons = _gather_completed_lessons(user.id, session)
    quiz_scores = _gather_quiz_scores(user.id, session)

    prompt = build_assessment_prompt(
        modules=modules,
        completed_lessons=completed_lessons,
        quiz_scores=quiz_scores,
    )

    client = _get_client()
    settings = get_settings()

    try:
        response = await client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"My background: {req.background_text}"},
            ],
            max_tokens=4096,
            temperature=0.7,
        )
    except Exception as e:
        logger.error("LLM assessment generation failed: %s", e)
        raise HTTPException(status_code=502, detail="Assessment generation failed. Please try again.")

    raw = (response.choices[0].message.content or "").strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        logger.error("Failed to parse assessment JSON: %s", raw[:500])
        raise HTTPException(status_code=502, detail="Assessment returned invalid format. Please try again.")

    # Resolve recommended module ID from title
    recommended_module_id = None
    rec_title = data.get("recommended_module_title", "")
    if rec_title:
        for mod in modules:
            if mod["title"].lower() == rec_title.lower():
                recommended_module_id = mod["id"]
                break

    assessment = SkillAssessment(
        user_id=user.id,
        background_text=req.background_text,
        overall_level=data.get("overall_level", "beginner"),
        overall_summary=data.get("overall_summary", ""),
        skill_dimensions=json.dumps(data.get("skill_dimensions", [])),
        strengths=json.dumps(data.get("strengths", [])),
        gaps=json.dumps(data.get("gaps", [])),
        recommended_module_id=recommended_module_id,
        recommendation_text=data.get("recommendation_text", ""),
    )
    session.add(assessment)
    session.commit()
    session.refresh(assessment)

    return _assessment_to_response(assessment)


# ── GET /assess/latest ────────────────────────────────────────────────────────

@router.get("/latest", response_model=AssessmentResponse)
async def get_latest_assessment(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    assessment = session.exec(
        select(SkillAssessment)
        .where(SkillAssessment.user_id == user.id)
        .order_by(SkillAssessment.created_at.desc())
    ).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="No assessment found")
    return _assessment_to_response(assessment)


# ── GET /assess/history ───────────────────────────────────────────────────────

@router.get("/history", response_model=List[AssessmentSummaryResponse])
async def get_assessment_history(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    assessments = session.exec(
        select(SkillAssessment)
        .where(SkillAssessment.user_id == user.id)
        .order_by(SkillAssessment.created_at.desc())
    ).all()
    return [
        AssessmentSummaryResponse(
            id=a.id,
            overall_level=a.overall_level,
            created_at=a.created_at,
        )
        for a in assessments
    ]
