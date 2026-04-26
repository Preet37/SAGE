import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse

from .config import get_settings
from .db import run_migrations, create_db_and_tables
from .routers import auth, learning_paths, progress, tutor, explore, quiz, concepts, assessment, curriculum
from .routers import projects, course_creator, visual_plot, visual_3d, sandbox, sms, diagnostic, broadcast, export
from .routers import cognition, network, media, fetchai_bridge, documents

settings = get_settings()

app = FastAPI(title="SAGE API", version="1.0.0")

_origins = [o.strip() for o in settings.frontend_url.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Session-Id"],
)


@app.on_event("startup")
def on_startup():
    if os.getenv("SKIP_DB_MIGRATIONS"):
        return
    if "sqlite" in settings.database_url:
        # SQLite: use create_all (same engine, no lock contention).
        # Run `alembic upgrade head` separately for production deploys.
        create_db_and_tables()
    else:
        run_migrations()


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(learning_paths.router)
app.include_router(progress.router)
app.include_router(tutor.router)
app.include_router(explore.router)
app.include_router(quiz.router)
app.include_router(concepts.router)
app.include_router(assessment.router)
app.include_router(curriculum.router)

app.include_router(projects.router)
app.include_router(course_creator.router)
app.include_router(sms.router)
app.include_router(diagnostic.router)
app.include_router(broadcast.router)
app.include_router(export.router)
app.include_router(visual_plot.router)
app.include_router(visual_3d.router)
app.include_router(sandbox.router)

# Hackathon track routers
app.include_router(cognition.router)
app.include_router(network.router)
app.include_router(media.router)
app.include_router(fetchai_bridge.router)
app.include_router(documents.router)

from .config import WIKI_DIR
_wiki_topics_dir = WIKI_DIR / "resources" / "by-topic"

_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}


@app.get("/api/wiki-images/{topic_slug}/images/{filename}")
async def serve_wiki_image(topic_slug: str, filename: str):
    """Serve image files only — blocks access to source markdown, proposals, etc."""
    if not _wiki_topics_dir.is_dir():
        raise HTTPException(status_code=404, detail="Wiki images not available")
    ext = Path(filename).suffix.lower()
    if ext not in _IMAGE_EXTENSIONS:
        raise HTTPException(status_code=403, detail="Only image files are served")
    file_path = (_wiki_topics_dir / topic_slug / "images" / filename).resolve()
    if not str(file_path).startswith(str(_wiki_topics_dir.resolve())):
        raise HTTPException(status_code=403, detail="Invalid path")
    if not file_path.is_file():
        # Fall back to source URL from images.json if the local file is missing
        # (e.g. image was recorded as url-only because download failed on server)
        images_json = (_wiki_topics_dir / topic_slug / "images" / "images.json").resolve()
        if images_json.is_file():
            try:
                entries = json.loads(images_json.read_text())
                for entry in entries:
                    if entry.get("file") == filename:
                        src = entry.get("source_url", "")
                        if src.startswith("http"):
                            return RedirectResponse(url=src, status_code=302)
            except Exception:
                pass
        raise HTTPException(status_code=404, detail="Image not found")
    media_types = {
        ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".gif": "image/gif", ".svg": "image/svg+xml", ".webp": "image/webp",
    }
    return FileResponse(file_path, media_type=media_types.get(ext, "application/octet-stream"))
