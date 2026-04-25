"""Tutor — sessions + Socratic streaming chat.

Live chat uses the 6-agent Orchestrator. SSE event sequence per turn:

    agent_event { agent="orchestrator", phase="start" }
    agent_event { agent="retriever",    phase="retrieved", k, scores }
    agent_event { agent="pedagogy",     phase="done",      plan }
    agent_event { agent="content",      phase="generating" }
    agent_event { agent="content",      phase="done",      chars }
    token       { agent="socratic",     text }                (repeated)
    verification { score, grounded, claims }
    agent_event { agent="concept_map",  phase="done", delta }
    agent_event { agent="assessment",   phase="done", data }
    agent_event { agent="peer_match",   phase="done", peers }
    agent_event { agent="progress",     phase="done", delta }
    done         { session_id, ok, grounded }

Concept map deltas are persisted as Concept rows on the session, and mastery
deltas from the Progress agent are applied to those rows so the UI map is
always live.
"""

from __future__ import annotations

import asyncio
import json
from typing import AsyncIterator

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as OrmSession
from sse_starlette.sse import EventSourceResponse

from app.agents.base import AgentContext
from app.agents.orchestrator import Orchestrator
from app.core.retrieval import CosineRetriever, Document
from app.core.verification import verify
from app.db import get_db
from app.models import Concept, Lesson
from app.models import Session as TutorSession
from app.models import User
from app.routers.accessibility import _PREFS as A11Y_STORE
from app.schemas import SessionCreate, SessionOut, TutorReply, TutorTurn
from app.security import get_current_user

router = APIRouter(prefix="/tutor", tags=["tutor"])


_ORCHESTRATOR = Orchestrator()


# ----- Sessions -----------------------------------------------------------


@router.post("/sessions", response_model=SessionOut, status_code=201)
def start_session(
    payload: SessionCreate,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if payload.lesson_id is not None:
        if not db.query(Lesson).filter(Lesson.id == payload.lesson_id).first():
            raise HTTPException(status_code=404, detail="Lesson not found")
    s = TutorSession(user_id=user.id, lesson_id=payload.lesson_id)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@router.get("/sessions", response_model=list[SessionOut])
def list_sessions(db: OrmSession = Depends(get_db), user: User = Depends(get_current_user)):
    return (
        db.query(TutorSession)
        .filter(TutorSession.user_id == user.id)
        .order_by(TutorSession.started_at.desc())
        .all()
    )


# ----- Non-streaming turn (legacy / fallback) -----------------------------


@router.post("/turn", response_model=TutorReply)
def take_turn(
    turn: TutorTurn,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    s = (
        db.query(TutorSession)
        .filter(TutorSession.id == turn.session_id, TutorSession.user_id == user.id)
        .first()
    )
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    s.transcript = (s.transcript or "") + f"\nUSER: {turn.message}"
    db.commit()
    return TutorReply(agent="socratic", reply="(stub) What do you already know about this?")


# ----- Helpers ------------------------------------------------------------


def _load_a11y(user_id: int) -> dict:
    p = A11Y_STORE.get(user_id)
    if not p:
        return {}
    return {
        "dyslexia_font": p.dyslexia_font,
        "high_contrast": p.high_contrast,
        "reduce_motion": p.reduce_motion,
        "tts_voice": p.tts_voice,
    }


def _load_mastery(db: OrmSession, session_id: int) -> list[dict]:
    rows = db.query(Concept).filter(Concept.session_id == session_id).all()
    return [{"label": c.label, "mastery": c.mastery or 0.0} for c in rows]


def _load_sources(db: OrmSession, lesson_id: int | None) -> list[str]:
    if not lesson_id:
        return []
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        return []
    return [s.strip() for s in (lesson.objective or "").split("\n\n") if s.strip()]


async def _stream_tokens(text: str, delay: float = 0.02) -> AsyncIterator[str]:
    if not text:
        return
    parts = text.split(" ")
    for i, tok in enumerate(parts):
        await asyncio.sleep(delay)
        yield (tok + (" " if i < len(parts) - 1 else ""))


def _sse(event: str, data: dict) -> dict:
    return {"event": event, "data": json.dumps(data)}


def _persist_concepts(db: OrmSession, session_id: int, delta: list[dict]) -> None:
    if not delta:
        return
    existing = {c.label for c in db.query(Concept).filter(Concept.session_id == session_id).all()}
    for d in delta:
        label = d.get("label", "").strip()
        if not label or label in existing:
            continue
        db.add(
            Concept(
                session_id=session_id,
                label=label,
                summary=d.get("summary", ""),
                mastery=float(d.get("mastery", 0.1)),
            )
        )
    db.commit()


def _apply_mastery_delta(db: OrmSession, session_id: int, by_concept: dict[str, float]) -> None:
    if not by_concept:
        return
    rows = db.query(Concept).filter(Concept.session_id == session_id).all()
    for c in rows:
        if c.label in by_concept:
            c.mastery = max(0.0, min(1.0, (c.mastery or 0.0) + float(by_concept[c.label])))
    db.commit()


# ----- Streaming chat ------------------------------------------------------


@router.get("/chat")
async def chat(
    session_id: int,
    message: str,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    s = (
        db.query(TutorSession)
        .filter(TutorSession.id == session_id, TutorSession.user_id == user.id)
        .first()
    )
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    if not message or len(message) > 4000:
        raise HTTPException(status_code=400, detail="Message empty or too long")

    a11y = _load_a11y(user.id)
    mastery = _load_mastery(db, session_id)
    raw_sources = _load_sources(db, s.lesson_id)

    # Retrieve top-k chunks deterministically.
    retriever = CosineRetriever()
    if raw_sources:
        retriever.add(Document(id=f"src-{i}", text=t) for i, t in enumerate(raw_sources))
    hits = retriever.search(message, k=4)
    sources = [h.doc.text for h in hits] or raw_sources[:4]
    scores = [round(h.score, 3) for h in hits]

    ctx = AgentContext(
        session_id=s.id,
        user_id=user.id,
        user_message=message,
        a11y=a11y,
        mastery=mastery,
        sources=sources,
        retrieved=[{"id": h.doc.id, "score": round(h.score, 3)} for h in hits],
    )

    orch = _ORCHESTRATOR

    async def gen():
        try:
            yield _sse("agent_event", {"agent": "orchestrator", "phase": "start", "session_id": s.id})
            yield _sse(
                "agent_event",
                {"agent": "retriever", "phase": "retrieved", "k": len(hits), "scores": scores},
            )

            await orch._run_agent(orch.pedagogy, ctx)
            yield _sse("agent_event", {"agent": "pedagogy", "phase": "done", "plan": ctx.plan})

            yield _sse("agent_event", {"agent": "content", "phase": "generating"})
            await orch._run_agent(orch.content, ctx)
            yield _sse(
                "agent_event",
                {"agent": "content", "phase": "done", "chars": len(ctx.answer)},
            )

            answer = ctx.answer or "I don't have enough source material to answer confidently."
            async for tok in _stream_tokens(answer):
                yield _sse("token", {"agent": "socratic", "text": tok})

            ctx.verification = verify(answer, ctx.sources).to_payload()
            yield _sse("verification", ctx.verification)

            await orch._run_agent(orch.concept_map, ctx)
            _persist_concepts(db, s.id, ctx.concept_map_delta)
            yield _sse(
                "agent_event",
                {"agent": "concept_map", "phase": "done", "delta": ctx.concept_map_delta},
            )

            await asyncio.gather(
                orch._run_agent(orch.assessment, ctx),
                orch._run_agent(orch.peer_match, ctx),
                orch._run_agent(orch.progress, ctx),
            )
            _apply_mastery_delta(db, s.id, ctx.progress_delta.get("by_concept", {}))

            yield _sse(
                "agent_event",
                {"agent": "assessment", "phase": "done", "data": ctx.assessment},
            )
            yield _sse(
                "agent_event",
                {"agent": "peer_match", "phase": "done", "peers": ctx.peers},
            )
            yield _sse(
                "agent_event",
                {"agent": "progress", "phase": "done", "delta": ctx.progress_delta},
            )

            s.transcript = (s.transcript or "") + f"\nUSER: {message}\nSAGE: {answer.strip()}"
            db.commit()

            yield _sse(
                "done",
                {
                    "session_id": s.id,
                    "ok": True,
                    "grounded": bool(ctx.verification.get("grounded", False)),
                },
            )
        except Exception as e:  # surface as SSE error rather than HTTP 500
            yield _sse("error", {"message": str(e)})

    return EventSourceResponse(gen())
