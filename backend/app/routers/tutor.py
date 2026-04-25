import asyncio
import json
from typing import AsyncIterator

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as OrmSession
from sse_starlette.sse import EventSourceResponse

from app.core.prompt_builder import A11yProfile, ConceptMastery, build_system_prompt
from app.core.retrieval import CosineRetriever, Document
from app.core.verification import verify
from app.db import get_db
from app.models import Concept, Lesson
from app.models import Session as TutorSession
from app.models import User
from app.routers.accessibility import _PREFS as A11Y_STORE
from app.agents.base import AgentContext
from app.agents.orchestrator import Orchestrator
from app.schemas import SessionCreate, SessionOut, TutorReply, TutorTurn
from app.security import get_current_user

router = APIRouter(prefix="/tutor", tags=["tutor"])


@router.post("/sessions", response_model=SessionOut, status_code=201)
def start_session(
    payload: SessionCreate,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    s = TutorSession(user_id=user.id, lesson_id=payload.lesson_id)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@router.get("/sessions", response_model=list[SessionOut])
def list_sessions(db: OrmSession = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(TutorSession).filter(TutorSession.user_id == user.id).all()


@router.post("/turn", response_model=TutorReply)
def take_turn(
    turn: TutorTurn,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    s = db.query(TutorSession).filter(
        TutorSession.id == turn.session_id, TutorSession.user_id == user.id
    ).first()
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    s.transcript = (s.transcript or "") + f"\nUSER: {turn.message}"
    db.commit()
    return TutorReply(agent="socratic", reply="(stub) What do you already know about this?")


def _load_a11y(user_id: int) -> A11yProfile:
    p = A11Y_STORE.get(user_id)
    if not p:
        return A11yProfile()
    return A11yProfile(
        dyslexia_font=p.dyslexia_font,
        high_contrast=p.high_contrast,
        reduce_motion=p.reduce_motion,
        tts_voice=p.tts_voice,
    )


def _load_mastery(db: OrmSession, session_id: int) -> list[ConceptMastery]:
    rows = db.query(Concept).filter(Concept.session_id == session_id).all()
    return [ConceptMastery(label=c.label, mastery=c.mastery) for c in rows]


def _load_sources(db: OrmSession, lesson_id: int | None) -> list[str]:
    if not lesson_id:
        return []
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        return []
    return [s.strip() for s in (lesson.objective or "").split("\n\n") if s.strip()]


async def _stream_tokens(text: str, delay: float = 0.02) -> AsyncIterator[str]:
    for tok in text.split(" "):
        await asyncio.sleep(delay)
        yield tok + " "


def _sse(event: str, data: dict) -> dict:
    return {"event": event, "data": json.dumps(data)}


@router.get("/chat")
async def chat(
    session_id: int,
    message: str,
    db: OrmSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """SSE pipeline. Emits: agent_event, token, verification, done."""
    s = db.query(TutorSession).filter(TutorSession.id == session_id).first()
    if not s:
        # Auto-create session for frictionless demo
        s = TutorSession(id=session_id, user_id=user.id)
        db.add(s)
        db.commit()
        db.refresh(s)

    a11y = _load_a11y(user.id)
    mastery = _load_mastery(db, session_id)
    raw_sources = _load_sources(db, s.lesson_id)

    retriever = CosineRetriever()
    if raw_sources:
        retriever.add(Document(id=f"src-{i}", text=t) for i, t in enumerate(raw_sources))
    hits = retriever.search(message, k=4)
    sources = [h.doc.text for h in hits]

    lesson = db.query(Lesson).filter(Lesson.id == s.lesson_id).first() if s.lesson_id else None
    system_prompt = build_system_prompt(
        a11y=a11y,
        mastery=mastery,
        sources=sources,
        objective=lesson.objective if lesson else None,
    )

    # Build initial context
    ctx = AgentContext(
        session_id=session_id,
        user_id=user.id,
        user_message=message,
        a11y=a11y.__dict__,
        mastery=[{"label": m.label, "mastery": m.mastery} for m in mastery],
        sources=sources,
        plan={
            "strategy": "socratic",
            "depth": 1,
            "ask_one_question": True,
            "weak_concepts": [],
            "expert_teacher_mode": True,
        }
    )

    # Use Orchestrator to stream the turn
    orchestrator = Orchestrator()

    async def gen():
        buf = ""
        # 1. Stream the background agent events
        async for event, payload in orchestrator.stream_turn(ctx):
            if event == "done":
                # Final save to DB
                s.transcript = (s.transcript or "") + f"\nUSER: {message}\nSAGE: {ctx.answer.strip()}"
                db.commit()
                yield _sse("done", payload)
            elif event == "token":
                # This should not happen yet as Orchestrator.stream_turn doesn't stream tokens yet
                # Wait, orchestrator.stream_turn doesn't yield 'token' events.
                # I should probably update stream_turn to stream tokens from the content agent.
                pass
            else:
                yield _sse(event, payload)
        
        # 2. Stream the final answer
        async for tok in _stream_tokens(ctx.answer):
            yield _sse("token", {"agent": "socratic", "text": tok})
            
    return EventSourceResponse(gen())
