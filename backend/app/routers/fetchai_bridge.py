"""Fetch.ai track — small bridge between the SAGE web app and the uAgent.

Two surfaces:
- GET  /fetchai/info   — agent address, registration link, payment SKUs
- POST /fetchai/chat   — proxy a chat message to the local SAGE uAgent over HTTP

The proxy is useful so the demo UI can show the agent path working end-to-end
without forcing a judge to install Agentverse Studio. In production you'd
remove this and let users chat through ASI:One directly.
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from typing import Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..config import get_settings
from ..deps import get_current_user
from ..models.user import User

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/fetchai", tags=["fetchai"])


class AgentInfoResponse(BaseModel):
    enabled: bool
    agent_name: str
    agent_address: Optional[str]
    agentverse_url: str
    asi_one_url: str
    register_link: str
    chat_protocol: str
    payment_skus: list[dict]


@router.get("/info", response_model=AgentInfoResponse)
def info(user: User = Depends(get_current_user)) -> AgentInfoResponse:
    settings = get_settings()
    address = _try_read_address()
    return AgentInfoResponse(
        enabled=settings.feature_fetchai_agent,
        agent_name=settings.fetchai_agent_name,
        agent_address=address,
        agentverse_url=settings.fetchai_agentverse_url,
        asi_one_url=settings.fetchai_asi_one_url,
        register_link=f"{settings.fetchai_agentverse_url.rstrip('/')}/agents/register",
        chat_protocol="AgentChatProtocol/0.3.0",
        payment_skus=[
            {"sku": "premium_course:lora-deep-dive", "price": 1.0, "currency": "FET"},
            {"sku": "annotated_video:attention", "price": 0.5, "currency": "FET"},
        ],
    )


def _try_read_address() -> Optional[str]:
    """Best-effort: read the agent address that the running uAgent prints to a file."""
    from pathlib import Path
    p = Path("/tmp/sage_uagent_address")
    if p.is_file():
        try:
            return p.read_text().strip()
        except Exception:
            return None
    return None


# ── Chat proxy ─────────────────────────────────────────────────

class FetchaiChatRequest(BaseModel):
    message: str
    target: str = "tutor"   # "tutor" | "quiz"


class FetchaiChatResponse(BaseModel):
    ok: bool
    text: str
    target_address: Optional[str]
    elapsed_ms: int
    note: str = ""


@router.post("/chat", response_model=FetchaiChatResponse)
async def proxy_chat(
    req: FetchaiChatRequest,
    user: User = Depends(get_current_user),
) -> FetchaiChatResponse:
    """Forward a chat message to the local SAGE uAgent's HTTP submit endpoint.

    Note: this is a demo path. Real ASI:One messaging happens off-platform via
    the Agentverse network — uAgents discover each other via their addresses,
    not via web hooks. This proxy exists so the SAGE web app can demonstrate
    Chat Protocol payloads without external setup.
    """
    settings = get_settings()
    if not settings.feature_fetchai_agent:
        raise HTTPException(status_code=400, detail="Fetch.ai feature disabled")

    port = 8101 if req.target == "tutor" else 8102
    started = time.perf_counter()

    payload = {
        "version": 1,
        "type": "uagents.contrib.protocols.chat.ChatMessage",
        "session": str(uuid.uuid4()),
        "schema_digest": "model:agentverse-chat-1",
        "payload": {
            "msg_id": str(uuid.uuid4()),
            "timestamp": int(time.time()),
            "content": [{"type": "text", "text": req.message}],
        },
    }

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(f"http://127.0.0.1:{port}/submit", json=payload)
        ok = 200 <= r.status_code < 300
        text = r.text if r.text else "(no body)"
    except Exception as e:
        ok, text = False, f"Could not reach uAgent on port {port}: {e}"

    elapsed = int((time.perf_counter() - started) * 1000)
    return FetchaiChatResponse(
        ok=ok,
        text=text[:2000],
        target_address=_try_read_address() if req.target == "tutor" else None,
        elapsed_ms=elapsed,
        note=(
            "uAgent submit endpoint accepts Chat Protocol envelopes. "
            "If you got a 4xx, the agent may not be running locally — start it with: "
            "`python -m app.agents.sage_uagent`."
        ),
    )
