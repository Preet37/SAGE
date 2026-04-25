"""ProgressAgent — updates mastery deltas based on the verification report."""

from __future__ import annotations

from app.agents.base import Agent, AgentContext


class ProgressAgent(Agent):
    name = "progress"

    async def run(self, ctx: AgentContext) -> AgentContext:
        score = float(ctx.verification.get("score", 0.0))
        grounded = bool(ctx.verification.get("grounded", False))
        bump = 0.05 if grounded else -0.02
        bump += (score - 0.5) * 0.1

        deltas: dict[str, float] = {}
        for c in ctx.mastery:
            label = c["label"]
            cur = float(c.get("mastery", 0.0))
            deltas[label] = max(0.0, min(1.0, cur + bump)) - cur

        ctx.progress_delta = {"bump": round(bump, 4), "by_concept": deltas}
        self._emit(ctx, "response", {"bump": bump, "concepts": len(deltas)})
        return ctx
