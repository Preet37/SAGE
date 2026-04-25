"""PedagogyAgent — chooses teaching strategy for the turn."""

from __future__ import annotations

from app.agents.base import Agent, AgentContext


class PedagogyAgent(Agent):
    name = "pedagogy"

    async def run(self, ctx: AgentContext) -> AgentContext:
        weak = [c for c in ctx.mastery if c.get("mastery", 0) < 0.5]
        if weak:
            strategy = "scaffold"
            depth = "shallow"
        elif any(c.get("mastery", 0) >= 0.8 for c in ctx.mastery):
            strategy = "extend"
            depth = "deep"
        else:
            strategy = "socratic"
            depth = "moderate"

        ctx.plan = {
            "strategy": strategy,
            "depth": depth,
            "ask_one_question": True,
            "weak_concepts": [c["label"] for c in weak][:3],
        }
        self._emit(ctx, "response", {"plan": ctx.plan})
        return ctx
