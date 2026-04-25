"""SAGE — Socratic Agent for Guided Education. FastAPI main application."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_tables
from app.config import get_settings
from app.logging_setup import RequestIdMiddleware, configure_logging
from app.rate_limit import RateLimitMiddleware
from app.routers import (
    auth,
    courses,
    tutor,
    concept_map,
    network,
    replay,
    accessibility,
    dashboard,
    notes,
    visual,
    visual_code,
    visual_plot,
    media,
    sms,
    diagnostic,
    broadcast,
    export,
)

settings = get_settings()
configure_logging(settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    # Boot the Fetch.ai Bureau (7 uAgents) in a background daemon thread
    # so the FastAPI process can talk to them via the Chat/Payment Protocol.
    if settings.environment != "test":
        try:
            from app.agents.bureau_runner import start_bureau_daemon
            start_bureau_daemon()
        except Exception:
            import logging
            logging.getLogger("sage.bureau").warning(
                "Bureau startup skipped", exc_info=True
            )
    yield


app = FastAPI(
    title="SAGE API",
    description="Socratic Agent for Guided Education — multi-agent AI tutor",
    version="1.0.0",
    lifespan=lifespan,
)

origins = [o.strip() for o in settings.frontend_url.split(",") if o.strip()]
if settings.cors_extra_origins:
    origins.extend(o.strip() for o in settings.cors_extra_origins.split(",") if o.strip())
if not settings.is_production:
    for port in ["3000", "3001", "3002"]:
        origin = f"http://localhost:{port}"
        if origin not in origins:
            origins.append(origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-Id"],
)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestIdMiddleware)

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(tutor.router)
app.include_router(concept_map.router)
app.include_router(network.router)
app.include_router(replay.router)
app.include_router(accessibility.router)
app.include_router(dashboard.router)
app.include_router(notes.router)
app.include_router(visual.router)
app.include_router(visual_code.router)
app.include_router(visual_plot.router)
app.include_router(media.router)
app.include_router(sms.router)
app.include_router(diagnostic.router)
app.include_router(broadcast.router)
app.include_router(export.router)


@app.get("/")
def root():
    return {
        "service": "sage",
        "version": "0.1.0",
        "environment": settings.environment,
        "features": [
            "auth",
            "courses",
            "tutor-streaming",
            "tutor-tts",
            "concept-map",
            "network-peer-match",
            "replay",
            "accessibility",
            "dashboard",
            "notes",
            "study-plan",
        ],
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/metrics")
async def metrics():
    from datetime import datetime, timezone
    from app.routers.network import _waiting_room, _peer_connections
    waiting = sum(len(v) for v in _waiting_room.values())
    return {
        "status": "ok",
        "environment": settings.environment,
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "peer": {
            "waiting_room_size": waiting,
            "active_connections": len(_peer_connections),
        },
    }
