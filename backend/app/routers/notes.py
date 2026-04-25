"""Notes synthesis from session transcript and learner-provided notes.

Build a study summary deterministically from the session transcript so the
notes panel works without any LLM key. When learner provides their own notes,
detect concept gaps by comparing tokens against the lesson sources.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as OrmSession

from app.core.retrieval import tokenize
from app.db import get_db
from app.models import Concept, Lesson
from app.models import Session as TutorSession
from app.models import User
from app.schemas import NotesIn, NotesOut
from app.security import get_current_user

router = APIRouter(prefix="/notes", tags=["notes"])


_STOP = {
    "the", "a", "an", "of", "to", "in", "is", "it", "and", "or", "for", "on",
    "with", "as", "by", "that", "this", "are", "be", "was", "were", "at",
    "from", "but", "if", "then", "so", "we", "you", "i", "they", "have", "has",
}


def _content_tokens(text: str) -> set[str]:
    return {t for t in tokenize(text) if t not in _STOP and len(t) > 2}


def _summarize_transcript(transcript: str) -> tuple[str, list[str]]:
    """Return a markdown summary and bullet list extracted from the transcript."""
    user_lines = [l[6:].strip() for l in (transcript or "").splitlines() if l.startswith("USER:")]
    sage_lines = [l[6:].strip() for l in (transcript or "").splitlines() if l.startswith("SAGE:")]
    bullets = [f"- **You asked:** {q}\n  - **SAGE replied:** {a[:240]}{'…' if len(a) > 240 else ''}"
               for q, a in zip(user_lines, sage_lines)]
    md = "\n".join(bullets) if bullets else "_No turns yet — start the conversation to populate notes._"
    return md, bullets


def _gaps(student_text: str, lesson_text: str) -> list[str]:
    src_toks = _content_tokens(lesson_text)
    own_toks = _content_tokens(student_text)
    missing = sorted(src_toks - own_toks)
    return missing[:10]


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
    md, _ = _summarize_transcript(s.transcript or "")
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
        summary=f"{len(concepts)} concept(s) tracked, {sum(1 for c in concepts if (c.mastery or 0.0) >= 0.8)} mastered.",
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
