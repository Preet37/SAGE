#!/usr/bin/env python3
"""SAGE MCP server — exposes the SAGE knowledge base as MCP tools.

Why this exists (Cognition track): coding agents and research agents are
limited by what they can pull into their context. SAGE's curated lesson KB
+ verified-claim verifier are exactly the kind of high-signal, grounded
augmentation that makes those agents measurably more capable. This server
lets any MCP-aware agent (Claude Code, Cursor, custom Agent SDK code) plug
into SAGE without writing HTTP glue.

Implementation: stdlib-only JSON-RPC 2.0 over stdio (the MCP transport).
Talks to a running SAGE backend over HTTP for actual data.

Usage (Claude Code / Cursor mcp.json):

    {
      "mcpServers": {
        "sage": {
          "command": "python",
          "args": ["/abs/path/to/SAGE/backend/mcp_server.py"],
          "env": {
            "SAGE_API_URL": "http://localhost:8000",
            "SAGE_AUTH_TOKEN": "<jwt from /auth/login>"
          }
        }
      }
    }

Tools exposed:
    sage.lesson.search   — find lessons by free-text query
    sage.lesson.get      — full content + reference KB for a lesson
    sage.concept.lookup  — curated wiki resources for a concept
    sage.verify          — score a factual claim against a lesson's KB
    sage.memory.recall   — recall the user's prior tutor conversations
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

PROTOCOL_VERSION = "2025-06-18"
SERVER_NAME = "sage-mcp"
SERVER_VERSION = "1.0.0"


def _api_url() -> str:
    return os.environ.get("SAGE_API_URL", "http://localhost:8000").rstrip("/")


def _headers() -> dict[str, str]:
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    token = os.environ.get("SAGE_AUTH_TOKEN", "")
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _http(method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    url = f"{_api_url()}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=_headers(), method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode("utf-8")
        except Exception:
            err_body = str(e)
        raise RuntimeError(f"HTTP {e.code}: {err_body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"network error: {e}") from e


# ── Tool implementations ───────────────────────────────────────

def tool_lesson_search(args: dict[str, Any]) -> str:
    query = (args.get("query") or "").strip().lower()
    paths = _http("GET", "/learn")
    if not isinstance(paths, list):
        return json.dumps({"error": "unexpected /learn response"})
    matches: list[dict[str, Any]] = []
    for p in paths:
        for m in p.get("modules") or []:
            for lesson in m.get("lessons") or []:
                hay = " ".join([
                    lesson.get("title") or "",
                    lesson.get("slug") or "",
                    lesson.get("summary") or "",
                    " ".join(lesson.get("concepts") or []),
                ]).lower()
                if not query or query in hay:
                    matches.append({
                        "lesson_id": lesson.get("id"),
                        "slug": lesson.get("slug"),
                        "title": lesson.get("title"),
                        "summary": (lesson.get("summary") or "")[:240],
                        "course": p.get("title"),
                    })
    return json.dumps({"matches": matches[:25]}, indent=2)


def tool_lesson_get(args: dict[str, Any]) -> str:
    lesson_id = args.get("lesson_id")
    if not lesson_id:
        return json.dumps({"error": "lesson_id is required"})
    data = _http("GET", f"/learn/lesson/{lesson_id}")
    return json.dumps({
        "id": data.get("id"),
        "title": data.get("title"),
        "summary": data.get("summary"),
        "content": data.get("content"),
        "reference_kb": data.get("reference_kb"),
        "concepts": data.get("concepts"),
    }, indent=2)


def tool_concept_lookup(args: dict[str, Any]) -> str:
    topic = (args.get("topic") or "").strip()
    if not topic:
        return json.dumps({"error": "topic is required"})
    data = _http("POST", "/concepts/search", {"topic": topic})
    return json.dumps(data, indent=2)


def tool_verify(args: dict[str, Any]) -> str:
    claim = args.get("claim")
    lesson_id = args.get("lesson_id")
    if not claim or not lesson_id:
        return json.dumps({"error": "claim and lesson_id are required"})
    data = _http("POST", "/cognition/verify", {"claim": claim, "lesson_id": lesson_id})
    return json.dumps(data, indent=2)


def tool_memory_recall(args: dict[str, Any]) -> str:
    query = args.get("query")
    if not query:
        return json.dumps({"error": "query is required"})
    payload: dict[str, Any] = {"query": query, "k": int(args.get("k", 5))}
    if args.get("lesson_id"):
        payload["lesson_id"] = args["lesson_id"]
    data = _http("POST", "/cognition/memory/recall", payload)
    return json.dumps(data, indent=2)


TOOLS = {
    "sage.lesson.search": {
        "fn": tool_lesson_search,
        "description": "Search SAGE lessons by free-text query. Returns matching lesson titles, slugs, and summaries.",
        "inputSchema": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "Free-text search query"}},
            "required": ["query"],
        },
    },
    "sage.lesson.get": {
        "fn": tool_lesson_get,
        "description": "Fetch a lesson's full content + reference KB by lesson_id.",
        "inputSchema": {
            "type": "object",
            "properties": {"lesson_id": {"type": "string"}},
            "required": ["lesson_id"],
        },
    },
    "sage.concept.lookup": {
        "fn": tool_concept_lookup,
        "description": "Look up curated educational resources (videos, blogs, papers) for a concept from the SAGE pedagogy wiki.",
        "inputSchema": {
            "type": "object",
            "properties": {"topic": {"type": "string", "description": "Concept name (e.g. 'self-attention')"}},
            "required": ["topic"],
        },
    },
    "sage.verify": {
        "fn": tool_verify,
        "description": "Score a factual claim against a SAGE lesson's reference KB. Returns a groundedness score 0-1, supported claims, and unsupported claims.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "claim": {"type": "string", "description": "The claim to verify"},
                "lesson_id": {"type": "string", "description": "Lesson whose KB to verify against"},
            },
            "required": ["claim", "lesson_id"],
        },
    },
    "sage.memory.recall": {
        "fn": tool_memory_recall,
        "description": "Recall the authenticated user's prior tutor conversations relevant to a query.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "lesson_id": {"type": "string"},
                "k": {"type": "integer", "default": 5},
            },
            "required": ["query"],
        },
    },
}


# ── JSON-RPC dispatch ──────────────────────────────────────────

def _send(msg: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


def _result(rid: Any, result: Any) -> None:
    _send({"jsonrpc": "2.0", "id": rid, "result": result})


def _error(rid: Any, code: int, message: str) -> None:
    _send({"jsonrpc": "2.0", "id": rid, "error": {"code": code, "message": message}})


def handle(req: dict[str, Any]) -> None:
    method = req.get("method")
    rid = req.get("id")
    params = req.get("params") or {}

    if method == "initialize":
        _result(rid, {
            "protocolVersion": PROTOCOL_VERSION,
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            "capabilities": {"tools": {}},
        })
        return

    if method == "notifications/initialized":
        return  # no response for notifications

    if method == "tools/list":
        _result(rid, {
            "tools": [
                {
                    "name": name,
                    "description": spec["description"],
                    "inputSchema": spec["inputSchema"],
                }
                for name, spec in TOOLS.items()
            ]
        })
        return

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        spec = TOOLS.get(name)
        if not spec:
            _error(rid, -32601, f"Unknown tool: {name}")
            return
        try:
            text = spec["fn"](args)
        except Exception as e:
            _error(rid, -32000, f"Tool error: {e}")
            return
        _result(rid, {"content": [{"type": "text", "text": text}]})
        return

    if rid is not None:
        _error(rid, -32601, f"Method not found: {method}")


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        try:
            handle(req)
        except Exception as e:
            rid = req.get("id") if isinstance(req, dict) else None
            if rid is not None:
                _error(rid, -32603, f"Internal error: {e}")


if __name__ == "__main__":
    main()
