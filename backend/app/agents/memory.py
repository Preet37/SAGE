"""AgentMemory — per-turn swarm trace persistence for debugging.

Each completed turn is written as a single JSON file under
`.sage_memory/swarm_traces/turn_<session>_<timestamp>.json`. This lets us
replay "what did each agent think" for any tutoring turn.

The store is intentionally append-only and best-effort: a memory write failure
must never break a tutoring turn.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from app.agents.base import AgentContext

log = logging.getLogger("sage.memory")

DEFAULT_ROOT = Path(".sage_memory") / "swarm_traces"


class AgentMemory:
    def __init__(self, root: Path | str = DEFAULT_ROOT):
        self.root = Path(root)
        try:
            self.root.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            log.warning("memory root %s unwritable: %s", self.root, e)

    def record_turn(self, ctx: AgentContext) -> Path | None:
        ts = int(time.time() * 1000)
        path = self.root / f"turn_{ctx.session_id}_{ts}.json"
        snapshot: dict[str, Any] = {
            "session_id": ctx.session_id,
            "user_id": ctx.user_id,
            "user_message": ctx.user_message,
            "plan": ctx.plan,
            "answer": ctx.answer,
            "verification": ctx.verification,
            "concept_map_delta": ctx.concept_map_delta,
            "assessment": ctx.assessment,
            "peers": ctx.peers,
            "progress_delta": ctx.progress_delta,
            "trace": [asdict(m) for m in ctx.trace],
            "timestamp_ms": ts,
        }
        try:
            path.write_text(json.dumps(snapshot, indent=2, default=str), encoding="utf-8")
            return path
        except OSError as e:
            log.warning("failed to persist swarm trace: %s", e)
            return None

    def list_recent(self, limit: int = 20) -> list[Path]:
        if not self.root.exists():
            return []
        files = sorted(self.root.glob("turn_*.json"), reverse=True)
        return files[:limit]
