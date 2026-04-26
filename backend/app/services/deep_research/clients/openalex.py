"""OpenAlex client — academic papers, citations, author graph.

OpenAlex is free and unauthenticated; the polite-pool just wants an email
via `mailto`. Premium API keys go in the Authorization header. We support
both transparently.
"""
from __future__ import annotations

import os
from typing import Any, Optional

import httpx

BASE_URL = "https://api.openalex.org"


def _headers() -> dict[str, str]:
    h: dict[str, str] = {"User-Agent": "SAGE-DeepResearch/1.0"}
    key = os.getenv("OPENALEX_API_KEY")
    if key:
        h["Authorization"] = f"Bearer {key}"
    return h


def _params(extra: Optional[dict] = None) -> dict[str, Any]:
    p: dict[str, Any] = {}
    mailto = os.getenv("OPENALEX_MAILTO")
    if mailto:
        p["mailto"] = mailto
    if extra:
        p.update(extra)
    return p


class OpenAlexClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(timeout=30.0, headers=_headers())

    async def close(self) -> None:
        await self._client.aclose()

    async def search_works(self, query: str, per_page: int = 25) -> list[dict[str, Any]]:
        """Return up to `per_page` works most relevant to `query`."""
        url = f"{BASE_URL}/works"
        params = _params({"search": query, "per-page": min(per_page, 200)})
        r = await self._client.get(url, params=params)
        r.raise_for_status()
        return r.json().get("results", [])

    async def get_author(self, author_id: str) -> dict[str, Any]:
        url = f"{BASE_URL}/authors/{author_id.split('/')[-1]}"
        r = await self._client.get(url, params=_params())
        r.raise_for_status()
        return r.json()

    async def works_by_author(
        self, author_id: str, per_page: int = 10
    ) -> list[dict[str, Any]]:
        url = f"{BASE_URL}/works"
        aid = author_id.split("/")[-1]
        params = _params(
            {"filter": f"author.id:{aid}", "per-page": min(per_page, 200)}
        )
        r = await self._client.get(url, params=params)
        r.raise_for_status()
        return r.json().get("results", [])
