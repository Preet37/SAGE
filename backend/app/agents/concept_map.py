"""ConceptMapAgent — extracts concept nodes/edges from the turn."""

from __future__ import annotations

import re

from app.agents.base import Agent, AgentContext

_NOUN_PHRASE = re.compile(r"\b([A-Z][a-z]{3,}(?:\s+[a-z]{3,})?)\b")


class ConceptMapAgent(Agent):
    name = "concept_map"

    async def run(self, ctx: AgentContext) -> AgentContext:
        text = f"{ctx.user_message}\n{ctx.answer}"
        seen: dict[str, int] = {}
        for m in _NOUN_PHRASE.finditer(text):
            label = m.group(1).strip()
            seen[label] = seen.get(label, 0) + 1

        existing = {c["label"] for c in ctx.mastery}
        delta = [
            {"label": label, "summary": "", "mastery": 0.1, "parent_label": None}
            for label, count in sorted(seen.items(), key=lambda kv: -kv[1])
            if label not in existing
        ][:5]

        ctx.concept_map_delta = delta
        self._emit(ctx, "response", {"new_nodes": len(delta)})
        return ctx
