"""Arista 'Connect the Dots' track — peer matching + resource router.

Two surfaces:

1. Peer presence + WebSocket signalling (`/network/presence`, `/network/ws`).
   Students studying the same lesson are matched and can see each other live.
   We use a WebSocket pub/sub fanout so updates feel instant; the DB row is
   the source of truth so peer state survives reconnects.

2. Resource router (`/network/resources`). Pulls related content from public
   APIs (arXiv, GitHub, YouTube) keyed off the lesson concepts, ranks it by
   relevance, and routes a unified feed back to the user. Heavy fetches are
   cached in `ResourceCacheEntry` to stay polite to upstream rate limits.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import quote_plus

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlmodel import Session, select

from ..config import get_settings
from ..db import engine, get_session
from ..deps import get_current_user
from ..models.learning import Lesson
from ..models.network import PeerPresence, ResourceCacheEntry
from ..models.user import User
from ..services.semantic_memory import tokenize

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/network", tags=["network"])


# ── Peer presence ──────────────────────────────────────────────

ACTIVE_WINDOW = timedelta(minutes=3)

ALLOWED_STATUSES = {"studying", "stuck", "review", "idle"}


class HeartbeatRequest(BaseModel):
    lesson_id: Optional[str] = None
    status: str = "studying"
    note: str = ""
    looking_for_pair: bool = False
    display_name: str = ""


class PeerOut(BaseModel):
    user_id: str
    display_name: str
    lesson_id: Optional[str]
    status: str
    note: str
    looking_for_pair: bool
    last_seen: datetime


class PresenceResponse(BaseModel):
    me: PeerOut
    peers_on_lesson: list[PeerOut]
    other_peers_online: list[PeerOut]


def _peer_out(p: PeerPresence) -> PeerOut:
    return PeerOut(
        user_id=p.user_id, display_name=p.display_name or "Anonymous",
        lesson_id=p.lesson_id, status=p.status, note=p.note,
        looking_for_pair=p.looking_for_pair, last_seen=p.last_seen,
    )


def _is_active(p: PeerPresence) -> bool:
    return (datetime.utcnow() - p.last_seen) <= ACTIVE_WINDOW


@router.post("/presence", response_model=PresenceResponse)
def heartbeat(
    req: HeartbeatRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> PresenceResponse:
    settings = get_settings()
    if not settings.feature_peer_network:
        raise HTTPException(status_code=400, detail="Peer network disabled")

    status = req.status if req.status in ALLOWED_STATUSES else "studying"
    display = (req.display_name or user.username or user.email.split("@")[0])[:48]

    existing = session.exec(
        select(PeerPresence).where(PeerPresence.user_id == user.id)
    ).first()
    if existing:
        existing.lesson_id = req.lesson_id
        existing.status = status
        existing.note = req.note[:240]
        existing.looking_for_pair = bool(req.looking_for_pair)
        existing.display_name = display
        existing.last_seen = datetime.utcnow()
        me = existing
    else:
        me = PeerPresence(
            user_id=user.id, lesson_id=req.lesson_id, status=status,
            note=req.note[:240], looking_for_pair=bool(req.looking_for_pair),
            display_name=display,
        )
        session.add(me)
    session.commit()
    session.refresh(me)

    cutoff = datetime.utcnow() - ACTIVE_WINDOW
    others = session.exec(
        select(PeerPresence)
        .where(PeerPresence.user_id != user.id, PeerPresence.last_seen >= cutoff)
        .order_by(PeerPresence.looking_for_pair.desc(), PeerPresence.last_seen.desc())
        .limit(100)
    ).all()

    on_lesson = [p for p in others if me.lesson_id and p.lesson_id == me.lesson_id]
    elsewhere = [p for p in others if not me.lesson_id or p.lesson_id != me.lesson_id]

    asyncio.create_task(broadcast_presence_change(user.id))

    return PresenceResponse(
        me=_peer_out(me),
        peers_on_lesson=[_peer_out(p) for p in on_lesson],
        other_peers_online=[_peer_out(p) for p in elsewhere],
    )


@router.delete("/presence")
def leave_presence(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> dict:
    existing = session.exec(
        select(PeerPresence).where(PeerPresence.user_id == user.id)
    ).first()
    if existing:
        session.delete(existing)
        session.commit()
    asyncio.create_task(broadcast_presence_change(user.id))
    return {"ok": True}


# ── WebSocket pub/sub ──────────────────────────────────────────

class _Hub:
    """Tiny in-process pub/sub for presence updates.

    For a single-instance deploy this is sufficient. Multi-instance would
    need Redis pubsub — out of scope for the hackathon demo.
    """

    def __init__(self) -> None:
        self.connections: set[WebSocket] = set()
        self.lock = asyncio.Lock()

    async def add(self, ws: WebSocket) -> None:
        async with self.lock:
            self.connections.add(ws)

    async def remove(self, ws: WebSocket) -> None:
        async with self.lock:
            self.connections.discard(ws)

    async def broadcast(self, payload: dict) -> None:
        async with self.lock:
            dead: list[WebSocket] = []
            for ws in self.connections:
                try:
                    await ws.send_json(payload)
                except Exception:
                    dead.append(ws)
            for ws in dead:
                self.connections.discard(ws)


_HUB = _Hub()


async def broadcast_presence_change(actor_id: str) -> None:
    snapshot = _snapshot_presence()
    await _HUB.broadcast({"type": "presence", "actor": actor_id, "peers": snapshot})


def _snapshot_presence() -> list[dict]:
    cutoff = datetime.utcnow() - ACTIVE_WINDOW
    with Session(engine) as db:
        rows = db.exec(
            select(PeerPresence)
            .where(PeerPresence.last_seen >= cutoff)
            .order_by(PeerPresence.last_seen.desc())
            .limit(200)
        ).all()
    return [
        {
            "user_id": r.user_id,
            "display_name": r.display_name or "Anonymous",
            "lesson_id": r.lesson_id,
            "status": r.status,
            "note": r.note,
            "looking_for_pair": r.looking_for_pair,
            "last_seen": r.last_seen.isoformat(),
        }
        for r in rows
    ]


@router.websocket("/ws")
async def presence_ws(ws: WebSocket):
    """Live presence feed — emits a snapshot on connect, then incremental
    updates whenever any peer's presence changes. Supports a `nudge` message
    to ping another user (broadcasted, the recipient's client filters)."""
    await ws.accept()
    await _HUB.add(ws)
    try:
        await ws.send_json({"type": "snapshot", "peers": _snapshot_presence()})
        while True:
            msg = await ws.receive_text()
            try:
                event = json.loads(msg)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "nudge":
                await _HUB.broadcast({
                    "type": "nudge",
                    "from": event.get("from", ""),
                    "to": event.get("to", ""),
                    "message": (event.get("message") or "")[:240],
                    "ts": datetime.utcnow().isoformat(),
                })
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.warning("WS error: %s", e)
    finally:
        await _HUB.remove(ws)


# ── Resource router ────────────────────────────────────────────

CACHE_TTL = timedelta(hours=12)


def _cache_key(source: str, query: str) -> str:
    return hashlib.sha1(f"{source}::{query.lower().strip()}".encode()).hexdigest()


def _cache_get(source: str, query: str) -> Optional[list[dict]]:
    key = _cache_key(source, query)
    with Session(engine) as db:
        row = db.exec(
            select(ResourceCacheEntry).where(ResourceCacheEntry.query_hash == key)
        ).first()
        if not row:
            return None
        if datetime.utcnow() - row.created_at > CACHE_TTL:
            db.delete(row)
            db.commit()
            return None
        try:
            return json.loads(row.payload)
        except json.JSONDecodeError:
            return None


def _cache_put(source: str, query: str, items: list[dict]) -> None:
    key = _cache_key(source, query)
    with Session(engine) as db:
        existing = db.exec(
            select(ResourceCacheEntry).where(ResourceCacheEntry.query_hash == key)
        ).first()
        if existing:
            existing.payload = json.dumps(items)
            existing.created_at = datetime.utcnow()
        else:
            db.add(ResourceCacheEntry(
                query_hash=key, source=source, payload=json.dumps(items),
            ))
        db.commit()


async def fetch_arxiv(query: str, max_results: int = 5) -> list[dict]:
    cached = _cache_get("arxiv", query)
    if cached is not None:
        return cached
    settings = get_settings()
    url = f"{settings.arxiv_url}?search_query=all:{quote_plus(query)}&start=0&max_results={max_results}&sortBy=relevance"
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(url)
            r.raise_for_status()
        items = _parse_arxiv(r.text)
    except Exception as e:
        logger.warning("arxiv fetch failed: %s", e)
        return []
    _cache_put("arxiv", query, items)
    return items


def _parse_arxiv(xml_text: str) -> list[dict]:
    ns = {"a": "http://www.w3.org/2005/Atom"}
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    out: list[dict] = []
    for entry in root.findall("a:entry", ns):
        title = (entry.findtext("a:title", default="", namespaces=ns) or "").strip()
        summary = (entry.findtext("a:summary", default="", namespaces=ns) or "").strip()
        link = ""
        for link_el in entry.findall("a:link", ns):
            if link_el.get("rel") == "alternate":
                link = link_el.get("href") or ""
                break
        authors = [
            (a.findtext("a:name", default="", namespaces=ns) or "").strip()
            for a in entry.findall("a:author", ns)
        ]
        published = entry.findtext("a:published", default="", namespaces=ns) or ""
        out.append({
            "source": "arxiv",
            "title": title,
            "url": link,
            "authors": authors[:5],
            "published": published[:10],
            "snippet": summary[:400],
        })
    return out


async def fetch_github(query: str, max_results: int = 5) -> list[dict]:
    cached = _cache_get("github", query)
    if cached is not None:
        return cached
    settings = get_settings()
    url = f"{settings.github_url}/search/repositories?q={quote_plus(query)}&sort=stars&per_page={max_results}"
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(url, headers={"Accept": "application/vnd.github+json"})
            r.raise_for_status()
            data = r.json()
    except Exception as e:
        logger.warning("github fetch failed: %s", e)
        return []
    items = [
        {
            "source": "github",
            "title": item.get("full_name") or item.get("name") or "",
            "url": item.get("html_url") or "",
            "stars": item.get("stargazers_count", 0),
            "language": item.get("language") or "",
            "snippet": (item.get("description") or "")[:400],
        }
        for item in (data.get("items") or [])[:max_results]
    ]
    _cache_put("github", query, items)
    return items


async def fetch_youtube(query: str, max_results: int = 5) -> list[dict]:
    settings = get_settings()
    if not (settings.youtube_search_enabled and settings.youtube_api_key):
        return []
    cached = _cache_get("youtube", query)
    if cached is not None:
        return cached
    url = (
        "https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet&type=video&maxResults={max_results}"
        f"&q={quote_plus(query)}&key={settings.youtube_api_key}"
    )
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(url)
            r.raise_for_status()
            data = r.json()
    except Exception as e:
        logger.warning("youtube fetch failed: %s", e)
        return []
    items = []
    for it in data.get("items") or []:
        vid = (it.get("id") or {}).get("videoId")
        snip = it.get("snippet") or {}
        if not vid:
            continue
        items.append({
            "source": "youtube",
            "title": snip.get("title", ""),
            "url": f"https://www.youtube.com/watch?v={vid}",
            "channel": snip.get("channelTitle", ""),
            "published": (snip.get("publishedAt") or "")[:10],
            "snippet": (snip.get("description") or "")[:400],
        })
    _cache_put("youtube", query, items)
    return items


def _rerank_local(items: list[dict], focus_terms: set[str]) -> list[dict]:
    """Light heuristic rerank: prefer items whose title/snippet covers more focus terms."""
    if not focus_terms:
        return items
    scored: list[tuple[float, dict]] = []
    for it in items:
        hay = f"{it.get('title','')} {it.get('snippet','')}".lower()
        hits = sum(1 for t in focus_terms if t in hay)
        score = hits + (it.get("stars", 0) / 5000 if it.get("source") == "github" else 0)
        scored.append((score, it))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [it for _, it in scored]


class ResourceRouterResponse(BaseModel):
    query: str
    items: list[dict]
    by_source: dict[str, int]
    elapsed_ms: int


@router.get("/resources", response_model=ResourceRouterResponse)
async def route_resources(
    query: Optional[str] = Query(default=None),
    lesson_id: Optional[str] = Query(default=None),
    sources: str = Query(default="arxiv,github,youtube"),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> ResourceRouterResponse:
    settings = get_settings()
    if not settings.feature_resource_router:
        raise HTTPException(status_code=400, detail="Resource router disabled")

    if lesson_id and not query:
        lesson = session.get(Lesson, lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        try:
            concepts = json.loads(lesson.concepts) if lesson.concepts else []
        except json.JSONDecodeError:
            concepts = []
        query = lesson.title + ((" " + " ".join(concepts[:3])) if concepts else "")

    if not query:
        raise HTTPException(status_code=400, detail="Provide query or lesson_id")

    requested = {s.strip().lower() for s in sources.split(",") if s.strip()}
    started = time.perf_counter()

    tasks = []
    if "arxiv" in requested:
        tasks.append(("arxiv", fetch_arxiv(query)))
    if "github" in requested:
        tasks.append(("github", fetch_github(query)))
    if "youtube" in requested:
        tasks.append(("youtube", fetch_youtube(query)))

    results = await asyncio.gather(*[t[1] for t in tasks], return_exceptions=True)
    by_source: dict[str, int] = {}
    aggregated: list[dict] = []
    for (src, _), res in zip(tasks, results):
        if isinstance(res, Exception):
            logger.warning("source %s failed: %s", src, res)
            by_source[src] = 0
            continue
        by_source[src] = len(res)
        aggregated.extend(res)

    focus_terms = set(tokenize(query))
    aggregated = _rerank_local(aggregated, focus_terms)

    elapsed = int((time.perf_counter() - started) * 1000)
    return ResourceRouterResponse(
        query=query,
        items=aggregated[:30],
        by_source=by_source,
        elapsed_ms=elapsed,
    )
