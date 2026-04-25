"""Notes synthesis from session transcript and learner-provided notes.

`/notes/{id}`             - auto-summary view (markdown)
`/notes/{id}/revise`      - learner provides notes, gaps + suggestions returned
`/notes/{id}/study-plan`  - structured multi-section study plan markdown
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as OrmSession

from app.core.retrieval import tokenize
from app.db import get_db
from app.models import Concept, Lesson
from app.models import Session as TutorSession
from app.models import User
from app.schemas import NotesIn, NotesOut, StudyPlanOut
from app.security import get_current_user

router = APIRouter(prefix="/notes", tags=["notes"])


_STOP = {
    "the", "a", "an", "of", "to", "in", "is", "it", "and", "or", "for", "on",
    "with", "as", "by", "that", "this", "are", "be", "was", "were", "at",
    "from", "but", "if", "then", "so", "we", "you", "i", "they", "have", "has",
}


def _content_tokens(text: str) -> set[str]:
    return {t for t in tokenize(text) if t not in _STOP and len(t) > 2}


def _summarize_transcript(transcript: str) -> str:
    user_lines = [l[6:].strip() for l in (transcript or "").splitlines() if l.startswith("USER:")]
    sage_lines = [l[6:].strip() for l in (transcript or "").splitlines() if l.startswith("SAGE:")]
    if not user_lines:
        return "_No turns yet — start the conversation to populate notes._"
    bullets = [
        f"- **You asked:** {q}\n  - **SAGE replied:** {a[:240]}{'…' if len(a) > 240 else ''}"
        for q, a in zip(user_lines, sage_lines)
    ]
    return "\n".join(bullets)


def _gaps(student_text: str, lesson_text: str) -> list[str]:
    src_toks = _content_tokens(lesson_text)
    own_toks = _content_tokens(student_text)
    return sorted(src_toks - own_toks)[:10]


def _own_session(db: OrmSession, session_id: int, user: User) -> TutorSession:
    s = (
        db.query(TutorSession)
        .filter(TutorSession.id == session_id, TutorSession.user_id == user.id)
        .first()
    )
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    return s


@router.get("/{session_id}", response_model=NotesOut)
def get_notes(
    session_id: int,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    s = _own_session(db, session_id, user)
    md = _summarize_transcript(s.transcript or "")
    concepts = db.query(Concept).filter(Concept.session_id == s.id).all()
    weak = [c.label for c in concepts if (c.mastery or 0.0) < 0.5][:5]
    suggestions = (
        [f"Review: {label}" for label in weak]
        if weak
        else ["Try a deeper synthesis question to extend your understanding."]
    )
    return NotesOut(
        session_id=s.id,
        markdown=md,
        summary=(
            f"{len(concepts)} concept(s) tracked, "
            f"{sum(1 for c in concepts if (c.mastery or 0.0) >= 0.8)} mastered."
        ),
        gaps=[],
        suggestions=suggestions,
    )


@router.post("/{session_id}/revise", response_model=NotesOut)
def revise_notes(
    session_id: int,
    payload: NotesIn,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    s = _own_session(db, session_id, user)
    lesson = db.query(Lesson).filter(Lesson.id == s.lesson_id).first() if s.lesson_id else None
    lesson_text = lesson.objective if lesson else ""

    student = payload.text.strip()
    gaps = _gaps(student, lesson_text)

    revised_md = (
        f"### Your notes\n\n{student}\n\n---\n\n"
        f"### Suggested additions\n\n"
        + ("\n".join(f"- consider: **{w}**" for w in gaps) if gaps else "_Looks comprehensive._")
    )

    concepts = db.query(Concept).filter(Concept.session_id == s.id).all()
    weak = [c.label for c in concepts if (c.mastery or 0.0) < 0.5][:5]
    suggestions = (
        [f"Tighten your understanding of: {label}" for label in weak]
        if weak
        else ["Consolidate by teaching the topic to someone else."]
    )

    return NotesOut(
        session_id=s.id,
        markdown=revised_md,
        summary=f"You wrote {len(student.split())} words. {len(gaps)} suggested additions.",
        gaps=gaps,
        suggestions=suggestions,
    )


@router.post("/{session_id}/study-plan", response_model=StudyPlanOut)
def generate_study_plan(
    session_id: int,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    s = _own_session(db, session_id, user)
    lesson = db.query(Lesson).filter(Lesson.id == s.lesson_id).first() if s.lesson_id else None
    concepts = db.query(Concept).filter(Concept.session_id == s.id).all()

    weak = [c for c in concepts if (c.mastery or 0.0) < 0.5]
    medium = [c for c in concepts if 0.5 <= (c.mastery or 0.0) < 0.8]
    strong = [c for c in concepts if (c.mastery or 0.0) >= 0.8]

    lesson_title = lesson.title if lesson else f"Session {s.id}"
    when = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    weak_lines = [_concept_line(c) for c in weak] or ["_None right now — pick a stretch goal below._"]
    medium_lines = [_concept_line(c) for c in medium] or ["_Keep going._"]
    strong_lines = [_concept_line(c) for c in strong] or ["_Build mastery on the focus list first._"]

    md = "\n".join(
        [
            f"# Study plan — {lesson_title}",
            f"_Generated {when} · session {s.id}_",
            "",
            "## Goals",
            "- Bring all weak concepts to at least 50% mastery.",
            "- Move at least one medium concept to mastered.",
            "- Connect strong concepts into a synthesis explanation.",
            "",
            "## Focus this week (weak)",
            *weak_lines,
            "",
            "## Reinforce (medium)",
            *medium_lines,
            "",
            "## Stretch (strong)",
            *strong_lines,
            "",
            "## Suggested order",
            "1. Re-read the lesson objective and extract the 3 most surprising claims.",
            "2. For each weak concept, ask SAGE to scaffold from first principles.",
            "3. Take a short quiz (ask SAGE: \"quiz me on the concepts I'm weakest at\").",
            "4. Write a 5-sentence summary in the Notes panel and run \"Review with SAGE\".",
            "",
            "## Lesson recap",
            (lesson.objective if lesson else "_No lesson attached._"),
        ]
    )

    return StudyPlanOut(
        session_id=s.id,
        filename=f"sage-study-plan-session-{s.id}.md",
        markdown=md,
    )


def _concept_line(c: Concept) -> str:
    pct = round((c.mastery or 0.0) * 100)
    return f"- **{c.label}** ({pct}%) — {c.summary or 'open this concept and go deeper.'}"
