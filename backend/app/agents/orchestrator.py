"""
Agent Orchestrator — coordinates all 6 SAGE agents.
Called before each tutor response to assemble context.
Results are streamed to the frontend as agent_event SSE events.
"""
import asyncio
import json
from datetime import datetime
import logging
import uuid
from typing import AsyncGenerator, AsyncIterator, Optional

from app.agents.assessment import AssessmentAgent
from app.agents.base import Agent, AgentContext, AgentMessage, LLM, asi1_complete
from app.agents.concept_map import ConceptMapAgent
from app.agents.content import ContentAgent
from app.agents.memory import AgentMemory
from app.agents.peer_match import PeerMatchAgent
from app.agents.pedagogy import PedagogyAgent
from app.agents.progress import ProgressAgent
from app.core.verification import verify

log = logging.getLogger("sage.orchestrator")


class AgentOrchestrator:
    """Coordinates the SAGE agent swarm for a single tutor turn."""

    def __init__(self, user_id: int, lesson_id: int, question: str, history: list[dict]):
        self.user_id = user_id
        self.lesson_id = lesson_id
        self.question = question
        self.history = history
        self.results: dict = {}

    async def run(self) -> AsyncGenerator[dict, None]:
        """
        Run all agents in parallel and yield events as they complete.
        Returns final assembled context dict.
        """
        tasks = {
            "pedagogy": self._run_pedagogy_agent(),
            "content": self._run_content_agent(),
            "concept_map": self._run_concept_map_agent(),
            "assessment": self._run_assessment_agent(),
            "peer_match": self._run_peer_match_agent(),
            "progress": self._run_progress_agent(),
        }

        # Run all agents concurrently
        agent_results = await asyncio.gather(
            *tasks.values(),
            return_exceptions=True,
        )

        for name, result in zip(tasks.keys(), agent_results):
            if isinstance(result, Exception):
                self.results[name] = {"error": str(result)}
            else:
                self.results[name] = result

        return self.results

    async def _run_pedagogy_agent(self) -> dict:
        """Determine optimal teaching strategy for this student + question."""
        history_summary = ""
        if self.history:
            last = self.history[-3:]
            history_summary = "\n".join([f"{m['role']}: {m['content'][:100]}..." for m in last])

        prompt = f"""You are the SAGE Pedagogy Agent. Analyze this tutoring situation and recommend the optimal teaching strategy.

Student question: {self.question}
Recent conversation:
{history_summary}

Respond with JSON:
{{
  "recommended_mode": "default|eli5|analogy|code|deep_dive",
  "reasoning": "brief explanation",
  "engagement_level": "low|medium|high",
  "misconception_detected": true/false,
  "misconception_detail": "if any"
}}"""

        result = await asi1_complete(prompt, max_tokens=256)
        try:
            return json.loads(result)
        except Exception:
            return {"recommended_mode": "default", "reasoning": result}

    async def _run_content_agent(self) -> dict:
        """Analyze question to identify most relevant KB sections."""
        prompt = f"""You are the SAGE Content Agent. Analyze what KB content is most relevant for this question.

Question: {self.question}
Lesson ID: {self.lesson_id}

Respond with JSON:
{{
  "key_terms": ["term1", "term2"],
  "content_focus": "what aspect of the lesson to emphasize",
  "requires_external_search": true/false,
  "search_query": "if external search needed"
}}"""

        result = await asi1_complete(prompt, max_tokens=200)
        try:
            return json.loads(result)
        except Exception:
            return {"key_terms": [], "content_focus": result}

    async def _run_concept_map_agent(self) -> dict:
        """Identify which concept nodes this question touches."""
        prompt = f"""You are the SAGE Concept Map Agent. Identify concept nodes related to this question.

Question: {self.question}

Respond with JSON:
{{
  "concepts_touched": ["concept1", "concept2"],
  "suggested_mastery_update": 0.1,
  "next_concept_recommendation": "what to study after"
}}"""

        result = await asi1_complete(prompt, max_tokens=150)
        try:
            return json.loads(result)
        except Exception:
            return {"concepts_touched": [], "suggested_mastery_update": 0.0}

    async def _run_assessment_agent(self) -> dict:
        """Determine if a quiz should be generated with the response."""
        prompt = f"""You are the SAGE Assessment Agent. Decide if this tutor turn warrants a quiz question.

Student question: {self.question}
Conversation turns: {len(self.history)}

Respond with JSON:
{{
  "should_quiz": true/false,
  "quiz_timing": "now|after_explanation|end_of_session",
  "difficulty": "easy|medium|hard",
  "concept_to_test": "specific concept to assess"
}}"""

        result = await asi1_complete(prompt, max_tokens=150)
        try:
            return json.loads(result)
        except Exception:
            return {"should_quiz": False}

    async def _run_peer_match_agent(self) -> dict:
        """Check if peer learning would benefit this student right now."""
        prompt = f"""You are the SAGE Peer Match Agent. Assess if peer learning would help this student.

Question: {self.question}
History length: {len(self.history)}

Respond with JSON:
{{
  "peer_match_recommended": true/false,
  "reasoning": "brief",
  "optimal_peer_type": "mastered|co-learning"
}}"""

        result = await asi1_complete(prompt, max_tokens=150)
        try:
            return json.loads(result)
        except Exception:
            return {"peer_match_recommended": False}

    async def _run_progress_agent(self) -> dict:
        """Assess overall learning progress and recommend next steps."""
        prompt = f"""You are the SAGE Progress Agent. Analyze this student's learning trajectory.

Current question: {self.question}
Session turns: {len(self.history)}

Respond with JSON:
{{
  "progress_signal": "struggling|progressing|excelling",
  "recommended_next_topic": "what to tackle next",
  "estimated_mastery": 0.0,
  "encouragement": "brief motivational note"
}}"""

        result = await asi1_complete(prompt, max_tokens=200)
        try:
            return json.loads(result)
        except Exception:
            return {"progress_signal": "progressing", "encouragement": result}


class Orchestrator:
    def __init__(self, llm: Optional[LLM] = None, memory: Optional[AgentMemory] = None):
        shared = llm or LLM.from_env()
        self.pedagogy = PedagogyAgent(shared)
        self.content = ContentAgent(shared)
        self.concept_map = ConceptMapAgent(shared)
        self.assessment = AssessmentAgent(shared)
        self.peer_match = PeerMatchAgent(shared)
        self.progress = ProgressAgent(shared)
        self.memory = memory or AgentMemory()

    async def _run_agent(self, agent: Agent, ctx: AgentContext) -> AgentContext:
        ctx.trace.append(AgentMessage("orchestrator", agent.name, "request", {}))
        try:
            return await agent.run(ctx)
        except Exception as e:
            log.exception("agent %s failed", agent.name)
            ctx.trace.append(AgentMessage("orchestrator", agent.name, "error", {"error": str(e)}))
            return ctx

    async def run_turn(self, ctx: AgentContext) -> AgentContext:
        ctx = await self._run_agent(self.pedagogy, ctx)
        ctx = await self._run_agent(self.content, ctx)
        ctx.trace.append(AgentMessage("orchestrator", self.pedagogy.name, "socratize", {}))
        try:
            ctx = await self.pedagogy.socratize(ctx)
        except Exception as e:
            log.exception("socratize failed")
            ctx.trace.append(AgentMessage("orchestrator", "pedagogy", "error", {"error": str(e)}))
        ctx.verification = verify(ctx.answer, ctx.sources).to_payload()
        ctx = await self._run_agent(self.concept_map, ctx)
        await asyncio.gather(
            self._run_agent(self.assessment, ctx),
            self._run_agent(self.peer_match, ctx),
            self._run_agent(self.progress, ctx),
        )
        self.memory.record_turn(ctx)
        return ctx

    async def stream_turn(self, ctx: AgentContext) -> AsyncIterator[tuple[str, dict]]:
        trace_id = str(uuid.uuid4())
        yield "agent_event", {"agent": "orchestrator", "phase": "start", "trace_id": trace_id}
        ctx = await self.run_turn(ctx)
        yield "agent_event", {"agent": "pedagogy", "phase": "done", "plan": ctx.plan}
        yield "agent_event", {"agent": "content", "phase": "done", "chars": len(ctx.answer)}
        yield "verification", ctx.verification
        yield "agent_event", {"agent": "concept_map", "phase": "done", "delta": ctx.concept_map_delta}
        yield "agent_event", {"agent": "assessment", "phase": "done", "data": ctx.assessment}
        yield "agent_event", {"agent": "peer_match", "phase": "done", "peers": ctx.peers}
        yield "agent_event", {"agent": "progress", "phase": "done", "delta": ctx.progress_delta}
        yield "done", {
            "session_id": ctx.session_id,
            "ok": True,
            "grounded": ctx.verification.get("grounded", False),
        }
