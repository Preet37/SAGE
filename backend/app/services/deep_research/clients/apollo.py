"""Apollo.io client — enrich expert profiles with role + organization data."""
from __future__ import annotations

import os
from typing import Any, Optional

import httpx

BASE_URL = "https://api.apollo.io/api/v1"


class ApolloClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("APOLLO_API_KEY", "")
        self._client = httpx.AsyncClient(timeout=20.0)

    async def close(self) -> None:
        await self._client.aclose()

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    async def search_people(
        self,
        *,
        name: Optional[str] = None,
        organization_name: Optional[str] = None,
        per_page: int = 5,
    ) -> list[dict[str, Any]]:
        if not self.enabled:
            return []
        body: dict[str, Any] = {"per_page": per_page}
        if name:
            body["q_keywords"] = name
        if organization_name:
            body["organization_names"] = [organization_name]
        try:
            r = await self._client.post(
                f"{BASE_URL}/mixed_people/api_search",
                json=body,
                headers={
                    "Cache-Control": "no-cache",
                    "Content-Type": "application/json",
                    "X-Api-Key": self.api_key,
                },
            )
            if r.status_code != 200:
                return []
            return r.json().get("people", []) or []
        except httpx.HTTPError:
            return []
