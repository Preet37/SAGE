"""
SAGE Director Agent — publicly discoverable on Agentverse/ASI:One.
Accepts student questions via Chat Protocol, fans out to 6 specialist agents,
gates Deep Dive mode behind Payment Protocol.
"""
import asyncio
import logging
import secrets
from uagents import Agent, Context
from app.config import get_settings
from app.agents.protocols.chat import ChatMessage, ChatResponse
from app.agents.protocols.payment import (
    PaymentRequest, PaymentConfirmation, DeepDiveUnlocked,
    DEEP_DIVE_COST_MICRO_ASI,
)

log = logging.getLogger("sage.director")
settings = get_settings()

director_agent = Agent(
    name="sage-director",
    seed="sage_agent_seed_director",
    port=8007,
    endpoint=["http://127.0.0.1:8007/submit"],
    agentverse={"api_key": settings.agentverse_api_key},
)

_unlocked_sessions: set[str] = set()


@director_agent.on_event("startup")
async def on_startup(ctx: Context):
    ctx.logger.info("=" * 60)
    ctx.logger.info("SAGE Director Agent started")
    ctx.logger.info(f"Address: {ctx.address}")
    ctx.logger.info(f"Agentverse: https://agentverse.ai/agents/{ctx.address}")
    ctx.logger.info("=" * 60)


@director_agent.on_message(model=ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Chat from {sender}: {msg.content[:80]}")

    from app.agents.base import asi1_complete

    prompt = (
        f"You are SAGE, a Socratic AI tutor. A student asks:\n\n"
        f'"{msg.content}"\n\n'
        f"Teaching mode: {msg.teaching_mode}\n\n"
        f"Respond with a Socratic, guiding answer in 100-150 words. "
        f"Ask a follow-up question at the end."
    )

    try:
        response_text = await asyncio.wait_for(
            asi1_complete(prompt, max_tokens=200), timeout=15.0
        )
    except Exception as e:
        response_text = f"I'm having trouble connecting right now. Please try again shortly. ({e})"

    await ctx.send(sender, ChatResponse(
        content=response_text,
        confidence_score=80,
    ))


@director_agent.on_message(model=PaymentConfirmation)
async def handle_payment(ctx: Context, sender: str, msg: PaymentConfirmation):
    if msg.amount >= DEEP_DIVE_COST_MICRO_ASI:
        session_token = secrets.token_urlsafe(16)
        _unlocked_sessions.add(session_token)
        ctx.logger.info(f"Deep Dive unlocked for {sender}, token {session_token}")
        await ctx.send(sender, DeepDiveUnlocked(session_token=session_token))
    else:
        ctx.logger.warning(f"Insufficient payment from {sender}: {msg.amount}")


def request_deep_dive_payment(sender_address: str) -> PaymentRequest:
    return PaymentRequest(
        amount=DEEP_DIVE_COST_MICRO_ASI,
        denom="atestfet",
        memo="SAGE Deep Dive session — Fetch.ai Payment Protocol",
    )


def is_deep_dive_unlocked(session_token: str) -> bool:
    return session_token in _unlocked_sessions
