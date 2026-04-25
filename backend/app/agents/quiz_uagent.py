"""Quiz uAgent — sibling agent that the SAGE Tutor delegates to.

This is the multi-agent orchestration deliverable for the Fetch.ai track:
the tutor agent decides quiz requests should be handled by a specialist,
sends a typed `QuizRequest` here, and we reply with a `QuizResponse` that
the tutor relays back to the user via the Chat Protocol.

We use the existing tutor agent loop in 'quiz' mode so the responses match
SAGE's pedagogical style (Socratic, with ground truth in the lesson KB).
"""

from __future__ import annotations

import json
import logging
import os
from typing import Optional

from sqlmodel import Session, select
from uagents import Agent, Context, Model, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    TextContent,
    chat_protocol_spec,
)

from ..agent.agent_loop import run_tutor_agent_loop
from ..agent.context import TutorContext
from ..config import get_settings
from ..db import engine
from ..models.learning import Lesson

logger = logging.getLogger("sage.quiz_uagent")


class QuizRequest(Model):
    topic: str
    requester: str = ""        # the original chat user — relayed back from the tutor
    n: int = 3


class QuizResponse(Model):
    topic: str
    formatted: str             # plain-text formatted quiz, ready to post back via chat
    requester: str = ""


# ── Agent ──────────────────────────────────────────────────────

settings = get_settings()
SEED = (settings.fetchai_agent_seed or "sage-quiz-default-seed-please-change-32") + "/quiz"
PORT = int(os.environ.get("SAGE_QUIZ_AGENT_PORT", "8102"))

agent = Agent(
    name=(settings.fetchai_agent_name or "sage-tutor") + "-quiz",
    seed=SEED,
    port=PORT,
    endpoint=[f"http://127.0.0.1:{PORT}/submit"],
)

quiz_proto = Protocol(name="SageQuiz", version="0.1.0")


def _find_lesson_for_topic(topic: str) -> Optional[Lesson]:
    needle = topic.lower().strip()
    if not needle:
        return None
    with Session(engine) as db:
        rows = db.exec(select(Lesson).limit(200)).all()
    best: tuple[int, Optional[Lesson]] = (0, None)
    for l in rows:
        hay = " ".join([
            (l.title or ""),
            (l.slug or ""),
            (l.summary or ""),
            (l.concepts or ""),
        ]).lower()
        score = sum(1 for tok in needle.split() if tok in hay)
        if score > best[0]:
            best = (score, l)
    return best[1]


async def _drain(messages: list[dict], context: TutorContext) -> str:
    out: list[str] = []
    async for chunk in run_tutor_agent_loop(messages, context):
        try:
            data = chunk.removeprefix("data: ").strip()
            if not data:
                continue
            ev = json.loads(data)
            if ev.get("type") == "text":
                out.append(ev.get("delta", ""))
        except Exception:
            continue
    return "".join(out).strip()


@quiz_proto.on_message(model=QuizRequest, replies=QuizResponse)
async def handle_quiz(ctx: Context, sender: str, msg: QuizRequest):
    ctx.logger.info("QuizRequest from %s: topic=%r requester=%s", sender, msg.topic, msg.requester or "(none)")
    lesson = _find_lesson_for_topic(msg.topic)
    if lesson is None:
        formatted = (
            f"I couldn't find a lesson covering '{msg.topic}' in SAGE's curriculum. "
            "Try one of: LoRA, attention, multimodal AI, agents, or physical AI."
        )
        await ctx.send(sender, QuizResponse(topic=msg.topic, formatted=formatted, requester=msg.requester))
        return

    concepts: list[str] = []
    try:
        concepts = json.loads(lesson.concepts) if lesson.concepts else []
    except Exception:
        concepts = []

    context = TutorContext(
        lesson_id=lesson.id,
        lesson_title=lesson.title,
        lesson_summary=lesson.summary or "",
        concepts=concepts,
        completed_lesson_titles=[],
        mode="quiz",
        lesson_content=(lesson.content or "")[:5000],
        reference_kb=lesson.reference_kb or "",
        curriculum_index=[],
        domain="technical",
        available_images=[],
    )

    user_msg = (
        f"Generate {max(1, min(msg.n, 5))} short conceptual quiz questions about "
        f"'{lesson.title}', focused on the topic '{msg.topic}'. For each question, "
        "give the question only — do not reveal the answer."
    )
    body = await _drain([{"role": "user", "content": user_msg}], context)

    formatted = (
        f"📚 Quiz on **{lesson.title}** (topic: {msg.topic})\n\n{body or '(empty response)'}"
    )
    await ctx.send(sender, QuizResponse(topic=msg.topic, formatted=formatted, requester=msg.requester))


# Allow the quiz agent to be addressed directly via Chat Protocol too.
chat_proto = Protocol(spec=chat_protocol_spec)


@chat_proto.on_message(ChatMessage)
async def chat_to_quiz(ctx: Context, sender: str, msg: ChatMessage):
    """If a user chats this agent directly, treat the text as a topic."""
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=msg.timestamp, acknowledged_msg_id=msg.msg_id,
    ))
    text = msg.text().strip() or "general"
    formatted_msg = QuizRequest(topic=text, requester=sender)
    await handle_quiz(ctx, sender, formatted_msg)


@chat_proto.on_message(ChatAcknowledgement)
async def chat_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass


agent.include(quiz_proto, publish_manifest=True)
agent.include(chat_proto, publish_manifest=True)


@agent.on_event("startup")
async def announce(ctx: Context):
    ctx.logger.info("SAGE Quiz uAgent ready — address: %s", agent.address)
    ctx.logger.info(
        "Set SAGE_QUIZ_AGENT_ADDRESS=%s in the tutor agent's env to enable delegation.",
        agent.address,
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
    agent.run()


if __name__ == "__main__":
    main()
