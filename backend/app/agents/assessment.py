"""AssessmentAgent — generates a check-for-understanding question."""

from __future__ import annotations

from app.agents.base import Agent, AgentContext


class AssessmentAgent(Agent):
    name = "assessment"

    async def run(self, ctx: AgentContext) -> AgentContext:
        weak_concepts = ctx.plan.get("weak_concepts", [])
        target = weak_concepts[0] if weak_concepts else None
        if not target and ctx.concept_map_delta:
            target = ctx.concept_map_delta[0]["label"]
        if not target:
            ctx.assessment = {"question": None, "skip": True}
            return ctx

        ctx.assessment = {
            "question": f"In your own words, what is the role of {target}?",
            "concept": target,
            "kind": "free_response",
            "skip": False,
        }
        self._emit(ctx, "response", {"target": target})
        return ctx
