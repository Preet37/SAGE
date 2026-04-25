"""PeerMatchAgent — suggests study peers based on complementary mastery."""

from __future__ import annotations

from app.agents.base import Agent, AgentContext


class PeerMatchAgent(Agent):
    name = "peer_match"

    async def run(self, ctx: AgentContext) -> AgentContext:
        weak = {c["label"] for c in ctx.mastery if c.get("mastery", 0) < 0.5}
        if not weak:
            ctx.peers = []
            return ctx

        ctx.peers = [
            {"peer_id": f"peer-{i}", "complements": list(weak)[:2], "score": round(0.9 - i * 0.1, 2)}
            for i in range(min(3, len(weak)))
        ]
        self._emit(ctx, "response", {"matches": len(ctx.peers)})
        return ctx
