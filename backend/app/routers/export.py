"""
PDF export — generates a print-ready A4 PDF of a SAGE chat session.
Uses ReportLab canvas (pure Python, no system dependencies).
"""
import io
import logging
import re
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

try:
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.utils import simpleSplit
    _RL_AVAILABLE = True
    A4_W, A4_H = A4
except ImportError:
    _RL_AVAILABLE = False
    A4_W, A4_H = 595.27, 841.89  # A4 fallback dimensions

router = APIRouter(prefix="/export", tags=["export"])
log = logging.getLogger("sage.export")
MARGIN = 40
BUBBLE_MAX_W = A4_W - MARGIN * 2 - 20
FONT_BODY = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
BODY_SIZE = 10
LINE_H = 14
BUBBLE_PAD = 8
CORNER_R = 6


class ChatMsg(BaseModel):
    role: str
    content: str


class ExportRequest(BaseModel):
    messages: list[ChatMsg]
    lesson_title: Optional[str] = "SAGE Session"
    course_title: Optional[str] = None


def _clean(text: str) -> str:
    text = re.sub(r"[*_`#~]", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def _key_concepts(messages: list[ChatMsg]) -> list[str]:
    concepts: list[str] = []
    for m in messages:
        if m.role == "assistant":
            found = re.findall(r"\b([A-Z][a-z]+(?: [A-Z][a-z]+)+)\b", m.content)
            concepts.extend(found)
    seen: set[str] = set()
    return [c for c in concepts if not (c in seen or seen.add(c))][:8]  # type: ignore[func-returns-value]


def _draw_bubble(
    c: "rl_canvas.Canvas",
    text: str,
    x: float,
    y: float,
    max_w: float,
    is_user: bool,
) -> float:
    """Draw a chat bubble. Returns the height consumed."""
    lines = simpleSplit(text, FONT_BODY, BODY_SIZE, max_w - BUBBLE_PAD * 2)
    if not lines:
        return 0
    bh = len(lines) * LINE_H + BUBBLE_PAD * 2
    bw = max(
        max(c.stringWidth(l, FONT_BODY, BODY_SIZE) for l in lines) + BUBBLE_PAD * 2,
        80,
    )
    bx = (A4_W - MARGIN - bw) if is_user else x
    by = y - bh

    bg = colors.HexColor("#E8F4FD") if is_user else colors.HexColor("#F0F0F0")
    c.setFillColor(bg)
    c.roundRect(bx, by, bw, bh, CORNER_R, fill=1, stroke=0)

    c.setFillColor(colors.HexColor("#1A1A1A"))
    c.setFont(FONT_BODY, BODY_SIZE)
    ty = by + bh - BUBBLE_PAD - LINE_H + 2
    for line in lines:
        c.drawString(bx + BUBBLE_PAD, ty, line)
        ty -= LINE_H

    return bh + 6


@router.post("/pdf")
async def export_pdf(req: ExportRequest) -> StreamingResponse:
    if not _RL_AVAILABLE:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="reportlab not installed")

    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=A4)

    # Header
    c.setFont(FONT_BOLD, 16)
    c.setFillColor(colors.HexColor("#0066CC"))
    c.drawString(MARGIN, A4_H - MARGIN, "SAGE")
    c.setFont(FONT_BODY, 10)
    c.setFillColor(colors.HexColor("#555555"))
    header_line = req.lesson_title or "Session Export"
    if req.course_title:
        header_line = f"{req.course_title} · {header_line}"
    c.drawString(MARGIN + 40, A4_H - MARGIN, header_line)

    c.setStrokeColor(colors.HexColor("#DDDDDD"))
    c.line(MARGIN, A4_H - MARGIN - 8, A4_W - MARGIN, A4_H - MARGIN - 8)

    # Key concepts
    concepts = _key_concepts(req.messages)
    cy = A4_H - MARGIN - 20
    if concepts:
        c.setFont(FONT_BOLD, 8)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(MARGIN, cy, "KEY CONCEPTS:")
        cx = MARGIN + 90
        c.setFont(FONT_BODY, 8)
        for concept in concepts:
            w = c.stringWidth(concept, FONT_BODY, 8) + 10
            c.setFillColor(colors.HexColor("#E8F4FD"))
            c.roundRect(cx, cy - 2, w, 12, 3, fill=1, stroke=0)
            c.setFillColor(colors.HexColor("#0066CC"))
            c.drawString(cx + 4, cy, concept)
            cx += w + 4
        cy -= 20
    else:
        cy -= 4

    # Messages
    y = cy - 10
    for msg in req.messages:
        if msg.role not in ("user", "assistant"):
            continue
        text = _clean(msg.content)
        if not text:
            continue
        is_user = msg.role == "user"
        role_label = "You" if is_user else "SAGE"
        c.setFont(FONT_BOLD, 7)
        c.setFillColor(colors.HexColor("#999999"))
        lx = (A4_W - MARGIN - c.stringWidth(role_label, FONT_BOLD, 7)) if is_user else MARGIN
        c.drawString(lx, y, role_label)
        y -= 10

        consumed = _draw_bubble(c, text, MARGIN, y, BUBBLE_MAX_W, is_user)
        y -= consumed

        if y < MARGIN + 60:
            c.showPage()
            y = A4_H - MARGIN - 20

    c.save()
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="sage-session.pdf"'},
    )
