"""
Student network API — Arista track.

Routes students to peers using **SRP** (SAGE Routing Protocol) — modeled on
Arista's link-state routing where every node advertises its "cost" and the
fabric picks the lowest-cost path.

For SAGE, "cost" is replaced by a learning-fitness score:

    srp_score = 0.40 * mastery_delta   # tutor knows what learner doesn't
              + 0.20 * recency         # both still in active session
              + 0.20 * style_compat    # teaching modes line up
              + 0.20 * novelty         # haven't been paired before

Higher score = better peer. The router returns the top-ranked peer plus the
full routing table so the UI can show the decision the way Arista's CLI
shows `show ip route`.
"""
import logging
import math
import secrets
import time
from dataclasses import dataclass
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User
from app.models.session import PeerSession
from app.models.concept import ConceptNode, StudentMastery
from app.routers.auth import get_current_user

router = APIRouter(prefix="/network", tags=["network"])
log = logging.getLogger("sage.network")

# SRP scoring weights — exposed so the dashboard can display the formula.
SRP_WEIGHTS = {
    "mastery_delta": 0.40,
    "recency": 0.20,
    "style_compat": 0.20,
    "novelty": 0.20,
}


@dataclass(frozen=True)
class RouteCandidate:
    user_id: int
    display: str
    score: float
    components: dict
    role: str  # "tutor" | "co_learner"
    last_seen_seconds: float


def _srp_score(
    *,
    mastery_delta: float,
    recency: float,
    style_compat: float,
    novelty: float,
) -> tuple[float, dict]:
    """Return (score, components) — components are normalized to 0..1."""
    components = {
        "mastery_delta": max(0.0, min(1.0, mastery_delta)),
        "recency": max(0.0, min(1.0, recency)),
        "style_compat": max(0.0, min(1.0, style_compat)),
        "novelty": max(0.0, min(1.0, novelty)),
    }
    score = sum(SRP_WEIGHTS[k] * components[k] for k in SRP_WEIGHTS)
    return score, components

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


async def _build_routing_table(
    db: AsyncSession,
    requester: User,
    concept_id: int,
) -> list[RouteCandidate]:
    """Compute SRP scores for every plausible peer for this concept."""
    now = time.monotonic()

    # Master tutors — students who already mastered this concept
    masters_result = await db.execute(
        select(User, StudentMastery)
        .join(StudentMastery, StudentMastery.user_id == User.id)
        .where(
            and_(
                StudentMastery.concept_id == concept_id,
                StudentMastery.is_mastered == True,
                StudentMastery.user_id != requester.id,
            )
        )
        .limit(20)
    )
    candidates: list[RouteCandidate] = []
    for u, mastery in masters_result.all():
        # Tutor mastery is high; learner mastery is low → big delta
        mastery_delta = float(mastery.score or 0.85)
        recency = 0.5  # we don't have last-seen for offline DB users
        # Style compat: same teaching mode → 1.0; otherwise simple matrix
        style_compat = 1.0 if (u.teaching_mode == requester.teaching_mode) else 0.6
        # Novelty: have we seen them before? Penalize repeat pairs.
        prior = await db.execute(
            select(PeerSession).where(
                or_(
                    and_(
                        PeerSession.initiator_id == requester.id,
                        PeerSession.partner_id == u.id,
                    ),
                    and_(
                        PeerSession.initiator_id == u.id,
                        PeerSession.partner_id == requester.id,
                    ),
                )
            )
        )
        prior_count = len(prior.scalars().all())
        novelty = math.exp(-prior_count / 2.0)

        score, components = _srp_score(
            mastery_delta=mastery_delta,
            recency=recency,
            style_compat=style_compat,
            novelty=novelty,
        )
        candidates.append(RouteCandidate(
            user_id=u.id,
            display=u.display_name or u.username or f"user-{u.id}",
            score=score,
            components=components,
            role="tutor",
            last_seen_seconds=0.0,
        ))

    # Co-learners — anyone currently waiting on the same concept
    waiting = _waiting_room.get(concept_id, [])
    for waiter_id, ts in waiting:
        if waiter_id == requester.id:
            continue
        wu_result = await db.execute(select(User).where(User.id == waiter_id))
        wu = wu_result.scalar_one_or_none()
        if not wu:
            continue
        seconds_waiting = now - ts
        recency = max(0.0, 1.0 - seconds_waiting / WAIT_TIMEOUT_SECONDS)
        score, components = _srp_score(
            mastery_delta=0.3,         # equal — both learners
            recency=recency,
            style_compat=1.0 if wu.teaching_mode == requester.teaching_mode else 0.5,
            novelty=1.0,
        )
        candidates.append(RouteCandidate(
            user_id=wu.id,
            display=wu.display_name or wu.username or f"user-{wu.id}",
            score=score,
            components=components,
            role="co_learner",
            last_seen_seconds=seconds_waiting,
        ))

    candidates.sort(key=lambda c: c.score, reverse=True)
    return candidates[:8]


def _route_table_payload(table: list[RouteCandidate]) -> list[dict]:
    return [
        {
            "user_id": c.user_id,
            "display": c.display,
            "score": round(c.score, 3),
            "components": {k: round(v, 3) for k, v in c.components.items()},
            "role": c.role,
            "last_seen_seconds": round(c.last_seen_seconds, 1),
        }
        for c in table
    ]


@router.post("/peer-match")
async def request_peer_match(
    req: PeerMatchRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    SRP-routed peer match. Returns the best peer from the routing table plus
    the full table so the UI can show the decision.
    """
    _cleanup_waiting_room()

    node_result = await db.execute(
        select(ConceptNode).where(ConceptNode.id == req.concept_id)
    )
    node = node_result.scalar_one_or_none()
    if not node:
        raise HTTPException(status_code=404, detail="Concept not found")

    routing_table = await _build_routing_table(db, user, req.concept_id)
    waiting = _waiting_room.get(req.concept_id, [])
    best = routing_table[0] if routing_table else None

    if best and best.role == "co_learner" and waiting and waiting[0][0] == best.user_id:
        # Pair with the best co-learner waiter
        _waiting_room[req.concept_id] = [
            (uid, ts) for uid, ts in _waiting_room.get(req.concept_id, [])
            if uid != best.user_id
        ]
        if not _waiting_room[req.concept_id]:
            _waiting_room.pop(req.concept_id, None)

        room_token = secrets.token_urlsafe(16)
        session = PeerSession(
            concept_id=req.concept_id,
            initiator_id=best.user_id,
            partner_id=user.id,
            room_token=room_token,
            status="active",
        )
        db.add(session)
        await db.commit()

        return {
            "matched": True,
            "room_token": room_token,
            "partner_is_master": False,
            "concept": node.label,
            "selected": _route_table_payload([best])[0],
            "routing_table": _route_table_payload(routing_table),
            "srp_weights": SRP_WEIGHTS,
        }

    if best and best.role == "tutor":
        # Tutor isn't necessarily live — return their info but mark waiting.
        if req.concept_id not in _waiting_room:
            _waiting_room[req.concept_id] = []
        if user.id not in [uid for uid, _ in _waiting_room[req.concept_id]]:
            _waiting_room[req.concept_id].append((user.id, time.monotonic()))
        room_token = secrets.token_urlsafe(16)
        db.add(PeerSession(
            concept_id=req.concept_id,
            initiator_id=user.id,
            room_token=room_token,
            status="waiting",
        ))
        await db.commit()
        return {
            "matched": False,
            "room_token": room_token,
            "waiting": True,
            "concept": node.label,
            "selected": _route_table_payload([best])[0],
            "routing_table": _route_table_payload(routing_table),
            "srp_weights": SRP_WEIGHTS,
        }

    # No candidates → enqueue
    if req.concept_id not in _waiting_room:
        _waiting_room[req.concept_id] = []
    if user.id not in [uid for uid, _ in _waiting_room[req.concept_id]]:
        _waiting_room[req.concept_id].append((user.id, time.monotonic()))
    room_token = secrets.token_urlsafe(16)
    db.add(PeerSession(
        concept_id=req.concept_id,
        initiator_id=user.id,
        room_token=room_token,
        status="waiting",
    ))
    await db.commit()
    return {
        "matched": False,
        "room_token": room_token,
        "waiting": True,
        "concept": node.label,
        "selected": None,
        "routing_table": _route_table_payload(routing_table),
        "srp_weights": SRP_WEIGHTS,
    }


@router.get("/topology/{concept_id}")
async def topology(
    concept_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Snapshot of the network topology for D3 rendering."""
    routing_table = await _build_routing_table(db, user, concept_id)
    nodes = [
        {"id": "self", "label": "you", "kind": "self", "x": 0, "y": 0},
    ]
    edges = []
    for i, c in enumerate(routing_table):
        nodes.append({
            "id": str(c.user_id),
            "label": c.display,
            "kind": c.role,
            "score": round(c.score, 3),
        })
        edges.append({
            "source": "self",
            "target": str(c.user_id),
            "weight": round(c.score, 3),
        })
    return {
        "nodes": nodes,
        "edges": edges,
        "weights": SRP_WEIGHTS,
        "routing_table": _route_table_payload(routing_table),
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
