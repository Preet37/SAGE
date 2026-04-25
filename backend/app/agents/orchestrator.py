"""Orchestrator — coordinates the 6-agent SAGE swarm.

Pipeline (per turn):
    Pedagogy → Content → ConceptMap → (Assessment ∥ PeerMatch ∥ Progress)

State is the shared `AgentContext`. The orchestrator is the only component that
sequences agents; agents themselves are stateless beyond what they write into
the context. This keeps inter-agent comms predictable and traceable.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from typing import AsyncIterator

from app.agents.assessment import AssessmentAgent
from app.agents.base import Agent, AgentContext, AgentMessage, LLM
from app.agents.concept_map import ConceptMapAgent
from app.agents.content import ContentAgent
from app.agents.peer_match import PeerMatchAgent
from app.agents.pedagogy import PedagogyAgent
from app.agents.progress import ProgressAgent
from app.core.verification import verify

log = logging.getLogger("sage.orchestrator")


class Orchestrator:
    def __init__(self, llm: LLM | None = None):
        shared = llm or LLM.from_env()
        self.pedagogy = PedagogyAgent(shared)
        self.content = ContentAgent(shared)
        self.concept_map = ConceptMapAgent(shared)
        self.assessment = AssessmentAgent(shared)
        self.peer_match = PeerMatchAgent(shared)
        self.progress = ProgressAgent(shared)

    async def _run_agent(self, agent: Agent, ctx: AgentContext) -> AgentContext:
        ctx.trace.append(AgentMessage("orchestrator", agent.name, "request", {}))
        try:
            return await agent.run(ctx)
        except Exception as e:
            log.exception("agent %s failed", agent.name)
            ctx.trace.append(
                AgentMessage("orchestrator", agent.name, "error", {"error": str(e)})
            )
            return ctx

    async def run_turn(self, ctx: AgentContext) -> AgentContext:
        """Execute the full pipeline once and return the populated context."""
        # 1. Plan
        ctx = await self._run_agent(self.pedagogy, ctx)
        # 2. Generate
        ctx = await self._run_agent(self.content, ctx)
        # 3. Verify (deterministic, not an agent)
        ctx.verification = verify(ctx.answer, ctx.sources).to_payload()
        # 4. Concept extraction (depends on answer)
        ctx = await self._run_agent(self.concept_map, ctx)
        # 5. Parallel: assessment, peer match, progress
        await asyncio.gather(
            self._run_agent(self.assessment, ctx),
            self._run_agent(self.peer_match, ctx),
            self._run_agent(self.progress, ctx),
        )
        return ctx

    async def stream_turn(self, ctx: AgentContext) -> AsyncIterator[tuple[str, dict]]:
        """Yield orchestration events as `(event_name, payload)` tuples.

        Compatible with the SSE pipeline in `routers/tutor.py`.
        """
        trace_id = str(uuid.uuid4())
        yield "agent_event", {"agent": "orchestrator", "phase": "start", "trace_id": trace_id}

        ctx = await self._run_agent(self.pedagogy, ctx)
        yield "agent_event", {"agent": "pedagogy", "phase": "done", "plan": ctx.plan}

        ctx = await self._run_agent(self.content, ctx)
        yield "agent_event", {"agent": "content", "phase": "done", "chars": len(ctx.answer)}

        ctx.verification = verify(ctx.answer, ctx.sources).to_payload()
        yield "verification", ctx.verification

        ctx = await self._run_agent(self.concept_map, ctx)
        yield "agent_event", {"agent": "concept_map", "phase": "done",
                              "delta": ctx.concept_map_delta}

        await asyncio.gather(
            self._run_agent(self.assessment, ctx),
            self._run_agent(self.peer_match, ctx),
            self._run_agent(self.progress, ctx),
        )
        yield "agent_event", {"agent": "assessment", "phase": "done", "data": ctx.assessment}
        yield "agent_event", {"agent": "peer_match",  "phase": "done", "peers": ctx.peers}
        yield "agent_event", {"agent": "progress",    "phase": "done",
                              "delta": ctx.progress_delta}
        yield "done", {"session_id": ctx.session_id, "ok": True,
                       "grounded": ctx.verification.get("grounded", False)}
