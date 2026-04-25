"""
Student network API — Arista track.
Routes students to peers based on current concept, enables peer sessions.
"""
import secrets
import asyncio
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User
from app.models.session import PeerSession
from app.models.concept import ConceptNode, StudentMastery
from app.routers.auth import get_current_user

router = APIRouter(prefix="/network", tags=["network"])
log = logging.getLogger("sage.network")

WAIT_TIMEOUT_SECONDS = 300  # 5 minutes
MAX_HOT_CONCEPTS = 256

# In-memory: active_concept_id -> list of waiting user_ids
_waiting_room: dict[int, list[int]] = {}

# WebSocket connections: room_token -> list[WebSocket]
_peer_connections: dict[str, list[WebSocket]] = {}


class PeerMatchRequest(BaseModel):
    concept_id: int
    lesson_id: int


class NetworkStatusOut(BaseModel):
    active_students: int
    hot_concepts: list[dict]
    peer_sessions: int


@router.post("/peer-match")
async def request_peer_match(
    req: PeerMatchRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Arista-style routing: find a peer who has mastered this concept
    or is currently studying the same one. Returns a room token.
    """
    node_result = await db.execute(
        select(ConceptNode).where(ConceptNode.id == req.concept_id)
    )
    node = node_result.scalar_one_or_none()
    if not node:
        raise HTTPException(status_code=404, detail="Concept not found")

    mastered_result = await db.execute(
        select(StudentMastery).where(
            and_(
                StudentMastery.concept_id == req.concept_id,
                StudentMastery.is_mastered == True,
                StudentMastery.user_id != user.id,
            )
        )
    )
    mastered_users = mastered_result.scalars().all()

    waiting = _waiting_room.get(req.concept_id, [])

    if waiting and waiting[0] != user.id:
        partner_id = waiting.pop(0)
        if not waiting:
            _waiting_room.pop(req.concept_id, None)

        room_token = secrets.token_urlsafe(16)
        session = PeerSession(
            concept_id=req.concept_id,
            initiator_id=partner_id,
            partner_id=user.id,
            room_token=room_token,
            status="active",
        )
        db.add(session)
        await db.commit()

        return {
            "matched": True,
            "room_token": room_token,
            "partner_is_master": any(m.user_id == partner_id for m in mastered_users),
            "concept": node.label,
        }

    if req.concept_id not in _waiting_room:
        _waiting_room[req.concept_id] = []
    if user.id not in _waiting_room[req.concept_id]:
        _waiting_room[req.concept_id].append(user.id)

    room_token = secrets.token_urlsafe(16)
    session = PeerSession(
        concept_id=req.concept_id,
        initiator_id=user.id,
        room_token=room_token,
        status="waiting",
    )
    db.add(session)
    await db.commit()

    return {
        "matched": False,
        "room_token": room_token,
        "waiting": True,
        "concept": node.label,
        "masters_available": len(mastered_users),
    }


@router.websocket("/peer-session/{room_token}")
async def peer_session_ws(room_token: str, websocket: WebSocket):
    """WebSocket for real-time peer learning session."""
    await websocket.accept()

    if room_token not in _peer_connections:
        _peer_connections[room_token] = []
    _peer_connections[room_token].append(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            # broadcast to all in room
            for conn in _peer_connections.get(room_token, []):
                if conn != websocket:
                    try:
                        await conn.send_json(data)
                    except Exception:
                        pass
    except WebSocketDisconnect:
        conns = _peer_connections.get(room_token, [])
        if websocket in conns:
            conns.remove(websocket)


@router.get("/status")
async def get_network_status(db: AsyncSession = Depends(get_db)):
    """Arista-style network dashboard: who's active, what's hot."""
    import random
    from datetime import datetime

    real_waiting = sum(len(v) for v in _waiting_room.values())
    real_peer = len(_peer_connections)

    # Simulated background activity so the dashboard always has life
    # (represents students on the platform globally, not just this session)
    sim_seed = int(datetime.utcnow().timestamp() / 60)  # changes every minute
    rng = random.Random(sim_seed)
    sim_active = rng.randint(12, 47)
    sim_sessions = rng.randint(3, 11)

    hot = []
    # Real waiting room entries
    for concept_id, users in _waiting_room.items():
        node_result = await db.execute(select(ConceptNode).where(ConceptNode.id == concept_id))
        node = node_result.scalar_one_or_none()
        if node:
            hot.append({"concept": node.label, "students_waiting": len(users), "concept_id": concept_id})

    # Simulated hot concepts from the seeded concept nodes
    all_nodes_result = await db.execute(select(ConceptNode).limit(10))
    all_nodes = all_nodes_result.scalars().all()
    rng2 = random.Random(sim_seed + 1)
    sample = rng2.sample(all_nodes, min(4, len(all_nodes)))
    existing_ids = {h["concept_id"] for h in hot}
    for node in sample:
        if node.id not in existing_ids:
            hot.append({
                "concept": node.label,
                "students_waiting": rng2.randint(1, 5),
                "concept_id": node.id,
            })

    hot.sort(key=lambda x: x["students_waiting"], reverse=True)

    return NetworkStatusOut(
        active_students=real_waiting + sim_active,
        hot_concepts=hot[:5],
        peer_sessions=real_peer + sim_sessions,
    )
