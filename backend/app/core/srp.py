"""
SAGE Routing Protocol (SRP) — Arista track.
BGP-inspired multi-factor peer scoring with concept graph BFS fallback.

Score = mastery_delta×0.40 + recency×0.20 + style_compat×0.20 + novelty×0.20
"""
from __future__ import annotations

import math
import logging
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.concept import ConceptNode, ConceptEdge, StudentMastery
from app.models.user import User

log = logging.getLogger("sage.srp")

W_MASTERY_DELTA = 0.40
W_RECENCY       = 0.20
W_STYLE_COMPAT  = 0.20
W_NOVELTY       = 0.20

RECENCY_HALFLIFE_HOURS = 48.0
RECENCY_LAMBDA = math.log(2) / RECENCY_HALFLIFE_HOURS


@dataclass
class SrpCandidate:
    user_id: int
    username: str
    mastery_score: float
    last_active: Optional[datetime]
    match_history_count: int = 0

    mastery_delta: float = 0.0
    recency_score: float = 0.0
    style_compat: float = 0.0
    novelty_score: float = 0.0
    srp_score: float = 0.0

    routed_via: Optional[str] = None


@dataclass
class SrpResult:
    candidates: list[SrpCandidate] = field(default_factory=list)
    routing_path: list[str] = field(default_factory=list)
    used_bfs: bool = False
    target_concept: str = ""
    routed_concept: str = ""


def _recency(last_active: Optional[datetime]) -> float:
    if last_active is None:
        return 0.10
    now = datetime.now(timezone.utc)
    if last_active.tzinfo is None:
        last_active = last_active.replace(tzinfo=timezone.utc)
    hours = (now - last_active).total_seconds() / 3600
    return round(math.exp(-RECENCY_LAMBDA * hours), 4)


def _novelty(match_count: int) -> float:
    return {0: 1.0, 1: 0.6, 2: 0.3}.get(match_count, 0.1)


def _style_compat(student_mode: Optional[str], peer_mode: Optional[str]) -> float:
    if student_mode and peer_mode and student_mode == peer_mode:
        return 1.0
    return 0.5


def _srp_score(c: SrpCandidate) -> float:
    return (
        c.mastery_delta   * W_MASTERY_DELTA
      + c.recency_score   * W_RECENCY
      + c.style_compat    * W_STYLE_COMPAT
      + c.novelty_score   * W_NOVELTY
    )


async def find_peers_srp(
    db: AsyncSession,
    concept_id: int,
    requesting_user_id: int,
    requesting_mastery: float,
    requesting_teaching_mode: Optional[str],
    match_history: dict[int, int],
    top_k: int = 3,
) -> SrpResult:
    result = SrpResult()

    concept_result = await db.execute(select(ConceptNode).where(ConceptNode.id == concept_id))
    concept = concept_result.scalar_one_or_none()
    result.target_concept = concept.label if concept else f"concept_{concept_id}"

    candidates = await _query_candidates(
        db, concept_id, requesting_user_id, requesting_mastery,
        requesting_teaching_mode, match_history,
    )

    if candidates:
        result.candidates = sorted(candidates, key=lambda c: c.srp_score, reverse=True)[:top_k]
        result.routing_path = [result.target_concept]
        result.routed_concept = result.target_concept
        return result

    bfs_result = await _bfs_routing(
        db, concept_id, requesting_user_id, requesting_mastery,
        requesting_teaching_mode, match_history,
    )
    if bfs_result:
        candidates, path, routed_label = bfs_result
        result.candidates = sorted(candidates, key=lambda c: c.srp_score, reverse=True)[:top_k]
        result.routing_path = path
        result.routed_concept = routed_label
        result.used_bfs = True
        for c in result.candidates:
            c.routed_via = routed_label

    return result


async def _query_candidates(
    db: AsyncSession,
    concept_id: int,
    requesting_user_id: int,
    requesting_mastery: float,
    requesting_teaching_mode: Optional[str],
    match_history: dict[int, int],
) -> list[SrpCandidate]:
    from datetime import timedelta
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)

    stmt = (
        select(StudentMastery, User)
        .join(User, User.id == StudentMastery.user_id)
        .where(
            and_(
                StudentMastery.concept_id == concept_id,
                StudentMastery.score >= 0.75,
                StudentMastery.is_mastered == True,
                StudentMastery.last_seen >= cutoff,
                StudentMastery.user_id != requesting_user_id,
            )
        )
        .limit(20)
    )
    rows = (await db.execute(stmt)).all()

    candidates: list[SrpCandidate] = []
    seen_users: set[int] = set()

    for mastery, user in rows:
        if mastery.user_id in seen_users:
            continue
        seen_users.add(mastery.user_id)

        match_count = match_history.get(mastery.user_id, 0)
        peer_mode = getattr(user, "teaching_mode", None)

        c = SrpCandidate(
            user_id=mastery.user_id,
            username=user.name or f"Learner #{mastery.user_id}",
            mastery_score=mastery.score,
            last_active=mastery.last_seen,
            match_history_count=match_count,
        )
        c.mastery_delta = max(0.0, min(1.0, mastery.score - requesting_mastery))
        c.recency_score = _recency(mastery.last_seen)
        c.style_compat = _style_compat(requesting_teaching_mode, peer_mode)
        c.novelty_score = _novelty(match_count)
        c.srp_score = round(_srp_score(c), 4)
        candidates.append(c)

    return candidates


async def _bfs_routing(
    db: AsyncSession,
    start_concept_id: int,
    requesting_user_id: int,
    requesting_mastery: float,
    requesting_teaching_mode: Optional[str],
    match_history: dict[int, int],
    max_hops: int = 3,
) -> Optional[tuple[list[SrpCandidate], list[str], str]]:
    visited: set[int] = {start_concept_id}
    queue: deque[tuple[int, list[int]]] = deque([(start_concept_id, [start_concept_id])])

    while queue:
        current_id, path = queue.popleft()
        if len(path) > max_hops + 1:
            break

        edges_result = await db.execute(
            select(ConceptEdge).where(
                and_(
                    ConceptEdge.source_id == current_id,
                    ConceptEdge.edge_type == "requires",
                )
            )
        )
        edges = edges_result.scalars().all()

        for edge in edges:
            neighbor_id = edge.target_id
            if neighbor_id in visited:
                continue
            visited.add(neighbor_id)
            new_path = path + [neighbor_id]

            candidates = await _query_candidates(
                db, neighbor_id, requesting_user_id, requesting_mastery,
                requesting_teaching_mode, match_history,
            )
            if candidates:
                node_labels: list[str] = []
                for nid in new_path:
                    node_result = await db.execute(
                        select(ConceptNode).where(ConceptNode.id == nid)
                    )
                    node = node_result.scalar_one_or_none()
                    node_labels.append(node.label if node else f"concept_{nid}")

                routed_label = node_labels[-1]
                return candidates, node_labels, routed_label

            queue.append((neighbor_id, new_path))

    return None
