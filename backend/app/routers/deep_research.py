"""Deep Research endpoints.

  POST   /deep-research/runs                      → start a run, returns run_id
  GET    /deep-research/runs/{run_id}             → snapshot of state
  GET    /deep-research/runs/{run_id}/stream      → SSE event stream
  POST   /deep-research/runs/{run_id}/outreach    → send a SendGrid email
  GET    /deep-research/runs                      → user's run history
"""
from __future__ import annotations

import json
from datetime import datetime
from typing import AsyncIterator, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlmodel import Session, select

from ..db import get_session
from ..deps import get_current_user
from ..models.deep_research import OutreachLog, ResearchRun
from ..models.user import User
from ..services.deep_research.orchestrator import (
    get_orchestrator,
    serialize_event,
)

router = APIRouter(prefix="/deep-research", tags=["deep-research"])


# ───────────── Schemas ─────────────


class StartRunPayload(BaseModel):
    topic: str
    depth: int = 2
    max_papers: int = 25


class StartRunResponse(BaseModel):
    run_id: str
    topic: str


class RunSummary(BaseModel):
    id: str
    topic: str
    status: str
    created_at: datetime


class RunDetail(BaseModel):
    id: str
    topic: str
    status: str
    graph: Optional[dict] = None
    validation: Optional[dict] = None
    experts: List[dict] = []
    created_at: datetime
    updated_at: datetime


class OutreachPayload(BaseModel):
    expert_id: str
    subject: str
    body: str


# ───────────── Endpoints ─────────────


@router.post("/runs", response_model=StartRunResponse)
async def start_run(
    payload: StartRunPayload,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    if not payload.topic.strip():
        raise HTTPException(status_code=400, detail="topic is required")

    orch = get_orchestrator()
    run_id = orch.start_run(
        topic=payload.topic.strip(),
        depth=payload.depth,
        max_papers=payload.max_papers,
    )

    db_run = ResearchRun(
        id=run_id,
        user_id=user.id,
        topic=payload.topic.strip(),
        status="running",
    )
    session.add(db_run)
    session.commit()

    return StartRunResponse(run_id=run_id, topic=payload.topic.strip())


@router.get("/runs", response_model=List[RunSummary])
def list_runs(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    rows = session.exec(
        select(ResearchRun)
        .where(ResearchRun.user_id == user.id)
        .order_by(ResearchRun.created_at.desc())
    ).all()
    return [
        RunSummary(id=r.id, topic=r.topic, status=r.status, created_at=r.created_at)
        for r in rows
    ]


@router.get("/runs/{run_id}", response_model=RunDetail)
def get_run(
    run_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    db_run = session.get(ResearchRun, run_id)
    if not db_run or db_run.user_id != user.id:
        raise HTTPException(status_code=404, detail="run not found")

    # Prefer in-memory live state when available, else DB snapshot
    orch = get_orchestrator()
    state = orch.runs.get(run_id)

    graph = (
        state.graph.model_dump() if state and state.graph.nodes
        else (json.loads(db_run.graph_json) if db_run.graph_json else None)
    )
    validation = (
        state.validation if state and state.validation
        else (json.loads(db_run.validation_json) if db_run.validation_json else None)
    )
    experts = (
        [e.model_dump() for e in state.experts]
        if state and state.experts
        else (json.loads(db_run.experts_json) if db_run.experts_json else [])
    )

    return RunDetail(
        id=db_run.id,
        topic=db_run.topic,
        status=db_run.status,
        graph=graph,
        validation=validation,
        experts=experts,
        created_at=db_run.created_at,
        updated_at=db_run.updated_at,
    )


@router.get("/runs/{run_id}/stream")
async def stream_run(
    run_id: str,
    request: Request,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Server-Sent Events stream of agent activity for a run."""
    db_run = session.get(ResearchRun, run_id)
    if not db_run or db_run.user_id != user.id:
        raise HTTPException(status_code=404, detail="run not found")

    orch = get_orchestrator()
    state = orch.runs.get(run_id)
    if not state:
        # Run finished before subscribe — replay summary from DB and close.
        async def replay() -> AsyncIterator[bytes]:
            from ..services.deep_research.protocol import StreamEvent

            ev = StreamEvent(
                agent="orchestrator",
                kind="phase",
                payload={"phase": "done", "from_db": True},
            )
            yield serialize_event(ev).encode()

        return StreamingResponse(replay(), media_type="text/event-stream")

    async def event_gen() -> AsyncIterator[bytes]:
        while True:
            if await request.is_disconnected():
                break
            event = await state.queue.get()
            if event is None:  # sentinel — pipeline finished
                # Persist final snapshot to DB
                db_run.graph_json = json.dumps(state.graph.model_dump())
                if state.validation:
                    db_run.validation_json = json.dumps(state.validation)
                if state.experts:
                    db_run.experts_json = json.dumps(
                        [e.model_dump() for e in state.experts]
                    )
                db_run.status = "ready_for_outreach" if state.experts else "done"
                db_run.updated_at = datetime.utcnow()
                session.add(db_run)
                session.commit()
                break
            yield serialize_event(event).encode()

    return StreamingResponse(
        event_gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/runs/{run_id}/outreach")
async def send_outreach(
    run_id: str,
    payload: OutreachPayload,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    db_run = session.get(ResearchRun, run_id)
    if not db_run or db_run.user_id != user.id:
        raise HTTPException(status_code=404, detail="run not found")

    orch = get_orchestrator()
    state = orch.runs.get(run_id)
    expert = None
    if state:
        expert = next((e for e in state.experts if e.id == payload.expert_id), None)
    if not expert and db_run.experts_json:
        try:
            for e in json.loads(db_run.experts_json):
                if e.get("id") == payload.expert_id:
                    from ..services.deep_research.protocol import ExpertProfile

                    expert = ExpertProfile.model_validate(e)
                    break
        except Exception:
            pass
    if not expert:
        raise HTTPException(status_code=404, detail="expert not found in run")

    if not expert.email:
        raise HTTPException(status_code=400, detail="No email available for this expert")

    result = await orch.send_outreach(
        run_id=run_id,
        expert_id=payload.expert_id,
        subject=payload.subject,
        body=payload.body,
    )

    log = OutreachLog(
        run_id=run_id,
        expert_id=payload.expert_id,
        expert_name=expert.name,
        expert_email=expert.email or "",
        subject=payload.subject,
        body=payload.body,
        sent=bool(result.get("sent")),
        status_code=result.get("status_code"),
        error=result.get("error"),
    )
    session.add(log)
    session.commit()

    return result
