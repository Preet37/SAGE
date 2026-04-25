from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.db import init_db
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


init_db()  # idempotent — protects against lifespan-bypass deployments

app = FastAPI(title="SAGE API", version="0.1.0", lifespan=lifespan)
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def _rl(_: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse({"detail": "rate limit exceeded"}, status_code=429)


app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
