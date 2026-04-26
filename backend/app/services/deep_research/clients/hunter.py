"""Hunter.io client — email discovery from a name + organization."""
from __future__ import annotations

import os
from typing import Any, Optional

import httpx

BASE_URL = "https://api.hunter.io/v2"


class HunterClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("HUNTER_API_KEY", "")
        self._client = httpx.AsyncClient(timeout=20.0)

    async def close(self) -> None:
        await self._client.aclose()

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    async def find_email(
        self,
        *,
        full_name: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        domain: Optional[str] = None,
        company: Optional[str] = None,
    ) -> dict[str, Any]:
        """Returns {email, score, ...} or {} if disabled / nothing found.

        Pass either full_name OR (first_name + last_name). Either domain or
        company is required.
        """
        if not self.enabled:
            return {}
        if full_name and not (first_name and last_name):
            parts = full_name.strip().split()
            if len(parts) >= 2:
                first_name = parts[0]
                last_name = parts[-1]
        params: dict[str, Any] = {"api_key": self.api_key}
        if first_name:
            params["first_name"] = first_name
        if last_name:
            params["last_name"] = last_name
        if domain:
            params["domain"] = domain
        elif company:
            params["company"] = company
        else:
            return {}
        try:
            r = await self._client.get(f"{BASE_URL}/email-finder", params=params)
            if r.status_code != 200:
                return {}
            return r.json().get("data", {}) or {}
        except httpx.HTTPError:
            return {}
