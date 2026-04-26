"""Tavily client — semantic web search with content snippets."""
from __future__ import annotations

import os
from typing import Any

import httpx

BASE_URL = "https://api.tavily.com"


class TavilyClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("TAVILY_API_KEY", "")
        self._client = httpx.AsyncClient(timeout=30.0)

    async def close(self) -> None:
        await self._client.aclose()

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    async def search(
        self,
        query: str,
        *,
        max_results: int = 5,
        search_depth: str = "advanced",
        include_answer: bool = True,
    ) -> dict[str, Any]:
        if not self.enabled:
            return {"results": [], "answer": None}
        r = await self._client.post(
            f"{BASE_URL}/search",
            json={
                "api_key": self.api_key,
                "query": query,
                "max_results": max_results,
                "search_depth": search_depth,
                "include_answer": include_answer,
            },
        )
        r.raise_for_status()
        return r.json()
