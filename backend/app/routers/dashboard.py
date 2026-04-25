"""
Course progress dashboard — per-user analytics.
Shows mastery by concept, session history, streak, time spent,
weak areas, and next recommended lessons.
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.database import get_db
from app.models.user import User
from app.models.lesson import Course, Lesson
from app.models.session import TutorSession, TutorMessage
from app.models.concept import ConceptNode, StudentMastery
from app.routers.auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview")
async def get_overview(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Full dashboard: mastery, sessions, weak areas, streaks, recommendations."""

    # Sessions in last 30 days
    thirty_ago = datetime.utcnow() - timedelta(days=30)
    sessions_result = await db.execute(
        select(TutorSession).where(
            and_(TutorSession.user_id == user.id, TutorSession.started_at >= thirty_ago)
        ).order_by(TutorSession.started_at.desc())
    )
    sessions = sessions_result.scalars().all()

    # Message count
    msg_count_result = await db.execute(
        select(func.count(TutorMessage.id)).join(
            TutorSession, TutorMessage.session_id == TutorSession.id
        ).where(TutorSession.user_id == user.id)
    )
    total_messages = msg_count_result.scalar() or 0

    # Mastery overview
    mastery_result = await db.execute(
        select(ConceptNode, StudentMastery)
        .join(StudentMastery, ConceptNode.id == StudentMastery.concept_id, isouter=True)
        .where(StudentMastery.user_id == user.id)
    )
    mastery_rows = mastery_result.all()

    mastered = [r for r in mastery_rows if r[1] and r[1].is_mastered]
    in_progress = [r for r in mastery_rows if r[1] and not r[1].is_mastered and r[1].score > 0]
    weak_areas = sorted(
        [r for r in mastery_rows if r[1] and r[1].score < 0.4 and r[1].attempts > 0],
        key=lambda r: r[1].score,
    )[:5]

    # Learning streak (consecutive days with sessions)
    streak = _calculate_streak(sessions)

    # Time spent (approx: avg 2 min per message)
    time_minutes = total_messages * 2

    # Verification fail rate (Cognition metric)
    fail_result = await db.execute(
        select(func.count(TutorMessage.id)).join(
            TutorSession, TutorMessage.session_id == TutorSession.id
        ).where(
            and_(
                TutorSession.user_id == user.id,
                TutorMessage.verification_passed == False,
                TutorMessage.role == "assistant",
            )
        )
    )
    verification_fails = fail_result.scalar() or 0

    # Courses enrolled (any sessions)
    courses_touched = set()
    for sess in sessions:
        lesson_result = await db.execute(select(Lesson).where(Lesson.id == sess.lesson_id))
        lesson = lesson_result.scalar_one_or_none()
        if lesson:
            courses_touched.add(lesson.course_id)

    all_courses_result = await db.execute(select(Course))
    all_courses = {c.id: c for c in all_courses_result.scalars().all()}

    return {
        "user": {
            "display_name": user.display_name,
            "subscription_tier": user.subscription_tier,
            "teaching_mode": user.teaching_mode,
            "member_since": user.created_at.isoformat(),
        },
        "stats": {
            "sessions_30d": len(sessions),
            "total_messages": total_messages,
            "time_spent_minutes": time_minutes,
            "streak_days": streak,
            "concepts_mastered": len(mastered),
            "concepts_in_progress": len(in_progress),
            "verification_fail_rate": (
                round(verification_fails / max(1, total_messages // 2), 3)
            ),
        },
        "mastery": {
            "mastered": [{"id": r[0].id, "label": r[0].label} for r in mastered],
            "in_progress": [
                {"id": r[0].id, "label": r[0].label, "score": round(r[1].score, 2)}
                for r in in_progress
            ],
            "weak_areas": [
                {
                    "id": r[0].id,
                    "label": r[0].label,
                    "score": round(r[1].score, 2),
                    "attempts": r[1].attempts,
                }
                for r in weak_areas
            ],
        },
        "recent_sessions": [
            {
                "id": s.id,
                "lesson_id": s.lesson_id,
                "started_at": s.started_at.isoformat(),
                "teaching_mode": s.teaching_mode,
            }
            for s in sessions[:5]
        ],
        "courses_active": [
            {"id": cid, "title": all_courses[cid].title}
            for cid in courses_touched
            if cid in all_courses
        ],
        "cognition_metrics": {
            "semantic_retrievals": total_messages,
            "verification_checks": total_messages // 2,
            "verification_pass_rate": round(
                1 - (verification_fails / max(1, total_messages // 2)), 3
            ),
        },
    }


@router.get("/course/{course_id}")
async def get_course_dashboard(
    course_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Per-course progress dashboard."""
    course_result = await db.execute(select(Course).where(Course.id == course_id))
    course = course_result.scalar_one_or_none()
    if not course:
        raise HTTPException(404, "Course not found")

    lessons_result = await db.execute(
        select(Lesson).where(Lesson.course_id == course_id).order_by(Lesson.order)
    )
    lessons = lessons_result.scalars().all()

    nodes_result = await db.execute(select(ConceptNode).where(ConceptNode.course_id == course_id))
    nodes = nodes_result.scalars().all()
    node_ids = [n.id for n in nodes]

    mastery_result = await db.execute(
        select(StudentMastery).where(
            and_(StudentMastery.user_id == user.id, StudentMastery.concept_id.in_(node_ids))
        )
    )
    mastery_map = {m.concept_id: m for m in mastery_result.scalars().all()}

    overall_mastery = 0.0
    if nodes:
        total_score = sum(mastery_map[n.id].score if n.id in mastery_map else 0.0 for n in nodes)
        overall_mastery = total_score / len(nodes)

    concept_breakdown = [
        {
            "id": n.id,
            "label": n.label,
            "score": round(mastery_map[n.id].score, 2) if n.id in mastery_map else 0.0,
            "is_mastered": mastery_map[n.id].is_mastered if n.id in mastery_map else False,
            "attempts": mastery_map[n.id].attempts if n.id in mastery_map else 0,
        }
        for n in nodes
    ]

    return {
        "course": {"id": course.id, "title": course.title, "level": course.level},
        "overall_mastery": round(overall_mastery, 3),
        "lessons": [
            {"id": l.id, "slug": l.slug, "title": l.title, "order": l.order}
            for l in lessons
        ],
        "concept_breakdown": concept_breakdown,
        "next_recommended": _recommend_next(concept_breakdown),
    }


def _calculate_streak(sessions: list) -> int:
    if not sessions:
        return 0
    dates = sorted(set(s.started_at.date() for s in sessions), reverse=True)
    streak = 0
    today = datetime.utcnow().date()
    for i, d in enumerate(dates):
        expected = today - timedelta(days=i)
        if d == expected:
            streak += 1
        else:
            break
    return streak


def _recommend_next(concepts: list[dict]) -> list[dict]:
    """Return 3 concepts to study next (lowest score, most attempts = struggle areas)."""
    struggling = [c for c in concepts if not c["is_mastered"] and c["attempts"] > 0]
    unstarted = [c for c in concepts if c["attempts"] == 0]
    struggling.sort(key=lambda c: c["score"])
    return (struggling + unstarted)[:3]
