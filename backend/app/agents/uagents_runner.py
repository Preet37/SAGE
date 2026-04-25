"""Fetch.ai uAgents runner for SAGE Agentverse deployment.

Wraps the local `Orchestrator` as a uAgent so it can be discovered and called
via the Agentverse network. Each protocol message corresponds to one tutoring
turn. ASI1-Mini is wired in as the fallback LLM via `LLM.from_env()`.

Run locally:
    AGENT_SEED="<your-seed>" ASI1_API_KEY="<key>" \
        python -m app.agents.uagents_runner
"""

from __future__ import annotations

import os
from typing import Any

try:
    from uagents import Agent as UAgent
    from uagents import Context, Model, Protocol
except Exception:  # pragma: no cover - optional dep
    UAgent = None  # type: ignore[assignment]
    Context = Model = Protocol = None  # type: ignore[assignment]

from app.agents.base import AgentContext, LLM
from app.agents.orchestrator import Orchestrator


if Model is not None:

    class TutorRequest(Model):
        session_id: int
        user_id: int
        message: str
        a11y: dict[str, Any] = {}
        mastery: list[dict[str, Any]] = []
        sources: list[str] = []

    class TutorResponse(Model):
        session_id: int
        answer: str
        verification: dict[str, Any]
        plan: dict[str, Any]
        concept_map_delta: list[dict[str, Any]]
        assessment: dict[str, Any]
        peers: list[dict[str, Any]]
        progress_delta: dict[str, Any]
        provider: str


def build_agent() -> Any:
    if UAgent is None:
        raise RuntimeError("uagents is not installed. `pip install uagents`")

    seed = os.getenv("AGENT_SEED", "sage-orchestrator-dev-seed")
    port = int(os.getenv("AGENT_PORT", "8001"))
    endpoint = os.getenv("AGENT_ENDPOINT", f"http://127.0.0.1:{port}/submit")

    agent = UAgent(name="sage-orchestrator", seed=seed, port=port, endpoint=[endpoint])
    proto = Protocol(name="sage-tutor", version="0.1.0")
    llm = LLM.from_env()
    orchestrator = Orchestrator(llm=llm)

    @proto.on_message(model=TutorRequest, replies=TutorResponse)
    async def handle_turn(ctx: Context, sender: str, msg: TutorRequest) -> None:
        ac = AgentContext(
            session_id=msg.session_id,
            user_id=msg.user_id,
            user_message=msg.message,
            a11y=msg.a11y,
            mastery=msg.mastery,
            sources=msg.sources,
        )
        ac = await orchestrator.run_turn(ac)
        await ctx.send(
            sender,
            TutorResponse(
                session_id=ac.session_id,
                answer=ac.answer,
                verification=ac.verification,
                plan=ac.plan,
                concept_map_delta=ac.concept_map_delta,
                assessment=ac.assessment,
                peers=ac.peers,
                progress_delta=ac.progress_delta,
                provider=llm.primary.name,
            ),
        )

    agent.include(proto, publish_manifest=True)
    return agent


def main() -> None:
    agent = build_agent()
    print(f"[sage] uAgent address: {agent.address}")
    agent.run()


if __name__ == "__main__":
    main()
