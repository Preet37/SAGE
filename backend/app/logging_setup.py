"""Structured logging with per-request correlation IDs.

`configure_logging()` installs a JSON-ish formatter on the root logger.
`RequestIdMiddleware` attaches a `request_id` to every request and exposes
it via response header `X-Request-Id` and a contextvar for log records.
"""

from __future__ import annotations

import contextvars
import json
import logging
import secrets
import time
from typing import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

REQUEST_ID: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": REQUEST_ID.get(),
        }
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(_JsonFormatter())
    root = logging.getLogger()
    # Replace existing handlers so uvicorn's defaults don't double-print.
    root.handlers = [handler]
    root.setLevel(level.upper())
    # Quiet down noisy libraries.
    for name in ("uvicorn.access", "httpx", "httpcore"):
        logging.getLogger(name).setLevel(logging.WARNING)


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        rid = request.headers.get("X-Request-Id") or secrets.token_urlsafe(8)
        token = REQUEST_ID.set(rid)
        started = time.perf_counter()
        try:
            response = await call_next(request)
        finally:
            REQUEST_ID.reset(token)
        duration_ms = round((time.perf_counter() - started) * 1000)
        response.headers["X-Request-Id"] = rid
        logging.getLogger("sage.access").info(
            "%s %s -> %s in %dms",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response
