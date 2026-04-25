"""
Teacher broadcast room — teacher creates a room, students join via QR code.
Real-time lesson content is pushed over WebSocket to all connected students.
The classroom hotspot is the server; no cloud sync required for lesson delivery.
"""
import io
import logging
import secrets
import string
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from pydantic import BaseModel

from app.config import get_settings
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/broadcast", tags=["broadcast"])
log = logging.getLogger("sage.broadcast")
settings = get_settings()

_ALPHABET = string.ascii_uppercase + string.digits
_CODE_LEN = 6


# ---------------------------------------------------------------------------
# In-memory room store (process-local)
# ---------------------------------------------------------------------------


@dataclass
class BroadcastRoom:
    code: str
    teacher_id: int
    lesson_id: int
    student_connections: list[WebSocket] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    lesson_content: Optional[dict] = None
    active: bool = True


rooms: dict[str, BroadcastRoom] = {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _new_code() -> str:
    for _ in range(20):
        code = "".join(secrets.choice(_ALPHABET) for _ in range(_CODE_LEN))
        if code not in rooms:
            return code
    raise RuntimeError("Could not generate unique room code")


def _backend_url() -> str:
    url = getattr(settings, "backend_url", "") or ""
    if url:
        return url.rstrip("/")
    return f"http://localhost:{getattr(settings, 'backend_port', 8000)}"


def _join_url(code: str) -> str:
    frontend = settings.frontend_url.split(",")[0].strip().rstrip("/")
    return f"{frontend}/broadcast/{code}"


def _qr_png(url: str) -> bytes:
    try:
        import qrcode  # type: ignore
        from qrcode.image.pure import PyPNGImage  # type: ignore

        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(image_factory=PyPNGImage)
        buf = io.BytesIO()
        img.save(buf)
        return buf.getvalue()
    except Exception:
        # Minimal 1×1 transparent PNG fallback when qrcode is not installed
        import base64
        return base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk"
            "YPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        )


def _require_room(code: str) -> BroadcastRoom:
    room = rooms.get(code.upper())
    if not room or not room.active:
        raise HTTPException(404, "Room not found or has been closed")
    return room


async def _push_to_students(room: BroadcastRoom, payload: dict) -> int:
    dead: list[WebSocket] = []
    sent = 0
    for ws in list(room.student_connections):
        try:
            await ws.send_json(payload)
            sent += 1
        except Exception:
            dead.append(ws)
    for ws in dead:
        if ws in room.student_connections:
            room.student_connections.remove(ws)
    return sent


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class CreateRoomRequest(BaseModel):
    lesson_id: int


class CreateRoomResponse(BaseModel):
    code: str
    join_url: str
    qr_url: str


class RoomInfo(BaseModel):
    code: str
    lesson_id: int
    student_count: int
    active: bool


class PushContentRequest(BaseModel):
    lesson_id: int
    content_md: str
    title: str
    key_concepts: list[str] = []


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.post("/room", response_model=CreateRoomResponse)
async def create_room(
    req: CreateRoomRequest,
    user: User = Depends(get_current_user),
) -> CreateRoomResponse:
    """Teacher creates a broadcast room. Returns a 6-char code + QR URL."""
    code = _new_code()
    rooms[code] = BroadcastRoom(code=code, teacher_id=user.id, lesson_id=req.lesson_id)
    log.info("Room %s created by teacher %s for lesson %s", code, user.id, req.lesson_id)
    return CreateRoomResponse(
        code=code,
        join_url=_join_url(code),
        qr_url=f"{_backend_url()}/broadcast/room/{code}/qr",
    )


@router.get("/room/{code}", response_model=RoomInfo)
async def get_room_info(code: str) -> RoomInfo:
    """Return public room info. No auth required — used by students on join."""
    room = _require_room(code)
    return RoomInfo(
        code=room.code,
        lesson_id=room.lesson_id,
        student_count=len(room.student_connections),
        active=room.active,
    )


@router.get("/room/{code}/qr")
async def get_room_qr(code: str) -> Response:
    """Return a PNG QR code encoding the student join URL."""
    room = _require_room(code)
    png = _qr_png(_join_url(room.code))
    return Response(content=png, media_type="image/png")


@router.post("/room/{code}/push")
async def push_content(
    code: str,
    req: PushContentRequest,
    user: User = Depends(get_current_user),
) -> dict:
    """Teacher pushes lesson content to all connected students."""
    room = _require_room(code)
    if room.teacher_id != user.id:
        raise HTTPException(403, "Only the room teacher can push content")

    payload: dict = {
        "type": "lesson_content",
        "lesson_id": req.lesson_id,
        "title": req.title,
        "content_md": req.content_md,
        "key_concepts": req.key_concepts,
    }
    room.lesson_content = payload
    room.lesson_id = req.lesson_id

    sent = await _push_to_students(room, payload)
    log.info("Teacher %s pushed to room %s (%d students)", user.id, code, sent)
    return {"pushed_to": sent, "code": code}


@router.websocket("/room/{code}/stream")
async def student_stream(code: str, websocket: WebSocket) -> None:
    """
    Student WebSocket connection.
    Immediately delivers cached lesson content if teacher already pushed.
    Stays open to receive future pushes.
    """
    room = rooms.get(code.upper())
    if not room or not room.active:
        await websocket.close(code=4004, reason="Room not found")
        return

    await websocket.accept()
    room.student_connections.append(websocket)
    log.info("Student joined room %s (total: %d)", code, len(room.student_connections))

    if room.lesson_content:
        try:
            await websocket.send_json(room.lesson_content)
        except Exception as exc:
            log.warning("Failed to deliver cached content to new student: %s", exc)

    try:
        while True:
            await websocket.receive_text()  # absorb keepalive pings
    except WebSocketDisconnect:
        pass
    finally:
        if websocket in room.student_connections:
            room.student_connections.remove(websocket)
        log.info("Student left room %s (remaining: %d)", code, len(room.student_connections))


@router.delete("/room/{code}")
async def delete_room(
    code: str,
    user: User = Depends(get_current_user),
) -> dict:
    """Teacher closes the room and disconnects all students."""
    room = _require_room(code)
    if room.teacher_id != user.id:
        raise HTTPException(403, "Only the room teacher can close this room")

    for ws in list(room.student_connections):
        try:
            await ws.send_json({"type": "room_closed", "code": code})
            await ws.close(1001, "Room closed by teacher")
        except Exception:
            pass

    room.active = False
    room.student_connections.clear()
    del rooms[code]
    log.info("Room %s closed by teacher %s", code, user.id)
    return {"closed": True, "code": code}
