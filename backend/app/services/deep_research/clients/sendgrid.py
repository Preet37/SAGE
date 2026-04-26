"""SendGrid client — outreach emails to discovered experts."""
from __future__ import annotations

import os
from typing import Any

import httpx


class SendGridClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("SENDGRID_API_KEY", "")
        self.from_email = os.getenv("SENDGRID_FROM_EMAIL", "noreply@example.com")
        self.from_name = os.getenv("SENDGRID_FROM_NAME", "SAGE Deep Research")
        self._client = httpx.AsyncClient(timeout=20.0)

    async def close(self) -> None:
        await self._client.aclose()

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    async def send_email(
        self, *, to_email: str, to_name: str, subject: str, body: str
    ) -> dict[str, Any]:
        if not self.enabled:
            return {"sent": False, "reason": "SENDGRID_API_KEY not configured"}
        payload = {
            "personalizations": [
                {"to": [{"email": to_email, "name": to_name}], "subject": subject}
            ],
            "from": {"email": self.from_email, "name": self.from_name},
            "content": [
                {"type": "text/plain", "value": body},
                {
                    "type": "text/html",
                    "value": body.replace("\n\n", "</p><p>").replace("\n", "<br/>"),
                },
            ],
        }
        try:
            r = await self._client.post(
                "https://api.sendgrid.com/v3/mail/send",
                json=payload,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
            return {
                "sent": r.status_code in (200, 202),
                "status_code": r.status_code,
                "message_id": r.headers.get("X-Message-Id"),
                "error": (r.text if r.status_code >= 400 else None),
            }
        except httpx.HTTPError as e:
            return {"sent": False, "error": str(e)}
