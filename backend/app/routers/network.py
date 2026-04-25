"""
Student network API — Arista track.
Routes students to peers using SAGE Routing Protocol (SRP).
No simulated/fake data — all metrics are real.
"""
import logging
import secrets
import time
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User
from app.models.session import PeerSession
from app.models.concept import ConceptNode, StudentMastery
from app.models.peer import PeerMessage, PeerSessionRating  # noqa: F401
from app.routers.auth import get_current_user

router = APIRouter(prefix="/network", tags=["network"])
log = logging.getLogger("sage.network")

WAIT_TIMEOUT_SECONDS = 300  # 5 minutes
MAX_HOT_CONCEPTS = 256

# In-memory: concept_id -> list of (user_id, entered_at_timestamp)
_waiting_room: dict[int, list[tuple[int, float]]] = {}

# WebSocket connections: room_token -> list[WebSocket]
_peer_connections: dict[str, list[WebSocket]] = {}


def _cleanup_waiting_room() -> None:
    """Remove waiters who have exceeded WAIT_TIMEOUT_SECONDS."""
    now = time.monotonic()
    expired_concepts = []
    for concept_id, waiters in _waiting_room.items():
        _waiting_room[concept_id] = [
            (uid, ts) for uid, ts in waiters
            if now - ts < WAIT_TIMEOUT_SECONDS
        ]
        if not _waiting_room[concept_id]:
            expired_concepts.append(concept_id)
    for concept_id in expired_concepts:
        del _waiting_room[concept_id]


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
    SRP-powered peer routing: scores candidates on 4 factors (mastery_delta,
    recency, style_compat, novelty) with BFS concept graph fallback.
    Returns a room token and full SRP score breakdown.
    """
    _cleanup_waiting_room()

    node_result = await db.execute(
        select(ConceptNode).where(ConceptNode.id == req.concept_id)
    )
    node = node_result.scalar_one_or_none()
    if not node:
        raise HTTPException(status_code=404, detail="Concept not found")

    # Get student's own mastery on this concept
    student_mastery_result = await db.execute(
        select(StudentMastery).where(
            and_(
                StudentMastery.user_id == user.id,
                StudentMastery.concept_id == req.concept_id,
            )
        )
    )
    student_mastery_row = student_mastery_result.scalar_one_or_none()
    student_mastery = student_mastery_row.score if student_mastery_row else 0.0

    # Build match history for novelty scoring
    history_result = await db.execute(
        select(PeerSession).where(
            and_(
                PeerSession.initiator_id == user.id,
                PeerSession.status == "completed",
            )
        )
    )
    past_sessions = history_result.scalars().all()
    match_history: dict[int, int] = {}
    for s in past_sessions:
        if s.partner_id:
            match_history[s.partner_id] = match_history.get(s.partner_id, 0) + 1

    # Run SRP
    from app.core.srp import find_peers_srp
    srp_result = await find_peers_srp(
        db=db,
        concept_id=req.concept_id,
        requesting_user_id=user.id,
        requesting_mastery=student_mastery,
        requesting_teaching_mode=getattr(user, "teaching_mode", None),
        match_history=match_history,
    )

    if not srp_result.candidates:
        # No peers — add to waiting room
        _waiting_room.setdefault(req.concept_id, [])
        if user.id not in [uid for uid, _ in _waiting_room[req.concept_id]]:
            _waiting_room[req.concept_id].append((user.id, time.monotonic()))

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
            "srp": {"used_bfs": False, "routing_path": [], "candidates": 0},
        }

    # Match with the top-scored candidate
    best = srp_result.candidates[0]
    room_token = secrets.token_urlsafe(16)
    session = PeerSession(
        concept_id=req.concept_id,
        initiator_id=user.id,
        partner_id=best.user_id,
        room_token=room_token,
        status="active",
    )
    db.add(session)
    await db.commit()

    return {
        "matched": True,
        "room_token": room_token,
        "partner_username": best.username,
        "partner_mastery": best.mastery_score,
        "concept": srp_result.routed_concept,
        "srp": {
            "score": best.srp_score,
            "mastery_delta": best.mastery_delta,
            "recency_score": best.recency_score,
            "style_compat": best.style_compat,
            "novelty_score": best.novelty_score,
            "used_bfs": srp_result.used_bfs,
            "routing_path": srp_result.routing_path,
            "routed_via": best.routed_via,
        },
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
    """Real network status — no simulated data."""
    real_waiting = sum(len(v) for v in _waiting_room.values())
    real_peer = len(_peer_connections)

    hot = []
    for concept_id, waiters in _waiting_room.items():
        node_result = await db.execute(
            select(ConceptNode).where(ConceptNode.id == concept_id)
        )
        node = node_result.scalar_one_or_none()
        if node:
            hot.append({
                "concept": node.label,
                "students_waiting": len(waiters),
                "concept_id": concept_id,
            })

    hot.sort(key=lambda x: x["students_waiting"], reverse=True)

    return NetworkStatusOut(
        active_students=real_waiting,
        hot_concepts=hot[:5],
        peer_sessions=real_peer,
    )


@router.get("/analytics")
async def get_srp_analytics(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """SRP Routing Table — concepts with peer availability, session counts."""
    from datetime import timedelta
    nodes_result = await db.execute(select(ConceptNode).limit(50))
    nodes = nodes_result.scalars().all()

    cutoff = datetime.utcnow() - timedelta(days=7)
    rows = []
    for node in nodes:
        peers_count = (await db.execute(
            select(func.count(StudentMastery.id)).where(
                and_(
                    StudentMastery.concept_id == node.id,
                    StudentMastery.score >= 0.75,
                    StudentMastery.is_mastered == True,
                    StudentMastery.last_seen >= cutoff,
                )
            )
        )).scalar_one() or 0

        session_count = (await db.execute(
            select(func.count(PeerSession.id)).where(
                and_(
                    PeerSession.concept_id == node.id,
                    PeerSession.status == "completed",
                )
            )
        )).scalar_one() or 0

        waiting = len(_waiting_room.get(node.id, []))

        rows.append({
            "concept_id": node.id,
            "concept": node.label,
            "peers_available": peers_count,
            "students_waiting": waiting,
            "sessions_completed": session_count,
            "avg_wait_seconds": None,
        })

    rows.sort(key=lambda r: r["peers_available"], reverse=True)

    return {
        "routing_table": rows[:20],
        "network_health": {
            "active_peers": sum(r["peers_available"] for r in rows),
            "total_waiting": sum(len(v) for v in _waiting_room.values()),
            "active_sessions": len(_peer_connections),
        },
    }


class PeerRatingRequest(BaseModel):
    stars: int
    note: str = ""


@router.post("/peer-sessions/{session_id}/rate")
async def rate_peer_session(
    session_id: int,
    req: PeerRatingRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit a quality rating for a peer session (1-5 stars)."""
    if not 1 <= req.stars <= 5:
        raise HTTPException(status_code=400, detail="stars must be 1-5")

    from app.models.peer import PeerSessionRating
    rating = PeerSessionRating(
        session_id=session_id,
        rater_id=user.id,
        stars=req.stars,
        note=req.note[:500] if req.note else None,
    )
    db.add(rating)
    await db.commit()
    return {"status": "ok", "stars": req.stars}
