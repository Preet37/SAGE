from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.config import assert_safe_for_production, settings
from app.db import init_db
from app.logging_setup import RequestIdMiddleware, configure_logging
from app.rate_limit import limiter
from app.routers import (
    accessibility,
    auth,
    concept_map,
    courses,
    dashboard,
    network,
    notes,
    replay,
    tutor,
)
from app.routers.network import start_peer_sweeper

configure_logging(settings.log_level)
assert_safe_for_production()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    sweeper = start_peer_sweeper()
    try:
        yield
    finally:
        sweeper.cancel()


init_db()  # idempotent — protects against lifespan-bypass deployments

app = FastAPI(title="SAGE API", version="0.1.0", lifespan=lifespan)
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def _rl(_: Request, exc: RateLimitExceeded) -> JSONResponse:  # noqa: ARG001
    return JSONResponse({"detail": "rate limit exceeded"}, status_code=429)


app.add_middleware(RequestIdMiddleware)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-Id"],
)


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
def health():
    return {"status": "ok", "service": "sage"}


for r in (
    auth.router,
    courses.router,
    tutor.router,
    concept_map.router,
    network.router,
    replay.router,
    accessibility.router,
    dashboard.router,
    notes.router,
):
    app.include_router(r)
