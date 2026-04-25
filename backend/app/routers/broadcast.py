"""
Teacher broadcast rooms — real-time lesson sharing via WebSocket.
Teacher creates a room, gets a 6-char code + QR join URL.
Students connect via WebSocket and receive lesson content when pushed.
"""
import io
import logging
import secrets
import string
from dataclasses import dataclass, field

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from pydantic import BaseModel

from app.config import get_settings

try:
    import qrcode
    import qrcode.image.pure
    _QR_AVAILABLE = True
except ImportError:
    _QR_AVAILABLE = False

router = APIRouter(prefix="/broadcast", tags=["broadcast"])
log = logging.getLogger("sage.broadcast")
settings = get_settings()

_CODE_CHARS = string.ascii_uppercase + string.digits


@dataclass
class BroadcastRoom:
    code: str
    teacher_id: str
    student_connections: list[WebSocket] = field(default_factory=list)
    last_lesson: dict | None = None


rooms: dict[str, BroadcastRoom] = {}


def _gen_code() -> str:
    while True:
        code = "".join(secrets.choice(_CODE_CHARS) for _ in range(6))
        if code not in rooms:
            return code


class RoomCreate(BaseModel):
    teacher_id: str


class LessonPush(BaseModel):
    lesson_id: str
    title: str
    content_md: str
    key_concepts: list[str] = []


@router.post("/room")
async def create_room(req: RoomCreate) -> dict:
    code = _gen_code()
    rooms[code] = BroadcastRoom(code=code, teacher_id=req.teacher_id)
    base = getattr(settings, "frontend_url", "http://localhost:3000").split(",")[0].strip()
    join_url = f"{base}/broadcast/{code}"
    return {
        "code": code,
        "join_url": join_url,
        "qr_url": f"/broadcast/room/{code}/qr",
    }


@router.get("/room/{code}/qr")
async def get_qr(code: str) -> Response:
    if code not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    if not _QR_AVAILABLE:
        raise HTTPException(status_code=503, detail="qrcode package not installed")

    base = getattr(settings, "frontend_url", "http://localhost:3000").split(",")[0].strip()
    join_url = f"{base}/broadcast/{code}"

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=8, border=2)
    qr.add_data(join_url)
    qr.make(fit=True)
    img = qr.make_image(image_factory=qrcode.image.pure.PyPNGImage)
    buf = io.BytesIO()
    img.save(buf)
    return Response(content=buf.getvalue(), media_type="image/png")


@router.post("/room/{code}/push")
async def push_lesson(code: str, payload: LessonPush) -> dict:
    room = rooms.get(code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    msg = {
        "type": "lesson_content",
        "lesson_id": payload.lesson_id,
        "title": payload.title,
        "content_md": payload.content_md,
        "key_concepts": payload.key_concepts,
    }
    room.last_lesson = msg

    dead: list[WebSocket] = []
    for ws in list(room.student_connections):
        try:
            await ws.send_json(msg)
        except Exception:
            dead.append(ws)
    for ws in dead:
        room.student_connections.remove(ws)

    return {"students_reached": len(room.student_connections)}


@router.websocket("/room/{code}/stream")
async def student_stream(websocket: WebSocket, code: str) -> None:
    room = rooms.get(code)
    if not room:
        await websocket.close(code=4004)
        return

    await websocket.accept()
    room.student_connections.append(websocket)

    if room.last_lesson:
        await websocket.send_json(room.last_lesson)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        if websocket in room.student_connections:
            room.student_connections.remove(websocket)


@router.delete("/room/{code}")
async def close_room(code: str) -> dict:
    room = rooms.pop(code, None)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    for ws in room.student_connections:
        try:
            await ws.send_json({"type": "room_closed"})
            await ws.close()
        except Exception:
            pass
    return {"closed": True, "students_disconnected": len(room.student_connections)}
