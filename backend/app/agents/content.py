"""ContentAgent — produces the actual answer text using LLM + retrieved sources."""

from __future__ import annotations

from app.agents.base import Agent, AgentContext
from app.core.prompt_builder import A11yProfile, ConceptMastery, build_system_prompt


class ContentAgent(Agent):
    name = "content"

    async def run(self, ctx: AgentContext) -> AgentContext:
        a11y_kwargs = {
            k: v for k, v in ctx.a11y.items() if k in A11yProfile.__dataclass_fields__
        }
        a11y = A11yProfile(**a11y_kwargs)
        mastery = [
            ConceptMastery(label=m["label"], mastery=m.get("mastery", 0.0))
            for m in ctx.mastery
        ]
        teaching_mode = ctx.a11y.get("teaching_mode", "default")
        system = build_system_prompt(
            a11y=a11y,
            mastery=mastery,
            sources=ctx.sources,
            teaching_mode=teaching_mode,
        )

        strategy = ctx.plan.get("strategy", "socratic")
        nudge = {
            "scaffold": "Break it into the smallest first step. Ask one tiny question.",
            "extend":   "Push the learner with a synthesis question that builds on mastery.",
            "socratic": "Ask one focused guiding question grounded in the sources.",
        }[strategy]

        user = f"Learner asked: {ctx.user_message}\n\nTeaching directive: {nudge}"
        ctx.answer = await self.llm.complete(system, user)
        self._emit(ctx, "response", {"chars": len(ctx.answer), "strategy": strategy, "mode": teaching_mode})
        return ctx
