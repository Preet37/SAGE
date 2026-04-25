"""
Fetch.ai Director Agent + Payment Protocol.

The Director is the 7th agent in the SAGE Bureau. It coordinates the other six
specialist agents and exposes:

  * Chat Protocol  — humans talk to the Director from Agentverse / ASI:One.
  * Payment Protocol — students burn 1000 micro-ASI per "Deep Dive" turn
                       so we can demonstrate metered, agent-to-agent payments.

Run as a background daemon thread alongside FastAPI (see uagents_runner.py).
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Optional

from app.config import get_settings

settings = get_settings()
log = logging.getLogger("sage.director")

DEEP_DIVE_COST_MICRO_ASI = 1000  # 0.001 ASI per deep dive turn

try:
    from uagents import Agent, Context, Model
    UAGENTS_AVAILABLE = True
except ImportError:
    UAGENTS_AVAILABLE = False


if UAGENTS_AVAILABLE:

    class DirectorChatRequest(Model):
        content: str
        user_id: Optional[int] = None

    class DirectorChatResponse(Model):
        content: str
        agents_consulted: list[str]
        timestamp: str

    class PaymentRequest(Model):
        """A student requests a metered Deep Dive turn."""
        user_id: int
        lesson_id: int
        question: str
        deep_dive_token: str  # opaque token returned to FastAPI

    class PaymentReceipt(Model):
        ok: bool
        amount_micro_asi: int
        deep_dive_token: str
        ts: str
        reason: str = ""


def create_director_agent():
    if not UAGENTS_AVAILABLE:
        return None

    agent = Agent(
        name="sage_director_agent",
        seed="sage_agent_seed_director",
        port=8007,
        endpoint=["http://localhost:8007/submit"],
        agentverse=settings.agentverse_api_key or None,
    )

    @agent.on_message(model=DirectorChatRequest)
    async def handle_chat(ctx: Context, sender: str, msg: DirectorChatRequest):
        from app.agents.base import asi1_complete

        response = await asi1_complete(
            msg.content,
            system=(
                "You are the SAGE Director Agent. You coordinate six specialist "
                "agents (Pedagogy, Content, ConceptMap, Assessment, PeerMatch, "
                "Progress) to deliver Socratic tutoring. When a user talks to "
                "you on Agentverse, summarize what SAGE can do and how the "
                "agent swarm collaborates."
            ),
        )
        await ctx.send(
            sender,
            DirectorChatResponse(
                content=response,
                agents_consulted=[
                    "pedagogy",
                    "content",
                    "concept_map",
                    "assessment",
                    "peer_match",
                    "progress",
                ],
                timestamp=datetime.utcnow().isoformat(),
            ),
        )

    @agent.on_message(model=PaymentRequest)
    async def handle_payment(ctx: Context, sender: str, msg: PaymentRequest):
        """Charge 1000 micro-ASI for a Deep Dive turn."""
        log.info(
            "deep_dive_payment user=%s lesson=%s amount=%s token=%s",
            msg.user_id, msg.lesson_id, DEEP_DIVE_COST_MICRO_ASI, msg.deep_dive_token,
        )
        # In a real deployment we would settle on the Fetch.ai chain here.
        # For the hackathon, we treat the request itself as proof-of-payment.
        await ctx.send(
            sender,
            PaymentReceipt(
                ok=True,
                amount_micro_asi=DEEP_DIVE_COST_MICRO_ASI,
                deep_dive_token=msg.deep_dive_token,
                ts=datetime.utcnow().isoformat(),
                reason="ok",
            ),
        )

    @agent.on_event("startup")
    async def announce(ctx: Context):
        ctx.logger.info("Director online: %s", agent.address)

    return agent


def director_address() -> str:
    """Return the Director's Agentverse address without starting the Bureau."""
    if not UAGENTS_AVAILABLE:
        return ""
    try:
        from uagents.crypto import Identity
        identity = Identity.from_seed("sage_agent_seed_director", 0)
        return identity.address
    except Exception:
        return ""


def director_badge_payload() -> dict:
    """Payload for the `fetchai_badge` SSE event."""
    return {
        "director_address": director_address(),
        "agentverse_url": "https://agentverse.ai/inspect/?uri=http%3A%2F%2Flocalhost%3A8007",
        "deep_dive_cost_micro_asi": DEEP_DIVE_COST_MICRO_ASI,
        "agents": [
            {"name": "Director", "port": 8007, "role": "coordinator"},
            {"name": "Pedagogy", "port": 8001, "role": "teaching strategy"},
            {"name": "Content", "port": 8002, "role": "KB retrieval"},
            {"name": "ConceptMap", "port": 8003, "role": "graph builder"},
            {"name": "Assessment", "port": 8004, "role": "quiz generator"},
            {"name": "PeerMatch", "port": 8005, "role": "peer routing"},
            {"name": "Progress", "port": 8006, "role": "mastery tracker"},
        ],
    }
