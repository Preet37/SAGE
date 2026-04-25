"""Small in-process per-IP rate limiter for auth and tutor endpoints."""

from __future__ import annotations

import os
import time
from collections import defaultdict, deque
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

_DISABLED = os.getenv("RATE_LIMIT_DISABLED") == "1"


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Sliding-window limiter scoped to high-cost or abuse-prone routes.

    This intentionally stays dependency-free because the app already runs in a
    single API process for MVP. Production multi-instance deployment should move
    this counter to Redis or an edge gateway.
    """

    def __init__(self, app, requests_per_minute: int = 30) -> None:
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.window_seconds = 60.0
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        if _DISABLED or not self._limited_path(request.url.path):
            return await call_next(request)

        forwarded = request.headers.get("x-forwarded-for", "")
        client_ip = forwarded.split(",", 1)[0].strip() or (
            request.client.host if request.client else "unknown"
        )
        key = f"{client_ip}:{request.url.path}"
        now = time.monotonic()
        hits = self._hits[key]
        while hits and now - hits[0] > self.window_seconds:
            hits.popleft()
        if len(hits) >= self.requests_per_minute:
            return JSONResponse(
                {"detail": "Rate limit exceeded. Try again shortly."},
                status_code=429,
                headers={"Retry-After": "60"},
            )
        hits.append(now)
        return await call_next(request)

    @staticmethod
    def _limited_path(path: str) -> bool:
        return path in {"/auth/register", "/auth/token", "/tutor/chat"}
