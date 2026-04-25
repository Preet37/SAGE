"""
SMS / WhatsApp webhook handler — Twilio integration.
Provides a stateless Socratic tutor accessible over SMS without an account.
Mock mode activates automatically when TWILIO_ACCOUNT_SID is not configured.
"""
import logging
import re
import xml.sax.saxutils
from dataclasses import dataclass, field
from typing import Optional

from fastapi import APIRouter, Form, Response
from openai import AsyncOpenAI

from app.config import get_settings

router = APIRouter(prefix="/sms", tags=["sms"])
log = logging.getLogger("sage.sms")
settings = get_settings()

SMS_MAX_CHARS = 160
_OVERFLOW_SUFFIX = "…(reply 'more' for rest)"
_HARD_CUTOFF = SMS_MAX_CHARS - len(_OVERFLOW_SUFFIX)

SOCRATIC_SMS_SYSTEM = (
    "You are SAGE, a Socratic AI tutor communicating via SMS. "
    "Your replies must be SHORT — under 130 characters when possible. "
    "Ask one guiding question at a time. Never lecture. "
    "Use plain text only — no markdown, no asterisks, no bullet points. "
    "Respond in the same language the student uses. "
    "Be warm, patient, and encouraging."
)


@dataclass
class SmsSession:
    phone: str
    user_id: Optional[str]
    history: list[dict] = field(default_factory=list)
    overflow_cache: str = ""


# phone_number -> SmsSession (process-local; resets on server restart)
sms_sessions: dict[str, SmsSession] = {}


def _is_mock_mode() -> bool:
    import os
    return not os.getenv("TWILIO_ACCOUNT_SID", "")


def _twiml(text: str) -> Response:
    safe = xml.sax.saxutils.escape(text)
    xml_str = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f"<Response><Message>{safe}</Message></Response>"
    )
    return Response(content=xml_str, media_type="text/xml")


def _trim_for_sms(text: str) -> tuple[str, str]:
    """Return (sms_text, overflow). Trims at word boundary if > SMS_MAX_CHARS."""
    clean = re.sub(r"\s+", " ", text).strip()
    clean = re.sub(r"[*_`#~]", "", clean)
    if len(clean) <= SMS_MAX_CHARS:
        return clean, ""
    cutoff = clean.rfind(" ", 0, _HARD_CUTOFF)
    if cutoff == -1:
        cutoff = _HARD_CUTOFF
    return clean[:cutoff] + _OVERFLOW_SUFFIX, clean[cutoff:].strip()


def _build_prompt(session: SmsSession, incoming: str) -> list[dict]:
    messages: list[dict] = []
    for turn in session.history[-6:]:
        messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": incoming})
    return messages


async def _llm_complete(messages: list[dict]) -> str:
    client = AsyncOpenAI(api_key=settings.llm_api_key, base_url=settings.llm_base_url)
    resp = await client.chat.completions.create(
        model=settings.llm_model,
        messages=[{"role": "system", "content": SOCRATIC_SMS_SYSTEM}] + messages,
        max_tokens=120,
        temperature=0.7,
    )
    return resp.choices[0].message.content or ""


@router.post("/incoming")
async def incoming_sms(
    Body: str = Form(default=""),
    From: str = Form(default=""),
    To: str = Form(default=""),
) -> Response:
    """Twilio webhook — receives inbound SMS/WhatsApp messages. No auth required."""
    phone = From.strip()
    message = Body.strip()

    if not phone:
        log.warning("SMS webhook received with no From field")
        return _twiml("Sorry, I could not identify your number.")

    if _is_mock_mode():
        log.info("[SMS MOCK] From=%s To=%s Body=%r", phone, To, message)

    session = sms_sessions.get(phone)
    if session is None:
        session = SmsSession(phone=phone, user_id=None)
        sms_sessions[phone] = session
        log.info("New SMS session for %s", phone)

    if message.lower().strip(" .") in {"more", "continue", "…more"}:
        if session.overflow_cache:
            sms_part, remaining = _trim_for_sms(session.overflow_cache)
            session.overflow_cache = remaining
            return _twiml(sms_part)
        return _twiml("No more to send. Ask me anything!")

    session.history.append({"role": "user", "content": message})
    api_messages = _build_prompt(session, message)

    try:
        raw = await _llm_complete(api_messages)
    except Exception as exc:
        log.error("LLM failed for SMS %s: %s", phone, exc)
        raw = "I'm having trouble right now. Please try again in a moment."

    sms_text, overflow = _trim_for_sms(raw)
    session.overflow_cache = overflow
    session.history.append({"role": "assistant", "content": raw})
    return _twiml(sms_text)


@router.get("/status")
async def sms_status() -> dict:
    return {
        "connected": not _is_mock_mode(),
        "active_sessions": len(sms_sessions),
        "mock_mode": _is_mock_mode(),
    }
