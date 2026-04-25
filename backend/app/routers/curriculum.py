import json
import logging
import re
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
from ..models.curriculum import GeneratedCurriculum
from ..schemas.curriculum import (
    CurriculumGenerateRequest,
    CurriculumResponse,
    CurriculumSummaryResponse,
    PhaseResponse,
    LessonRef,
    GapResponse,
)
from ..agent.system_prompt_curriculum import build_curriculum_prompt
from ..config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/curriculum", tags=["curriculum"])

_async_client: AsyncOpenAI | None = None


def _safe_hours(val) -> float:
    """Coerce an LLM-returned hours value to float, handling strings like '4 hours 30 mins'."""
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        nums = re.findall(r"[\d.]+", val)
        return float(nums[0]) if nums else 0
    return 0


def _get_client() -> AsyncOpenAI:
    global _async_client
    if _async_client is None:
        settings = get_settings()
        _async_client = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
        )
    return _async_client


def _gather_full_catalog(session: Session) -> tuple[list[dict], dict[str, dict]]:
    """Return (courses_for_prompt, lesson_lookup) where lesson_lookup maps ID -> lesson info."""
    paths = session.exec(select(LearningPath)).all()
    courses: list[dict] = []
    lesson_lookup: dict[str, dict] = {}

    for path in paths:
        mods = session.exec(
            select(Module).where(Module.learning_path_id == path.id).order_by(Module.order_index)
        ).all()
        modules_out = []
        for mod in mods:
            lessons = session.exec(
                select(Lesson).where(Lesson.module_id == mod.id).order_by(Lesson.order_index)
            ).all()
            lessons_out = []
            for lesson in lessons:
                try:
                    concepts = json.loads(lesson.concepts) if lesson.concepts else []
                except (json.JSONDecodeError, TypeError):
                    concepts = []
                lesson_info = {
                    "id": lesson.id,
                    "title": lesson.title,
                    "summary": lesson.summary,
                    "concepts": concepts if isinstance(concepts, list) else [],
                }
                lessons_out.append(lesson_info)
                lesson_lookup[lesson.id] = {
                    **lesson_info,
                    "course_title": path.title,
                    "path_slug": path.slug,
                }
            modules_out.append({"title": mod.title, "lessons": lessons_out})
        courses.append({
            "path_title": path.title,
            "path_slug": path.slug,
            "modules": modules_out,
        })
    return courses, lesson_lookup


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


def _load_latest_assessment(user_id: str, session: Session) -> dict | None:
    assessment = session.exec(
        select(SkillAssessment)
        .where(SkillAssessment.user_id == user_id)
        .order_by(SkillAssessment.created_at.desc())
    ).first()
    if not assessment:
        return None

    def _parse(raw: str, default):
        try:
            return json.loads(raw)
        except Exception:
            return default

    return {
        "overall_level": assessment.overall_level,
        "skill_dimensions": _parse(assessment.skill_dimensions, []),
        "strengths": _parse(assessment.strengths, []),
        "gaps": _parse(assessment.gaps, []),
    }


def _curriculum_to_response(
    c: GeneratedCurriculum,
    lesson_lookup: dict[str, dict],
    completed_lessons: list[str],
) -> CurriculumResponse:
    def _parse(raw: str, default):
        try:
            return json.loads(raw)
        except Exception:
            return default

    raw_phases = _parse(c.phases, [])
    phases: list[PhaseResponse] = []
    for p in raw_phases:
        if not isinstance(p, dict):
            continue
        lesson_ids = p.get("lesson_ids", [])
        lessons = []
        for lid in lesson_ids:
            info = lesson_lookup.get(lid)
            if info:
                lessons.append(LessonRef(
                    id=lid,
                    title=info["title"],
                    summary=info.get("summary", ""),
                    course_title=info.get("course_title", ""),
                    path_slug=info.get("path_slug", ""),
                    completed=lid in completed_lessons,
                ))
        phases.append(PhaseResponse(
            order=p.get("order", 0),
            title=p.get("title", ""),
            level=p.get("level", "intermediate"),
            estimated_hours=_safe_hours(p.get("estimated_hours", 0)),
            description=p.get("description", ""),
            lessons=lessons,
            milestone_title=p.get("milestone_title", ""),
            milestone_skills=p.get("milestone_skills", []),
        ))

    raw_gaps = _parse(c.gaps, [])
    gaps = [
        GapResponse(
            topic=g.get("topic", ""),
            description=g.get("description", ""),
            explore_query=g.get("explore_query", g.get("topic", "")),
        )
        for g in raw_gaps
        if isinstance(g, dict)
    ]

    return CurriculumResponse(
        id=c.id,
        title=c.title,
        level_range=c.level_range,
        estimated_hours=c.estimated_hours,
        personalization_note=c.personalization_note,
        phases=phases,
        gaps=gaps,
        learning_goals=c.learning_goals,
        created_at=c.created_at,
    )


# ── POST /curriculum/generate ─────────────────────────────────────────────────

@router.post("/generate", response_model=CurriculumResponse)
async def generate_curriculum(
    req: CurriculumGenerateRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    courses, lesson_lookup = _gather_full_catalog(session)
    if not courses:
        raise HTTPException(status_code=400, detail="No courses available for curriculum generation")

    completed_lessons = _gather_completed_lessons(user.id, session)
    quiz_scores = _gather_quiz_scores(user.id, session)
    assessment = _load_latest_assessment(user.id, session)

    prompt = build_curriculum_prompt(
        courses=courses,
        completed_lessons=completed_lessons,
        quiz_scores=quiz_scores,
        assessment=assessment,
    )

    client = _get_client()
    settings = get_settings()

    try:
        response = await client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"My learning goals: {req.learning_goals}"},
            ],
            max_tokens=4096,
            temperature=0.7,
        )
    except Exception as e:
        logger.error("LLM curriculum generation failed: %s", e)
        raise HTTPException(status_code=502, detail="Curriculum generation failed. Please try again.")

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
        logger.error("Failed to parse curriculum JSON: %s", raw[:500])
        raise HTTPException(status_code=502, detail="Curriculum generation returned invalid format. Please try again.")

    # Validate lesson IDs in phases — strip any hallucinated ones
    valid_phases = data.get("phases", [])
    for phase in valid_phases:
        if isinstance(phase, dict) and "lesson_ids" in phase:
            phase["lesson_ids"] = [lid for lid in phase["lesson_ids"] if lid in lesson_lookup]

    curriculum = GeneratedCurriculum(
        user_id=user.id,
        learning_goals=req.learning_goals,
        title=data.get("title", "Personalized Curriculum"),
        level_range=data.get("level_range", ""),
        estimated_hours=_safe_hours(data.get("estimated_hours", 0)),
        personalization_note=data.get("personalization_note", ""),
        phases=json.dumps(valid_phases),
        gaps=json.dumps(data.get("gaps", [])),
    )
    session.add(curriculum)
    session.commit()
    session.refresh(curriculum)

    return _curriculum_to_response(curriculum, lesson_lookup, completed_lessons)


# ── GET /curriculum/latest ────────────────────────────────────────────────────

@router.get("/latest", response_model=CurriculumResponse)
async def get_latest_curriculum(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    curriculum = session.exec(
        select(GeneratedCurriculum)
        .where(GeneratedCurriculum.user_id == user.id)
        .order_by(GeneratedCurriculum.created_at.desc())
    ).first()
    if not curriculum:
        raise HTTPException(status_code=404, detail="No curriculum found")

    _, lesson_lookup = _gather_full_catalog(session)
    completed_lessons = _gather_completed_lessons(user.id, session)
    return _curriculum_to_response(curriculum, lesson_lookup, completed_lessons)


# ── GET /curriculum/history ───────────────────────────────────────────────────

@router.get("/history", response_model=List[CurriculumSummaryResponse])
async def get_curriculum_history(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    curricula = session.exec(
        select(GeneratedCurriculum)
        .where(GeneratedCurriculum.user_id == user.id)
        .order_by(GeneratedCurriculum.created_at.desc())
    ).all()
    return [
        CurriculumSummaryResponse(
            id=c.id,
            title=c.title,
            level_range=c.level_range,
            created_at=c.created_at,
        )
        for c in curricula
    ]
