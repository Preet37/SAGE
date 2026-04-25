"""PedagogyAgent — chooses teaching strategy AND enforces Socratic rewriting.

Two responsibilities:
  1. `run()` (pre-Content): picks strategy based on mastery profile and writes
     `ctx.plan`. ContentAgent reads this hint to nudge the LLM.
  2. `socratize()` (post-Content): rewrites `ctx.answer` into a guided question
     when the strategy is socratic/scaffold. This is the actual Socratic
     enforcement — we don't trust the LLM to obey the nudge alone.
"""

from __future__ import annotations

import re

from app.agents.base import Agent, AgentContext


SOCRATIC_SYSTEM = (
    "You are a Socratic tutor. Rewrite the assistant's draft answer so it does "
    "NOT directly state the solution. Instead, surface ONE focused guiding "
    "question that nudges the learner toward the key insight. Keep it under "
    "3 sentences. End with a single '?'. Preserve any specific terminology "
    "used in the draft. Do not introduce new facts."
)

SCAFFOLD_SYSTEM = (
    "You are a scaffolding tutor for a struggling learner. Rewrite the draft "
    "so it: (1) states only the FIRST step toward the answer in plain language, "
    "(2) ends with one concrete sub-question the learner can attempt next. "
    "Under 4 sentences. Do not give away the full solution."
)


def _looks_like_question(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    return stripped.endswith("?") and len(re.findall(r"\?", stripped)) >= 1


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
            "ask_one_question": False if (strategy == "extend" or True) else True, # Defaulting to False for lesson plan
            "weak_concepts": [c["label"] for c in weak][:3],
            "expert_teacher_mode": True,
        }
        self._emit(ctx, "response", {"plan": ctx.plan})
        return ctx

    async def socratize(self, ctx: AgentContext) -> AgentContext:
        """Post-Content rewrite: enforce that the answer is a guided question."""
        strategy = ctx.plan.get("strategy", "socratic")
        if strategy == "extend" or ctx.plan.get("expert_teacher_mode"):
            self._emit(ctx, "response", {"socratized": False, "reason": "skip-socratize"})
            return ctx
        if not ctx.answer.strip():
            return ctx
        if strategy == "socratic" and _looks_like_question(ctx.answer):
            self._emit(ctx, "response", {"socratized": False, "reason": "already-question"})
            return ctx

        system = SCAFFOLD_SYSTEM if strategy == "scaffold" else SOCRATIC_SYSTEM
        user = (
            f"Learner asked: {ctx.user_message}\n\n"
            f"Draft answer to rewrite:\n{ctx.answer}"
        )
        try:
            rewritten = await self.llm.complete(system, user, max_tokens=220)
            rewritten = rewritten.strip()
        except Exception as e:
            self._emit(ctx, "error", {"socratize_failed": str(e)})
            return ctx

        if rewritten:
            original = ctx.answer
            ctx.answer = rewritten
            self._emit(
                ctx,
                "response",
                {
                    "socratized": True,
                    "strategy": strategy,
                    "before_chars": len(original),
                    "after_chars": len(rewritten),
                },
            )
        return ctx
