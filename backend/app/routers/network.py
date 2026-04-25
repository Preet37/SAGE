"""Network — peer matching and live peer-session websocket.

In-memory only: matching state lives for the lifetime of the process. Suitable
for single-instance MVP; horizontal scaling needs Redis pub/sub.
"""

from __future__ import annotations

import asyncio
import secrets
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Deque

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.models import User
from app.schemas import NetworkStatus, PeerMatchRequest, PeerMatchResponse
from app.security import get_current_user

router = APIRouter(prefix="/network", tags=["network"])


@dataclass
class _Waiter:
    user_id: int
    user_name: str
    concept: str | None
    room_token: str


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
        # Find a waiting partner not equal to the current user.
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
            }
            return PeerMatchResponse(
                state="matched",
                room_token=partner.room_token,
                peer=partner.user_name,
            )

        token = secrets.token_urlsafe(8)
        _WAITING.append(_Waiter(user.id, user.name or user.email, payload.concept, token))
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
        await websocket.send_json({"event": "joined", "room": room_token,
                                   "peers": len(_ROOM_CONNS[room_token])})
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
