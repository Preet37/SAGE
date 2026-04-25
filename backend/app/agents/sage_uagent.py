"""SAGE Tutor uAgent — Fetch.ai Agentverse-discoverable wrapper.

What it does:
- Implements the mandatory **Chat Protocol** so any ASI:One user (or
  another uAgent) can chat with SAGE.
- Routes incoming chat messages through the existing tutor agent loop,
  grounded in a 'general inquiry' lesson so the loop has valid context.
- Delegates quiz requests to a sibling **quiz uAgent** (multi-agent
  orchestration demo) by sending a typed `QuizRequest` message.
- Implements an optional **Payment Protocol** stub for premium content.

Run:
    python -m app.agents.sage_uagent

Then register on Agentverse using the URL printed at startup, or use
`agentverse-client` to register programmatically (see scripts/register_uagents.py).
"""

from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from uagents import Agent, Context, Model, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

# Local imports — keep them late so this module can be imported without
# pulling in the full FastAPI stack (uagents only needs the agent loop +
# config + DB lookup).
from ..agent.agent_loop import run_tutor_agent_loop
from ..agent.context import TutorContext
from ..config import get_settings
from ..db import engine
from sqlmodel import Session, select

from .quiz_uagent import QuizRequest, QuizResponse  # multi-agent target

logger = logging.getLogger("sage.uagent")

# ── Agent ──────────────────────────────────────────────────────

settings = get_settings()
SEED = settings.fetchai_agent_seed or "sage-tutor-default-seed-please-change-in-production-32chars"
PORT = int(os.environ.get("SAGE_UAGENT_PORT", "8101"))

agent = Agent(
    name=settings.fetchai_agent_name or "sage-tutor",
    seed=SEED,
    port=PORT,
    endpoint=[f"http://127.0.0.1:{PORT}/submit"],
)

chat_proto = Protocol(spec=chat_protocol_spec)


# ── Optional Payment Protocol (stub) ───────────────────────────

class PaymentRequest(Model):
    sku: str          # e.g. "premium_course:lora-deep-dive"
    amount: float     # FET tokens
    currency: str = "FET"


class PaymentReceipt(Model):
    sku: str
    paid: bool
    tx_hash: str = ""
    note: str = ""


payment_proto = Protocol(name="SagePayment", version="0.1.0")


@payment_proto.on_message(model=PaymentRequest, replies=PaymentReceipt)
async def handle_payment(ctx: Context, sender: str, msg: PaymentRequest):
    """Stubbed payment handler — accepts the request and returns a receipt.

    A production deployment would integrate with the Fetch.ai escrow contract
    or check an on-chain payment confirmation here. We return a deterministic
    receipt for the demo path.
    """
    ctx.logger.info("Payment request from %s: sku=%s amount=%s", sender, msg.sku, msg.amount)
    await ctx.send(sender, PaymentReceipt(
        sku=msg.sku,
        paid=True,
        tx_hash=f"demo-tx-{datetime.now(timezone.utc).timestamp():.0f}",
        note="Demo receipt. Wire to Fetch.ai escrow for production billing.",
    ))


# ── Helpers ────────────────────────────────────────────────────

def _looks_like_quiz_request(text: str) -> Optional[str]:
    lower = text.lower().strip()
    triggers = ["quiz me", "give me a quiz", "test me on", "make a quiz"]
    for t in triggers:
        if t in lower:
            topic = lower.split(t, 1)[1].strip(" .?:on")
            return topic or "general"
    return None


def _pick_default_lesson() -> Optional[dict]:
    """Pick any lesson from the DB to give the tutor a valid context."""
    try:
        from ..models.learning import Lesson
        with Session(engine) as db:
            lesson = db.exec(select(Lesson).limit(1)).first()
            if not lesson:
                return None
            return {
                "id": lesson.id,
                "title": lesson.title,
                "summary": lesson.summary or "",
                "content": (lesson.content or "")[:6000],
                "reference_kb": lesson.reference_kb or "",
                "concepts": _safe_list(lesson.concepts),
            }
    except Exception as e:
        logger.warning("Could not load default lesson: %s", e)
        return None


def _safe_list(value: Optional[str]) -> list[str]:
    if not value:
        return []
    try:
        import json
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return [str(x) for x in parsed]
    except Exception:
        pass
    return []


async def _stream_to_text(messages: list[dict], context: TutorContext) -> str:
    """Drain the SSE generator into a single concatenated reply."""
    import json as _json
    out: list[str] = []
    async for chunk in run_tutor_agent_loop(messages, context):
        try:
            data = chunk.removeprefix("data: ").strip()
            if not data:
                continue
            event = _json.loads(data)
            if event.get("type") == "text":
                out.append(event.get("delta", ""))
            elif event.get("type") == "verification":
                v = event.get("result", {})
                if v.get("label") == "unverified":
                    out.append(
                        f"\n\n_(verification: {int(v.get('score', 0)*100)}%; treat with care)_"
                    )
        except Exception:
            continue
    return "".join(out).strip()


# ── Chat Protocol handler (mandatory) ──────────────────────────

@chat_proto.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    """Receive a chat from ASI:One / another agent. Reply with the tutor's
    answer, ack the original message, optionally delegate to the quiz agent."""

    # 1) Acknowledge the incoming message immediately.
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.now(timezone.utc),
        acknowledged_msg_id=msg.msg_id,
    ))

    user_text = msg.text() or ""
    ctx.logger.info("Inbound from %s: %s", sender, user_text[:160])

    # 2) Decide if this is a quiz request → multi-agent delegation.
    quiz_topic = _looks_like_quiz_request(user_text)
    if quiz_topic:
        quiz_agent_addr = os.environ.get("SAGE_QUIZ_AGENT_ADDRESS", "")
        if quiz_agent_addr:
            ctx.logger.info("Delegating quiz to %s on topic '%s'", quiz_agent_addr, quiz_topic)
            await ctx.send(quiz_agent_addr, QuizRequest(topic=quiz_topic, requester=sender))
            return  # quiz agent will reply directly to the user
        # Fall through if no quiz agent registered — let the tutor handle it.

    # 3) Plain tutor flow — wrap in a TutorContext.
    lesson = _pick_default_lesson()
    if lesson is None:
        reply = (
            "SAGE's database is empty (no lessons seeded). "
            "Run `python seed.py` on the server first."
        )
    else:
        ctx_obj = TutorContext(
            lesson_id=lesson["id"],
            lesson_title=lesson["title"],
            lesson_summary=lesson["summary"],
            concepts=lesson["concepts"],
            completed_lesson_titles=[],
            mode="default",
            lesson_content=lesson["content"],
            reference_kb=lesson["reference_kb"],
            curriculum_index=[],
            domain="technical",
            available_images=[],
        )
        try:
            reply = await _stream_to_text(
                [{"role": "user", "content": user_text}], ctx_obj,
            )
            if not reply:
                reply = "(SAGE produced an empty response — please try rephrasing.)"
        except Exception as e:
            ctx.logger.exception("Tutor loop failed: %s", e)
            reply = "Sorry, the SAGE tutor hit an error answering that question."

    # 4) Send the reply back as a ChatMessage with TextContent.
    await ctx.send(sender, ChatMessage(content=[TextContent(type="text", text=reply)]))

    # 5) End the session politely.
    await ctx.send(sender, ChatMessage(content=[EndSessionContent(type="end-session")]))


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info("Ack from %s for %s", sender, msg.acknowledged_msg_id)


# ── Quiz reply handling (multi-agent) ──────────────────────────

quiz_relay_proto = Protocol(name="SageQuizRelay", version="0.1.0")


@quiz_relay_proto.on_message(model=QuizResponse)
async def handle_quiz_response(ctx: Context, sender: str, msg: QuizResponse):
    """When the quiz agent replies, forward the formatted text to the
    original requester recorded in the QuizResponse payload."""
    if msg.requester:
        await ctx.send(msg.requester, ChatMessage(
            content=[TextContent(type="text", text=msg.formatted)],
        ))
        await ctx.send(msg.requester, ChatMessage(
            content=[EndSessionContent(type="end-session")],
        ))


# ── Wire-up ────────────────────────────────────────────────────

agent.include(chat_proto, publish_manifest=True)
agent.include(payment_proto, publish_manifest=True)
agent.include(quiz_relay_proto, publish_manifest=True)


@agent.on_event("startup")
async def announce(ctx: Context):
    ctx.logger.info("SAGE Tutor uAgent ready — address: %s", agent.address)
    ctx.logger.info("Register at: %s/agents/register", settings.fetchai_agentverse_url)
    try:
        from pathlib import Path
        Path("/tmp/sage_uagent_address").write_text(agent.address)
    except Exception:
        pass


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
    agent.run()


if __name__ == "__main__":
    main()
