"""SAGE — Socratic Agent for Guided Education. FastAPI main application."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_tables
from app.config import get_settings
from app.routers import auth, courses, tutor, concept_map, network, replay, accessibility, dashboard, notes

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title="SAGE API",
    description="Socratic Agent for Guided Education — multi-agent AI tutor",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(tutor.router)
app.include_router(concept_map.router)
app.include_router(network.router)
app.include_router(replay.router)
app.include_router(accessibility.router)
app.include_router(dashboard.router)
app.include_router(notes.router)


@app.get("/")
async def root():
    return {
        "name": "SAGE",
        "version": "2.0.0",
        "status": "online",
        "agents": ["pedagogy", "content", "concept_map", "assessment", "peer_match", "progress"],
        "tracks": ["Fetch.ai", "Cognition", "Arista", "ZETIC", "Light the Way"],
        "features": [
            "socratic_tutoring", "live_concept_map", "voice_agent",
            "peer_matching", "session_replay", "accessibility_profiles",
            "note_revision", "course_dashboard", "offline_lesson_plans",
            "on_device_ai_zetic",
        ],
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
