"""Per-IP rate limiter (slowapi).

Used on auth and chat endpoints to mitigate credential stuffing and abuse.
Set `RATE_LIMIT_DISABLED=1` in tests or local environments where the limit
gets in the way.
"""

from __future__ import annotations

import os

from slowapi import Limiter
from slowapi.util import get_remote_address

_DISABLED = os.getenv("RATE_LIMIT_DISABLED") == "1"

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
    enabled=not _DISABLED,
)
