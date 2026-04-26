"""Wiki staging review endpoints.

The wiki enrichment pipeline writes new topic pages and concept-map updates to
``content/pedagogy-wiki/.pending/`` instead of mutating the canonical wiki
tree. This router exposes the staging queue so a maintainer can list pending
items, approve them (apply to the wiki), or reject them (delete the staged
file).
"""

from __future__ import annotations

import json
import logging
import re
import time
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from ..config import WIKI_DIR
from ..deps import get_current_user
from ..models.user import User

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/wiki/staging", tags=["wiki-staging"])

_PENDING_DIR = WIKI_DIR / ".pending"
_TOPICS_DIR = WIKI_DIR / "resources" / "by-topic"
_CONCEPT_MAP = WIKI_DIR / "concept-map.md"

# Filenames are written by the enrichment pipeline as
# ``{timestamp}_{type}_{slug}.json`` — we lock down what we'll resolve.
_SAFE_NAME = re.compile(r"^[A-Za-z0-9_.\-]+\.json$")


def _resolve_pending_file(filename: str) -> Path:
    if not _SAFE_NAME.match(filename):
        raise HTTPException(status_code=400, detail="Invalid filename")
    path = (_PENDING_DIR / filename).resolve()
    if not str(path).startswith(str(_PENDING_DIR.resolve())):
        raise HTTPException(status_code=400, detail="Invalid path")
    if not path.is_file():
        raise HTTPException(status_code=404, detail="Pending item not found")
    return path


@router.get("")
def list_pending(_user: User = Depends(get_current_user)):
    """List all wiki changes awaiting review."""
    if not _PENDING_DIR.is_dir():
        return {"items": []}
    items: list[dict] = []
    for path in sorted(_PENDING_DIR.glob("*.json")):
        try:
            payload = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError) as e:
            logger.warning("Skipping malformed pending file %s: %s", path.name, e)
            continue
        items.append({
            "filename": path.name,
            "type": payload.get("type", "unknown"),
            "topic_slug": payload.get("topic_slug", ""),
            "course": payload.get("course", ""),
            "timestamp": payload.get("timestamp", ""),
            # Preview only — full payload returned by GET /{filename}
            "summary": _summarize(payload),
        })
    return {"items": items}


@router.get("/{filename}")
def get_pending(filename: str, _user: User = Depends(get_current_user)):
    """Return the full payload of a pending item for review."""
    path = _resolve_pending_file(filename)
    return json.loads(path.read_text())


@router.post("/{filename}/approve")
def approve_pending(filename: str, _user: User = Depends(get_current_user)):
    """Apply a pending change to the canonical wiki and remove it from staging."""
    path = _resolve_pending_file(filename)
    payload = json.loads(path.read_text())
    item_type = payload.get("type")
    data = payload.get("data") or {}

    if item_type == "new_topic":
        slug = payload.get("topic_slug") or ""
        if not slug or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
            raise HTTPException(status_code=400, detail="Invalid topic_slug")
        _TOPICS_DIR.mkdir(parents=True, exist_ok=True)
        page_path = _TOPICS_DIR / f"{slug}.md"
        page_content = data.get("page_content", "")
        if page_content and not page_path.exists():
            page_path.write_text(page_content)
        # Append the concept-map entry if not already present.
        cm_entry = data.get("concept_map_entry", "")
        if cm_entry and _CONCEPT_MAP.exists():
            existing = _CONCEPT_MAP.read_text()
            if cm_entry.strip() and cm_entry not in existing:
                _CONCEPT_MAP.write_text(existing.rstrip() + "\n" + cm_entry)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown pending item type: {item_type!r}",
        )

    path.unlink(missing_ok=True)
    return {"status": "approved", "type": item_type, "filename": filename}


@router.post("/{filename}/reject")
def reject_pending(
    filename: str, _user: User = Depends(get_current_user),
):
    """Delete a pending item without applying it."""
    path = _resolve_pending_file(filename)
    path.unlink(missing_ok=True)
    return {"status": "rejected", "filename": filename}


def _summarize(payload: dict) -> str:
    data = payload.get("data") or {}
    if payload.get("type") == "new_topic":
        concepts = data.get("concepts") or []
        n = len(concepts)
        first = ", ".join(concepts[:3])
        suffix = f" (+{n - 3} more)" if n > 3 else ""
        return f"{n} concepts: {first}{suffix}" if concepts else "new topic page"
    return payload.get("type", "")


@router.get("/_stats/all", include_in_schema=False)
def stats(_user: User = Depends(get_current_user)):
    """Quick health snapshot — used by ops dashboards."""
    if not _PENDING_DIR.is_dir():
        return {"pending": 0, "oldest_age_seconds": 0}
    files = list(_PENDING_DIR.glob("*.json"))
    oldest = min((f.stat().st_mtime for f in files), default=time.time())
    return {
        "pending": len(files),
        "oldest_age_seconds": int(time.time() - oldest) if files else 0,
    }
