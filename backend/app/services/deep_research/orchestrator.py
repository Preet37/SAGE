"""Orchestrator — runs the three agents end-to-end with a shared event queue.

Lifecycle for a research run:

  Research      → builds knowledge graph + identifies top authors
  Validator     → scores credibility from the graph
  Concierge     → enriches top authors and finds emails
  (paused)      → user picks who to email, hits POST /outreach
  Concierge     → sends emails via SendGrid, logs status

Each phase pushes events into an in-memory queue. The HTTP layer subscribes
to the queue and forwards to the browser via SSE, so the UI sees agents
working live.
"""
from __future__ import annotations

import asyncio
import json
from collections import defaultdict
from typing import Optional
from uuid import uuid4

from .agents.concierge_agent import ConciergeAgent
from .agents.research_agent import ResearchAgent
from .agents.validator_agent import ValidatorAgent
from .clients.apollo import ApolloClient
from .clients.hunter import HunterClient
from .clients.openalex import OpenAlexClient
from .clients.sendgrid import SendGridClient
from .clients.tavily import TavilyClient
from .protocol import (
    ExpertProfile,
    KnowledgeGraph,
    OutreachRequest,
    ResearchTask,
    StreamEvent,
)


class RunState:
    """In-memory state for one research run.

    Persisted snapshot lives in the DB (ResearchRun row); this class just
    coordinates live work + the event queue.
    """

    def __init__(self, run_id: str, topic: str) -> None:
        self.run_id = run_id
        self.topic = topic
        self.queue: asyncio.Queue[Optional[StreamEvent]] = asyncio.Queue()
        self.graph: KnowledgeGraph = KnowledgeGraph()
        self.experts: list[ExpertProfile] = []
        self.tavily_answer: Optional[str] = None
        self.validation: Optional[dict] = None
        self.top_authors: list[dict] = []
        self.done: bool = False

    async def emit(self, event: StreamEvent) -> None:
        await self.queue.put(event)

    async def close(self) -> None:
        self.done = True
        await self.queue.put(None)  # sentinel — terminates SSE


class DeepResearchOrchestrator:
    """One orchestrator per process. Holds clients + active runs."""

    def __init__(self) -> None:
        self.openalex = OpenAlexClient()
        self.tavily = TavilyClient()
        self.hunter = HunterClient()
        self.apollo = ApolloClient()
        self.sendgrid = SendGridClient()
        self.runs: dict[str, RunState] = {}
        self._tasks: dict[str, asyncio.Task] = defaultdict(lambda: None)  # type: ignore[arg-type]

    async def shutdown(self) -> None:
        await asyncio.gather(
            self.openalex.close(),
            self.tavily.close(),
            self.hunter.close(),
            self.apollo.close(),
            self.sendgrid.close(),
            return_exceptions=True,
        )

    def start_run(self, topic: str, depth: int = 2, max_papers: int = 25) -> str:
        run_id = uuid4().hex
        state = RunState(run_id, topic)
        self.runs[run_id] = state
        task = asyncio.create_task(self._run_pipeline(state, depth, max_papers))
        self._tasks[run_id] = task
        return run_id

    async def _run_pipeline(
        self, state: RunState, depth: int, max_papers: int
    ) -> None:
        try:
            research = ResearchAgent(self.openalex, self.tavily)
            validator = ValidatorAgent()
            concierge = ConciergeAgent(
                self.openalex, self.hunter, self.apollo, self.sendgrid
            )

            await state.emit(
                StreamEvent(
                    agent="orchestrator",
                    kind="phase",
                    payload={"phase": "research", "topic": state.topic},
                )
            )

            async for ev in research.run(
                ResearchTask(topic=state.topic, depth=depth, max_papers=max_papers)
            ):
                # Capture state for downstream agents
                if ev.kind == "tavily":
                    state.tavily_answer = ev.payload.get("answer")
                if ev.kind == "done" and ev.agent == "research":
                    g = ev.payload.get("graph") or {}
                    state.graph = KnowledgeGraph.model_validate(g) if g else state.graph
                    state.top_authors = ev.payload.get("top_authors", []) or []
                await state.emit(ev)

            # Reasoning loop hook: if no results, escalate or stop early.
            if not state.graph.nodes:
                await state.emit(
                    StreamEvent(
                        agent="orchestrator",
                        kind="phase",
                        payload={
                            "phase": "halt",
                            "reason": "no papers found — try a different topic",
                        },
                    )
                )
                return

            await state.emit(
                StreamEvent(
                    agent="orchestrator", kind="phase", payload={"phase": "validate"}
                )
            )
            async for ev in validator.run(
                state.topic, state.graph, state.tavily_answer
            ):
                if ev.kind == "validation":
                    state.validation = ev.payload
                await state.emit(ev)

            await state.emit(
                StreamEvent(
                    agent="orchestrator", kind="phase", payload={"phase": "concierge"}
                )
            )
            async for ev in concierge.discover_experts(state.top_authors):
                if ev.kind == "expert":
                    state.experts.append(ExpertProfile.model_validate(ev.payload))
                await state.emit(ev)

            await state.emit(
                StreamEvent(
                    agent="orchestrator",
                    kind="phase",
                    payload={
                        "phase": "ready_for_outreach",
                        "experts": [e.model_dump() for e in state.experts],
                    },
                )
            )
        except Exception as e:
            await state.emit(
                StreamEvent(
                    agent="orchestrator",
                    kind="error",
                    payload={"message": f"Pipeline error: {e}"},
                )
            )
        finally:
            await state.close()

    async def send_outreach(
        self,
        run_id: str,
        expert_id: str,
        subject: str,
        body: str,
    ) -> dict:
        state = self.runs.get(run_id)
        if not state:
            return {"sent": False, "reason": "run not found"}
        expert = next((e for e in state.experts if e.id == expert_id), None)
        if not expert:
            return {"sent": False, "reason": "expert not found in run"}
        concierge = ConciergeAgent(
            self.openalex, self.hunter, self.apollo, self.sendgrid
        )
        return await concierge.send_outreach(
            expert, OutreachRequest(expert_id=expert_id, subject=subject, body=body)
        )


# Single shared instance — keeps async clients alive across requests
orchestrator: Optional[DeepResearchOrchestrator] = None


def get_orchestrator() -> DeepResearchOrchestrator:
    global orchestrator
    if orchestrator is None:
        orchestrator = DeepResearchOrchestrator()
    return orchestrator


def serialize_event(event: StreamEvent) -> str:
    """Format a StreamEvent as an SSE data line."""
    return f"data: {json.dumps(event.model_dump())}\n\n"
