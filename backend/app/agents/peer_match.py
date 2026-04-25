"""PeerMatchAgent — real peer suggestions from StudentMastery table."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.base import Agent, AgentContext
from app.models.concept import StudentMastery
from app.models.user import User

log = logging.getLogger("sage.peer_match")

MASTERY_THRESHOLD = 0.75
ACTIVE_WITHIN_DAYS = 7
MAX_PEERS = 3


class PeerMatchAgent(Agent):
    name = "peer_match"

    async def run(self, ctx: AgentContext) -> AgentContext:
        weak_concepts = [c for c in ctx.mastery if c.get("mastery", 0) < 0.5]
        if not weak_concepts:
            ctx.peers = []
            return ctx

        weak_concept_ids = [c.get("concept_id") for c in weak_concepts if c.get("concept_id")]

        if not weak_concept_ids or not hasattr(ctx, "db") or ctx.db is None:
            ctx.peers = []
            self._emit(ctx, "response", {"matches": 0, "reason": "no_db_context"})
            return ctx

        db: AsyncSession = ctx.db
        cutoff = datetime.now(timezone.utc) - timedelta(days=ACTIVE_WITHIN_DAYS)
        current_user_id = getattr(ctx, "user_id", None)

        try:
            stmt = (
                select(StudentMastery, User)
                .join(User, User.id == StudentMastery.user_id)
                .where(
                    and_(
                        StudentMastery.concept_id.in_(weak_concept_ids),
                        StudentMastery.score >= MASTERY_THRESHOLD,
                        StudentMastery.is_mastered == True,
                        StudentMastery.last_seen >= cutoff,
                        StudentMastery.user_id != current_user_id,
                    )
                )
                .order_by(StudentMastery.score.desc())
                .limit(MAX_PEERS * 3)
            )
            results = await db.execute(stmt)
            rows = results.all()

            seen_users: dict[int, dict] = {}
            for mastery, user in rows:
                uid = mastery.user_id
                if uid not in seen_users or mastery.score > seen_users[uid]["mastery_score"]:
                    seen_users[uid] = {
                        "peer_id": uid,
                        "username": user.name or f"Learner #{uid}",
                        "mastery_score": round(mastery.score, 2),
                        "concept_id": mastery.concept_id,
                        "last_active": mastery.last_seen.isoformat() if mastery.last_seen else None,
                    }

            peers = list(seen_users.values())[:MAX_PEERS]
            ctx.peers = peers
            self._emit(ctx, "response", {"matches": len(peers)})

        except Exception as e:
            log.warning(f"PeerMatchAgent DB query failed: {e}")
            ctx.peers = []
            self._emit(ctx, "response", {"matches": 0, "reason": str(e)})

        return ctx
