"""Network — peer matching and live peer-session websocket.

In-memory only: matching state lives for the lifetime of the process. Suitable
for single-instance MVP; horizontal scaling needs Redis pub/sub.

`start_peer_sweeper(app)` is wired from `lifespan` in main.py and clears
waiters that exceed `WAIT_TIMEOUT_SECONDS` so the queue never accumulates
abandoned matches.
"""

from __future__ import annotations

import asyncio
import logging
import secrets
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any, Deque

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.models import User
from app.schemas import NetworkStatus, PeerMatchRequest, PeerMatchResponse
from app.security import get_current_user

router = APIRouter(prefix="/network", tags=["network"])
log = logging.getLogger("sage.network")

WAIT_TIMEOUT_SECONDS = 300  # 5 minutes


@dataclass
class _Waiter:
    user_id: int
    user_name: str
    concept: str | None
    room_token: str
    enqueued_at: float


_WAITING: Deque[_Waiter] = deque()
_ACTIVE_ROOMS: dict[str, dict[str, Any]] = {}
_HOT_CONCEPTS: dict[str, int] = defaultdict(int)
_ROOM_CONNS: dict[str, list[WebSocket]] = defaultdict(list)
_LOCK = asyncio.Lock()


def _bump_hot(concept: str | None) -> None:
    if concept:
        _HOT_CONCEPTS[concept] = _HOT_CONCEPTS.get(concept, 0) + 1


@router.post("/peer-match", response_model=PeerMatchResponse)
async def peer_match(
    payload: PeerMatchRequest,
    user: User = Depends(get_current_user),
):
    _bump_hot(payload.concept)
    async with _LOCK:
        partner: _Waiter | None = None
        for w in list(_WAITING):
            if w.user_id != user.id and (payload.concept is None or w.concept == payload.concept):
                partner = w
                _WAITING.remove(w)
                break

        if partner:
            _ACTIVE_ROOMS[partner.room_token] = {
                "concept": partner.concept,
                "users": [partner.user_id, user.id],
                "started_at": time.time(),
            }
            return PeerMatchResponse(
                state="matched",
                room_token=partner.room_token,
                peer=partner.user_name,
            )

        token = secrets.token_urlsafe(8)
        _WAITING.append(
            _Waiter(
                user_id=user.id,
                user_name=user.name or user.email,
                concept=payload.concept,
                room_token=token,
                enqueued_at=time.time(),
            )
        )
        return PeerMatchResponse(state="waiting", room_token=token, peer=None)


@router.get("/status", response_model=NetworkStatus)
async def network_status(_: User = Depends(get_current_user)):
    hot = [c for c, _ in sorted(_HOT_CONCEPTS.items(), key=lambda kv: -kv[1])[:5]]
    return NetworkStatus(
        waiting=len(_WAITING),
        active_rooms=len(_ACTIVE_ROOMS),
        hot_concepts=hot,
    )


@router.websocket("/peer-session/{room_token}")
async def peer_session(websocket: WebSocket, room_token: str):
    await websocket.accept()
    _ROOM_CONNS[room_token].append(websocket)
    try:
        await websocket.send_json(
            {"event": "joined", "room": room_token, "peers": len(_ROOM_CONNS[room_token])}
        )
        while True:
            data = await websocket.receive_json()
            for ws in list(_ROOM_CONNS[room_token]):
                if ws is websocket:
                    continue
                try:
                    await ws.send_json({"event": "message", **data})
                except Exception:
                    _ROOM_CONNS[room_token].remove(ws)
    except WebSocketDisconnect:
        pass
    finally:
        if websocket in _ROOM_CONNS[room_token]:
            _ROOM_CONNS[room_token].remove(websocket)
        if not _ROOM_CONNS[room_token]:
            _ROOM_CONNS.pop(room_token, None)
            _ACTIVE_ROOMS.pop(room_token, None)


# ----- Sweeper ------------------------------------------------------------


async def _sweep_loop(interval_seconds: float = 60.0) -> None:
    """Drop waiters older than WAIT_TIMEOUT_SECONDS; run forever."""
    while True:
        try:
            await asyncio.sleep(interval_seconds)
            cutoff = time.time() - WAIT_TIMEOUT_SECONDS
            async with _LOCK:
                kept = deque(w for w in _WAITING if w.enqueued_at >= cutoff)
                dropped = len(_WAITING) - len(kept)
                if dropped:
                    _WAITING.clear()
                    _WAITING.extend(kept)
                    log.info("dropped %d stale peer waiters", dropped)
        except asyncio.CancelledError:
            raise
        except Exception:  # pragma: no cover - never crash the sweeper
            log.exception("peer sweep failed")


def start_peer_sweeper() -> asyncio.Task:
    return asyncio.create_task(_sweep_loop())
