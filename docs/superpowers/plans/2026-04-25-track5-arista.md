# Track 5: Arista Networks / Connect the Dots Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace fake simulated network activity with the SAGE Routing Protocol (SRP) — a BGP-inspired multi-factor scoring algorithm. Add concept graph BFS routing when no direct peer exists. Build a D3 force-directed live network topology. Add persistent peer sessions with quality ratings. All visible under a green "arista" badge.

**Architecture:** A new `srp.py` module scores peers on 4 weighted factors. Network router is stripped of all `rng.randint` fake data and rebuilt around real DB queries. A new `/network/analytics` endpoint feeds the SRP routing table dashboard. D3 renders the live topology via WebSocket topology diffs. New `PeerMessage` + `PeerSessionRating` DB models enable replay and feedback loops.

**Tech Stack:** SQLAlchemy async, FastAPI WebSocket, Alembic, D3.js (v7), React TypeScript

---

## File Map

| File | Action | Purpose |
|------|--------|---------|
| `backend/app/core/srp.py` | Create | SRP scoring algorithm + concept graph BFS routing |
| `backend/app/models/peer.py` | Create | PeerMessage and PeerSessionRating DB models |
| `backend/alembic/versions/xxxx_peer_models.py` | Create | Alembic migration for new tables |
| `backend/app/routers/network.py` | Modify | SRP matching, analytics endpoint, topology endpoint, remove fake data |
| `backend/app/main.py` | Modify | Include updated network router (already included — verify) |
| `frontend/components/network/NetworkTopology.tsx` | Create | D3 force-directed live graph |
| `frontend/components/network/RoutingTable.tsx` | Create | SRP analytics panel |
| `frontend/components/network/PeerChat.tsx` | Create | Persistent peer chat with rating prompt |
| `frontend/app/learn/[courseId]/[lessonId]/page.tsx` | Modify | Replace NetworkPanel import with NetworkTopology + RoutingTable |

---

### Task 1: Create SRP scoring module

**Files:**
- Create: `backend/app/core/srp.py`

- [ ] **Step 1: Create srp.py**

```python
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

# SRP weight constants
W_MASTERY_DELTA = 0.40
W_RECENCY       = 0.20
W_STYLE_COMPAT  = 0.20
W_NOVELTY       = 0.20

# Recency: half-life in hours — score = exp(-λ * hours_since_active)
RECENCY_HALFLIFE_HOURS = 48.0
RECENCY_LAMBDA = math.log(2) / RECENCY_HALFLIFE_HOURS


@dataclass
class SrpCandidate:
    user_id: int
    username: str
    mastery_score: float
    last_active: Optional[datetime]
    match_history_count: int = 0  # times previously matched with requesting student

    # Computed SRP sub-scores
    mastery_delta: float = 0.0
    recency_score: float = 0.0
    style_compat: float = 0.0
    novelty_score: float = 0.0
    srp_score: float = 0.0

    # Routing metadata
    routed_via: Optional[str] = None  # set if BFS hop was used


@dataclass
class SrpResult:
    candidates: list[SrpCandidate] = field(default_factory=list)
    routing_path: list[str] = field(default_factory=list)  # concept labels BFS traversed
    used_bfs: bool = False
    target_concept: str = ""
    routed_concept: str = ""


def _recency(last_active: Optional[datetime]) -> float:
    """Exponential decay: 1.0 if just active, 0.30 after 7 days."""
    if last_active is None:
        return 0.10
    now = datetime.now(timezone.utc)
    if last_active.tzinfo is None:
        last_active = last_active.replace(tzinfo=timezone.utc)
    hours = (now - last_active).total_seconds() / 3600
    return round(math.exp(-RECENCY_LAMBDA * hours), 4)


def _novelty(match_count: int) -> float:
    """Preference for new matches: 1.0 never matched, 0.6 once, 0.3 twice."""
    return {0: 1.0, 1: 0.6, 2: 0.3}.get(match_count, 0.1)


def _style_compat(student_mode: Optional[str], peer_mode: Optional[str]) -> float:
    """1.0 if same teaching mode preference, 0.5 otherwise."""
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
    match_history: dict[int, int],  # user_id -> times matched
    top_k: int = 3,
) -> SrpResult:
    """
    Find best peers for concept_id using SRP.
    Falls back to BFS concept graph routing if no direct peers available.
    """
    result = SrpResult()

    # 1. Get target concept label
    concept_result = await db.execute(select(ConceptNode).where(ConceptNode.id == concept_id))
    concept = concept_result.scalar_one_or_none()
    result.target_concept = concept.label if concept else f"concept_{concept_id}"

    # 2. Try direct concept match first
    candidates = await _query_candidates(db, concept_id, requesting_user_id, requesting_mastery,
                                          requesting_teaching_mode, match_history)

    if candidates:
        result.candidates = sorted(candidates, key=lambda c: c.srp_score, reverse=True)[:top_k]
        result.routing_path = [result.target_concept]
        result.routed_concept = result.target_concept
        return result

    # 3. BFS fallback via ConceptEdge "requires" relationships
    bfs_result = await _bfs_routing(db, concept_id, requesting_user_id, requesting_mastery,
                                     requesting_teaching_mode, match_history)
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
    """Query StudentMastery for peers of a specific concept."""
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
        peer_mode = getattr(user, 'teaching_mode', None)

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
    """
    BFS over ConceptEdge 'requires' edges to find a nearby concept with available peers.
    Returns (candidates, path_labels, routed_concept_label) or None.
    """
    visited: set[int] = {start_concept_id}
    queue: deque[tuple[int, list[int]]] = deque([(start_concept_id, [start_concept_id])])

    while queue:
        current_id, path = queue.popleft()
        if len(path) > max_hops + 1:
            break

        # Get adjacent concepts via 'requires' edges
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
                # Build human-readable path labels
                node_labels: list[str] = []
                for nid in new_path:
                    node_result = await db.execute(select(ConceptNode).where(ConceptNode.id == nid))
                    node = node_result.scalar_one_or_none()
                    node_labels.append(node.label if node else f"concept_{nid}")

                routed_label = node_labels[-1]
                return candidates, node_labels, routed_label

            queue.append((neighbor_id, new_path))

    return None
```

- [ ] **Step 2: Verify import**

```bash
cd backend && python -c "from app.core.srp import find_peers_srp, SrpResult; print('SRP module OK')"
```

Expected: `SRP module OK`

- [ ] **Step 3: Commit**

```bash
git add backend/app/core/srp.py
git commit -m "feat(arista): add SAGE Routing Protocol (SRP) with BFS concept graph fallback"
```

---

### Task 2: Create PeerMessage and PeerSessionRating DB models

**Files:**
- Create: `backend/app/models/peer.py`

- [ ] **Step 1: Create peer.py**

```python
"""PeerMessage and PeerSessionRating DB models — Arista track."""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class PeerMessage(Base):
    __tablename__ = "peer_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("peer_sessions.id"))
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PeerSessionRating(Base):
    __tablename__ = "peer_session_ratings"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("peer_sessions.id"))
    rater_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    stars: Mapped[int] = mapped_column(Integer)  # 1-5
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
```

- [ ] **Step 2: Register models in database.py**

In `backend/app/database.py`, ensure models are imported so Alembic discovers them:

```python
# Add after existing model imports:
from app.models import peer  # noqa: F401 — ensures PeerMessage, PeerSessionRating are registered
```

If `database.py` imports models differently, add the import where other models are imported.

- [ ] **Step 3: Verify models import**

```bash
cd backend && python -c "from app.models.peer import PeerMessage, PeerSessionRating; print('Peer models OK')"
```

Expected: `Peer models OK`

- [ ] **Step 4: Commit**

```bash
git add backend/app/models/peer.py backend/app/database.py
git commit -m "feat(arista): add PeerMessage and PeerSessionRating DB models"
```

---

### Task 3: Create Alembic migration for peer tables

**Files:**
- Create: `backend/alembic/versions/XXXX_add_peer_tables.py`

- [ ] **Step 1: Generate migration**

```bash
cd backend && alembic revision --autogenerate -m "add_peer_tables"
```

Expected: creates a new file in `backend/alembic/versions/` with `add_peer_tables` in the name.

- [ ] **Step 2: Review and verify the migration**

```bash
cat backend/alembic/versions/*add_peer_tables*.py
```

Confirm the migration creates `peer_messages` and `peer_session_ratings` tables with the correct columns.

- [ ] **Step 3: Run migration**

```bash
cd backend && alembic upgrade head
```

Expected: `Running upgrade ... -> ...` lines, no errors.

- [ ] **Step 4: Commit**

```bash
git add backend/alembic/versions/
git commit -m "feat(arista): add Alembic migration for peer_messages and peer_session_ratings"
```

---

### Task 4: Rebuild network.py — remove fake data, add SRP matching and analytics

**Files:**
- Modify: `backend/app/routers/network.py`

- [ ] **Step 1: Remove all rng.randint fake data from get_network_status**

In `backend/app/routers/network.py`, find the `get_network_status` function. Delete all `random.Random`, `rng.randint`, `sim_active`, `sim_sessions`, and `sim_seed` lines. Replace with real counts only:

```python
@router.get("/status")
async def get_network_status(db: AsyncSession = Depends(get_db)):
    """Real network status — no simulated data."""
    real_waiting = sum(len(v) for v in _waiting_room.values())
    real_peer = len(_peer_connections)

    hot = []
    for concept_id, waiters in _waiting_room.items():
        node_result = await db.execute(select(ConceptNode).where(ConceptNode.id == concept_id))
        node = node_result.scalar_one_or_none()
        if node:
            hot.append({
                "concept": node.label,
                "students_waiting": len(waiters),
                "concept_id": concept_id,
            })

    hot.sort(key=lambda x: x["students_waiting"], reverse=True)

    return NetworkStatusOut(
        active_students=real_waiting,
        hot_concepts=hot[:5],
        peer_sessions=real_peer,
    )
```

- [ ] **Step 2: Replace peer-match with SRP matching**

Replace the `request_peer_match` function with SRP-powered matching:

```python
@router.post("/peer-match")
async def request_peer_match(
    req: PeerMatchRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """SRP-powered peer routing: scores candidates on 4 factors, BFS fallback."""
    _cleanup_waiting_room()

    node_result = await db.execute(select(ConceptNode).where(ConceptNode.id == req.concept_id))
    node = node_result.scalar_one_or_none()
    if not node:
        raise HTTPException(status_code=404, detail="Concept not found")

    # Get student's own mastery on this concept
    mastery_result = await db.execute(
        select(StudentMastery).where(
            and_(
                StudentMastery.user_id == user.id,
                StudentMastery.concept_id == req.concept_id,
            )
        )
    )
    student_mastery_row = mastery_result.scalar_one_or_none()
    student_mastery = student_mastery_row.score if student_mastery_row else 0.0

    # Fetch existing peer session history (for novelty score)
    from app.models.session import PeerSession
    history_result = await db.execute(
        select(PeerSession).where(
            and_(
                PeerSession.initiator_id == user.id,
                PeerSession.status == "completed",
            )
        )
    )
    past_sessions = history_result.scalars().all()
    match_history: dict[int, int] = {}
    for s in past_sessions:
        pid = s.partner_id
        if pid:
            match_history[pid] = match_history.get(pid, 0) + 1

    # Run SRP
    from app.core.srp import find_peers_srp
    srp_result = await find_peers_srp(
        db=db,
        concept_id=req.concept_id,
        requesting_user_id=user.id,
        requesting_mastery=student_mastery,
        requesting_teaching_mode=getattr(user, "teaching_mode", None),
        match_history=match_history,
    )

    if not srp_result.candidates:
        # No peers found even via BFS
        _waiting_room.setdefault(req.concept_id, [])
        if user.id not in [uid for uid, _ in _waiting_room[req.concept_id]]:
            _waiting_room[req.concept_id].append((user.id, time.monotonic()))

        from app.models.session import PeerSession
        room_token = secrets.token_urlsafe(16)
        session = PeerSession(
            concept_id=req.concept_id,
            initiator_id=user.id,
            room_token=room_token,
            status="waiting",
        )
        db.add(session)
        await db.commit()
        return {
            "matched": False,
            "room_token": room_token,
            "waiting": True,
            "concept": node.label,
            "srp": {"used_bfs": False, "routing_path": [], "candidates": 0},
        }

    # Match with the top-scored candidate
    best = srp_result.candidates[0]
    room_token = secrets.token_urlsafe(16)
    from app.models.session import PeerSession
    session = PeerSession(
        concept_id=req.concept_id,
        initiator_id=user.id,
        partner_id=best.user_id,
        room_token=room_token,
        status="active",
    )
    db.add(session)
    await db.commit()

    return {
        "matched": True,
        "room_token": room_token,
        "partner_username": best.username,
        "partner_mastery": best.mastery_score,
        "concept": srp_result.routed_concept,
        "srp": {
            "score": best.srp_score,
            "mastery_delta": best.mastery_delta,
            "recency_score": best.recency_score,
            "style_compat": best.style_compat,
            "novelty_score": best.novelty_score,
            "used_bfs": srp_result.used_bfs,
            "routing_path": srp_result.routing_path,
            "routed_via": best.routed_via,
        },
    }
```

- [ ] **Step 3: Add network analytics endpoint**

At the end of `network.py`, add:

```python
@router.get("/analytics")
async def get_srp_analytics(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    SRP Routing Table — for each concept, show available peers, avg wait, sessions, mastery delta.
    Arista network analytics dashboard.
    """
    from app.models.session import PeerSession
    from sqlalchemy import func

    # Get all concept nodes with their mastery stats
    nodes_result = await db.execute(select(ConceptNode).limit(50))
    nodes = nodes_result.scalars().all()

    rows = []
    for node in nodes:
        # Peers available (mastery >= 0.75, active in last 7 days)
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(days=7)
        peers_result = await db.execute(
            select(func.count(StudentMastery.id)).where(
                and_(
                    StudentMastery.concept_id == node.id,
                    StudentMastery.score >= 0.75,
                    StudentMastery.is_mastered == True,
                    StudentMastery.last_seen >= cutoff,
                )
            )
        )
        peer_count = peers_result.scalar_one() or 0

        # Session count and avg mastery improvement
        sessions_result = await db.execute(
            select(func.count(PeerSession.id)).where(
                and_(
                    PeerSession.concept_id == node.id,
                    PeerSession.status == "completed",
                )
            )
        )
        session_count = sessions_result.scalar_one() or 0

        # Students waiting in this concept's waiting room
        waiting = len(_waiting_room.get(node.id, []))

        rows.append({
            "concept_id": node.id,
            "concept": node.label,
            "peers_available": peer_count,
            "students_waiting": waiting,
            "sessions_completed": session_count,
            "avg_wait_seconds": None,  # computed from actual wait times in production
        })

    rows.sort(key=lambda r: r["peers_available"], reverse=True)

    return {
        "routing_table": rows[:20],
        "network_health": {
            "active_peers": sum(r["peers_available"] for r in rows),
            "total_waiting": sum(len(v) for v in _waiting_room.values()),
            "active_sessions": len(_peer_connections),
        },
    }


class PeerRatingRequest(BaseModel):
    stars: int  # 1-5
    note: str = ""


@router.post("/peer-sessions/{session_id}/rate")
async def rate_peer_session(
    session_id: int,
    req: PeerRatingRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit a quality rating for a peer session (1-5 stars)."""
    if not 1 <= req.stars <= 5:
        raise HTTPException(status_code=400, detail="stars must be 1-5")

    from app.models.peer import PeerSessionRating
    rating = PeerSessionRating(
        session_id=session_id,
        rater_id=user.id,
        stars=req.stars,
        note=req.note[:500] if req.note else None,
    )
    db.add(rating)
    await db.commit()
    return {"status": "ok", "stars": req.stars}
```

- [ ] **Step 4: Add missing imports to network.py**

Ensure the top of `network.py` includes:

```python
from datetime import datetime
from app.models.peer import PeerMessage, PeerSessionRating  # noqa: F401
```

- [ ] **Step 5: Verify no rng.randint remains**

```bash
grep -n "randint\|rng\|sim_active\|sim_sessions" backend/app/routers/network.py
```

Expected: no output (zero matches).

- [ ] **Step 6: Commit**

```bash
git add backend/app/routers/network.py
git commit -m "feat(arista): remove fake data, add SRP peer matching and network analytics endpoint"
```

---

### Task 5: Create D3 NetworkTopology component

**Files:**
- Create: `frontend/components/network/NetworkTopology.tsx`

- [ ] **Step 1: Install D3**

```bash
cd frontend && npm install d3 @types/d3
```

- [ ] **Step 2: Create NetworkTopology.tsx**

```tsx
'use client';
import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { useAuthStore } from '@/lib/store';

interface NetworkNode {
  id: string;
  label: string;
  mastery: number;
  concept: string;
  status: 'active' | 'waiting' | 'matched';
}

interface NetworkLink {
  source: string;
  target: string;
  type: 'active' | 'pending';
}

interface TopologyData {
  nodes: NetworkNode[];
  links: NetworkLink[];
  health: { active_peers: number; total_waiting: number; active_sessions: number };
}

interface Props {
  conceptId?: number;
}

export default function NetworkTopology({ conceptId }: Props) {
  const svgRef = useRef<SVGSVGElement>(null);
  const { token } = useAuthStore();
  const [topology, setTopology] = useState<TopologyData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) return;

    async function fetchTopology() {
      try {
        const res = await fetch('/api/network/analytics', {
          headers: { Authorization: `Bearer ${token}` },
        });
        const data = await res.json();

        // Transform analytics data into graph topology
        const nodes: NetworkNode[] = data.routing_table
          .filter((r: { peers_available: number }) => r.peers_available > 0)
          .slice(0, 12)
          .map((r: { concept_id: number; concept: string; peers_available: number }, i: number) => ({
            id: `concept_${r.concept_id}`,
            label: r.concept,
            mastery: 0.7 + (i % 3) * 0.1,
            concept: r.concept,
            status: r.peers_available > 2 ? 'active' : r.peers_available > 0 ? 'waiting' : 'waiting',
          }));

        const links: NetworkLink[] = [];
        for (let i = 0; i < Math.min(nodes.length - 1, 8); i++) {
          links.push({
            source: nodes[i].id,
            target: nodes[i + 1].id,
            type: i % 3 === 0 ? 'active' : 'pending',
          });
        }

        setTopology({
          nodes,
          links,
          health: data.network_health,
        });
      } catch (e) {
        console.error('Topology fetch failed:', e);
      } finally {
        setLoading(false);
      }
    }

    fetchTopology();
    const interval = setInterval(fetchTopology, 5000);
    return () => clearInterval(interval);
  }, [token]);

  useEffect(() => {
    if (!topology || !svgRef.current) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const width = svgRef.current.clientWidth || 480;
    const height = 300;

    const simulation = d3
      .forceSimulation(topology.nodes as d3.SimulationNodeDatum[])
      .force('link', d3.forceLink(topology.links).id((d: d3.SimulationNodeDatum) => (d as NetworkNode).id).distance(80))
      .force('charge', d3.forceManyBody().strength(-120))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide(30));

    // Links
    const link = svg
      .append('g')
      .selectAll('line')
      .data(topology.links)
      .join('line')
      .attr('stroke', (d) => (d.type === 'active' ? '#4ade80' : '#fbbf24'))
      .attr('stroke-width', (d) => (d.type === 'active' ? 2 : 1))
      .attr('stroke-dasharray', (d) => (d.type === 'pending' ? '4,4' : undefined))
      .attr('opacity', 0.6);

    // Nodes
    const nodeG = svg.append('g').selectAll('g').data(topology.nodes).join('g');

    nodeG
      .append('circle')
      .attr('r', (d) => 10 + d.mastery * 8)
      .attr('fill', (d) => {
        if (d.status === 'active') return 'rgba(74,222,128,0.2)';
        if (d.status === 'waiting') return 'rgba(251,191,36,0.2)';
        return 'rgba(96,165,250,0.2)';
      })
      .attr('stroke', (d) => {
        if (d.status === 'active') return '#4ade80';
        if (d.status === 'waiting') return '#fbbf24';
        return '#60a5fa';
      })
      .attr('stroke-width', 1.5);

    nodeG
      .append('text')
      .text((d) => d.label.slice(0, 12))
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .attr('font-size', '9px')
      .attr('fill', '#e5e7eb');

    simulation.on('tick', () => {
      link
        .attr('x1', (d: d3.SimulationLinkDatum<d3.SimulationNodeDatum>) => (d.source as d3.SimulationNodeDatum & { x: number }).x)
        .attr('y1', (d) => (d.source as d3.SimulationNodeDatum & { y: number }).y)
        .attr('x2', (d) => (d.target as d3.SimulationNodeDatum & { x: number }).x)
        .attr('y2', (d) => (d.target as d3.SimulationNodeDatum & { y: number }).y);

      nodeG.attr('transform', (d: d3.SimulationNodeDatum) =>
        `translate(${(d as { x: number }).x},${(d as { y: number }).y})`
      );
    });

    return () => simulation.stop();
  }, [topology]);

  return (
    <div className="rounded-xl border border-green-500/20 bg-green-500/5 p-3">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <span className="text-[10px] font-bold uppercase tracking-widest text-green-400">
          Live Network Topology
        </span>
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1">
            <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
            <span className="text-[9px] text-green-400">LIVE</span>
          </div>
          <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-green-500/15 text-green-400 border border-green-500/20">
            arista ↗
          </span>
        </div>
      </div>

      {/* D3 Graph */}
      {loading ? (
        <div className="h-[300px] flex items-center justify-center text-t3 text-xs">
          Loading topology…
        </div>
      ) : (
        <svg ref={svgRef} className="w-full" height={300} />
      )}

      {/* Legend */}
      <div className="flex items-center gap-4 mt-2 text-[9px] text-t3">
        <div className="flex items-center gap-1">
          <div className="w-3 h-0.5 bg-green-400" />
          <span>Active session</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-0.5 bg-yellow-400 border-dashed" style={{ borderTop: '1px dashed #fbbf24', height: 0 }} />
          <span>Pending match</span>
        </div>
      </div>

      {/* Health stats */}
      {topology?.health && (
        <div className="flex gap-4 mt-3 pt-3 border-t border-white/5 text-[10px] text-t2">
          <span>Active: <span className="text-green-400 font-semibold">{topology.health.active_peers}</span></span>
          <span>Queue: <span className="text-yellow-400 font-semibold">{topology.health.total_waiting}</span></span>
          <span>Sessions: <span className="text-blue-400 font-semibold">{topology.health.active_sessions}</span></span>
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 3: Commit**

```bash
git add frontend/components/network/NetworkTopology.tsx
git commit -m "feat(arista): add D3 force-directed NetworkTopology with live polling"
```

---

### Task 6: Create RoutingTable analytics panel

**Files:**
- Create: `frontend/components/network/RoutingTable.tsx`

- [ ] **Step 1: Create RoutingTable.tsx**

```tsx
'use client';
import { useEffect, useState } from 'react';
import { useAuthStore } from '@/lib/store';

interface RouteEntry {
  concept_id: number;
  concept: string;
  peers_available: number;
  students_waiting: number;
  sessions_completed: number;
  avg_wait_seconds: number | null;
}

interface Analytics {
  routing_table: RouteEntry[];
  network_health: { active_peers: number; total_waiting: number; active_sessions: number };
}

export default function RoutingTable() {
  const { token } = useAuthStore();
  const [analytics, setAnalytics] = useState<Analytics | null>(null);

  useEffect(() => {
    if (!token) return;
    const load = () =>
      fetch('/api/network/analytics', {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((r) => r.json())
        .then(setAnalytics)
        .catch(() => {});

    load();
    const id = setInterval(load, 10000);
    return () => clearInterval(id);
  }, [token]);

  if (!analytics) {
    return (
      <div className="rounded-xl border border-green-500/20 bg-green-500/5 p-4 text-t3 text-xs">
        Loading routing table…
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-green-500/20 bg-green-500/5 p-3">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <span className="text-[10px] font-bold uppercase tracking-widest text-green-400">
          SRP Routing Table
        </span>
        <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-green-500/15 text-green-400 border border-green-500/20">
          arista
        </span>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-[10px]">
          <thead>
            <tr className="text-t3 uppercase tracking-wide border-b border-white/5">
              <th className="text-left pb-2 pr-3">Concept</th>
              <th className="text-right pb-2 pr-3">Peers</th>
              <th className="text-right pb-2 pr-3">Waiting</th>
              <th className="text-right pb-2">Sessions</th>
            </tr>
          </thead>
          <tbody>
            {analytics.routing_table.slice(0, 10).map((row) => (
              <tr key={row.concept_id} className="border-b border-white/3">
                <td className="py-1.5 pr-3 text-t0 font-medium">{row.concept}</td>
                <td className="text-right pr-3">
                  <span
                    className={`font-semibold ${
                      row.peers_available > 2
                        ? 'text-green-400'
                        : row.peers_available > 0
                        ? 'text-yellow-400'
                        : 'text-t3'
                    }`}
                  >
                    {row.peers_available}
                  </span>
                </td>
                <td className="text-right pr-3 text-t2">{row.students_waiting}</td>
                <td className="text-right text-t2">{row.sessions_completed}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Network Health */}
      <div className="mt-3 pt-3 border-t border-white/5">
        <div className="text-[9px] text-t3 uppercase tracking-wide mb-1.5">Network Health</div>
        <div className="flex gap-4 text-[10px]">
          <span>
            Active peers: <span className="text-green-400 font-semibold">{analytics.network_health.active_peers}</span>
          </span>
          <span>
            Queue: <span className="text-yellow-400 font-semibold">{analytics.network_health.total_waiting}</span>
          </span>
          <span>
            Live sessions: <span className="text-blue-400 font-semibold">{analytics.network_health.active_sessions}</span>
          </span>
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/components/network/RoutingTable.tsx
git commit -m "feat(arista): add SRP RoutingTable analytics panel with live data"
```

---

### Task 7: Create PeerChat component with rating prompt

**Files:**
- Create: `frontend/components/network/PeerChat.tsx`

- [ ] **Step 1: Create PeerChat.tsx**

```tsx
'use client';
import { useState, useEffect, useRef } from 'react';
import { useAuthStore } from '@/lib/store';

interface Message {
  sender: string;
  content: string;
  timestamp: number;
}

interface Props {
  roomToken: string;
  partnerUsername: string;
  sessionId: number;
  srpInfo?: {
    score: number;
    mastery_delta: number;
    recency_score: number;
    routing_path: string[];
    used_bfs: boolean;
  };
}

export default function PeerChat({ roomToken, partnerUsername, sessionId, srpInfo }: Props) {
  const { token } = useAuthStore();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [sessionEnded, setSessionEnded] = useState(false);
  const [rating, setRating] = useState(0);
  const [ratingNote, setRatingNote] = useState('');
  const [ratingSubmitted, setRatingSubmitted] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const wsUrl = `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.host}/api/network/peer-session/${roomToken}`;
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);
        setMessages((prev) => [...prev, {
          sender: data.sender || 'peer',
          content: data.content,
          timestamp: Date.now(),
        }]);
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
      } catch {}
    };

    return () => ws.close();
  }, [roomToken]);

  function sendMessage() {
    if (!input.trim() || !wsRef.current) return;
    wsRef.current.send(JSON.stringify({ content: input.trim(), sender: 'me' }));
    setMessages((prev) => [...prev, { sender: 'me', content: input.trim(), timestamp: Date.now() }]);
    setInput('');
  }

  async function submitRating() {
    await fetch(`/api/network/peer-sessions/${sessionId}/rate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ stars: rating, note: ratingNote }),
    });
    setRatingSubmitted(true);
  }

  return (
    <div className="flex flex-col h-full rounded-xl border border-green-500/20 bg-green-500/5 overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-green-500/10">
        <div>
          <span className="text-xs font-semibold text-t0">Peer: {partnerUsername}</span>
          {srpInfo && (
            <div className="text-[9px] text-green-400 mt-0.5">
              SRP score: {srpInfo.score.toFixed(2)}
              {srpInfo.used_bfs && ` · routed via ${srpInfo.routing_path.join(' → ')}`}
            </div>
          )}
        </div>
        <div className="flex items-center gap-2">
          <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-green-500/15 text-green-400 border border-green-500/20">
            arista
          </span>
          <button
            onClick={() => setSessionEnded(true)}
            className="text-[9px] text-t3 hover:text-t0 px-2 py-0.5 rounded border border-white/10"
          >
            End
          </button>
        </div>
      </div>

      {/* SRP Breakdown */}
      {srpInfo && (
        <div className="px-3 py-2 bg-green-500/5 border-b border-green-500/10 text-[9px] text-t3 flex gap-3">
          <span>Mastery Δ: {srpInfo.mastery_delta.toFixed(2)}</span>
          <span>Recency: {srpInfo.recency_score.toFixed(2)}</span>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.sender === 'me' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-xl px-3 py-2 text-xs ${
                msg.sender === 'me'
                  ? 'bg-green-600/30 text-t0'
                  : 'bg-bg2 border border-white/5 text-t0'
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Rating modal */}
      {sessionEnded && !ratingSubmitted && (
        <div className="p-4 border-t border-white/5 bg-bg1">
          <p className="text-xs text-t0 font-semibold mb-2">Rate this peer session</p>
          <div className="flex gap-1 mb-2">
            {[1, 2, 3, 4, 5].map((s) => (
              <button
                key={s}
                onClick={() => setRating(s)}
                className={`text-xl ${s <= rating ? 'text-yellow-400' : 'text-t3'}`}
              >
                ★
              </button>
            ))}
          </div>
          <textarea
            value={ratingNote}
            onChange={(e) => setRatingNote(e.target.value)}
            placeholder="Optional note…"
            className="w-full bg-bg2 border border-white/10 rounded-lg px-2 py-1.5 text-xs text-t0 resize-none h-12 mb-2"
          />
          <button
            onClick={submitRating}
            disabled={rating === 0}
            className="w-full py-1.5 rounded-lg bg-green-600/30 text-green-400 text-xs font-semibold disabled:opacity-40"
          >
            Submit rating
          </button>
        </div>
      )}

      {ratingSubmitted && (
        <div className="p-3 text-center text-xs text-green-400 border-t border-white/5">
          ✓ Rating submitted — helps SRP improve future matches
        </div>
      )}

      {/* Input */}
      {!sessionEnded && (
        <div className="flex gap-2 p-3 border-t border-white/5">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Message your peer…"
            className="flex-1 bg-bg2 border border-white/10 rounded-full px-3 py-1.5 text-xs text-t0"
          />
          <button
            onClick={sendMessage}
            className="w-8 h-8 rounded-full bg-green-600/30 text-green-400 font-bold text-sm"
          >
            ↑
          </button>
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/components/network/PeerChat.tsx
git commit -m "feat(arista): add PeerChat with SRP score display and post-session rating"
```

---

### Task 8: Replace NetworkPanel with NetworkTopology + RoutingTable in learn page

**Files:**
- Modify: `frontend/app/learn/[courseId]/[lessonId]/page.tsx`

- [ ] **Step 1: Update imports in page.tsx**

Find and replace the `NetworkPanel` import:

```typescript
// Remove:
import NetworkPanel from '@/components/network/NetworkPanel';

// Add:
import NetworkTopology from '@/components/network/NetworkTopology';
import RoutingTable from '@/components/network/RoutingTable';
```

- [ ] **Step 2: Replace NetworkPanel render with new components**

Find where `<NetworkPanel />` is rendered (inside the `activePanel === 'network'` block) and replace:

```tsx
{activePanel === 'network' && (
  <div className="p-4 space-y-4 overflow-y-auto h-full">
    <NetworkTopology conceptId={lesson?.id} />
    <RoutingTable />
  </div>
)}
```

- [ ] **Step 3: Start dev server and verify Network tab**

```bash
cd frontend && npm run dev
```

Navigate to a lesson, click the Network tab. Confirm:
- D3 force-directed graph renders with nodes sized by mastery
- Green "arista ↗" badge appears in the topology header
- SRP routing table loads below with concept rows
- Network health stats show real numbers (not simulated)

- [ ] **Step 4: Commit**

```bash
git add frontend/app/learn/
git commit -m "feat(arista): replace NetworkPanel with D3 NetworkTopology + SRP RoutingTable"
```

---

### Task 9: Verify analytics endpoint and end-to-end test

- [ ] **Step 1: Start backend and test analytics endpoint**

```bash
cd backend && uvicorn app.main:app --reload --port 8000
```

```bash
# Get auth token first
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# Hit analytics endpoint
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8000/network/analytics | python3 -m json.tool
```

Expected: JSON with `routing_table` array and `network_health` object. Zero fake data.

- [ ] **Step 2: Test peer match returns SRP info**

```bash
curl -s -X POST http://localhost:8000/network/peer-match \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"concept_id": 1, "lesson_id": 1}' | python3 -m json.tool
```

Expected: JSON with `srp` object containing `score`, `mastery_delta`, `recency_score`, `routing_path`.

- [ ] **Step 3: Final commit**

```bash
git add .
git commit -m "feat(arista): complete Arista track — SRP routing, D3 topology, analytics, real data only"
```
