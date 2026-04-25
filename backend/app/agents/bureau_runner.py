"""
Run the SAGE Bureau as a background daemon thread alongside FastAPI.

Import `start_bureau_daemon()` from `main.py` `lifespan` to bring all 7 agents
online inside the same process. A failure to start (missing uagents, port in
use, missing API key) is logged and swallowed — the API stays up.
"""
from __future__ import annotations

import logging
import threading
from typing import Optional

log = logging.getLogger("sage.bureau")

_thread: Optional[threading.Thread] = None
_started = False


def _run_bureau() -> None:
    # uagents `Agent.__init__` calls `get_event_loop()` which raises in a
    # non-main thread unless we explicitly install one first.
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        from uagents import Bureau
        from app.agents.director_agent import create_director_agent
        from app.agents.uagents_runner import (
            create_assessment_agent,
            create_concept_map_agent,
            create_content_agent,
            create_pedagogy_agent,
            create_peer_match_agent,
            create_progress_agent,
        )
    except ImportError as e:
        log.warning("uagents not installed; Bureau not started: %s", e)
        return

    agents = [
        create_director_agent(),
        create_pedagogy_agent(),
        create_content_agent(),
        create_concept_map_agent(),
        create_assessment_agent(),
        create_peer_match_agent(),
        create_progress_agent(),
    ]
    agents = [a for a in agents if a is not None]
    if not agents:
        log.warning("No agents were created; Bureau exit.")
        return

    log.info("Starting SAGE Bureau with %d agents", len(agents))
    for a in agents:
        log.info("  -> %s @ %s", a.name, a.address)

    bureau = Bureau()
    for a in agents:
        bureau.add(a)
    try:
        bureau.run()
    except Exception as e:
        log.exception("Bureau crashed: %s", e)


def start_bureau_daemon() -> None:
    """Idempotent — safe to call multiple times."""
    global _thread, _started
    if _started:
        return
    _started = True
    _thread = threading.Thread(target=_run_bureau, name="sage-bureau", daemon=True)
    _thread.start()
    log.info("Bureau daemon thread launched")


def is_bureau_running() -> bool:
    return _thread is not None and _thread.is_alive()
