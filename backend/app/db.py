from pathlib import Path

from sqlalchemy import text
from sqlmodel import SQLModel, create_engine, Session
from .config import get_settings

_BACKEND_DIR = Path(__file__).parent.parent

settings = get_settings()

def _resolve_db_url(url: str) -> str:
    """Resolve relative SQLite paths to absolute (relative to backend/)."""
    if url.startswith("sqlite:///./"):
        rel = url.replace("sqlite:///./", "")
        return f"sqlite:///{_BACKEND_DIR / rel}"
    return url

engine = create_engine(
    _resolve_db_url(settings.database_url),
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
    echo=False,
)


def _add_column_if_missing(conn, table: str, column: str, col_def: str):
    cols = [row[1] for row in conn.execute(text(f"PRAGMA table_info({table})"))]
    if column not in cols:
        conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {col_def}"))


def _run_sqlite_migrations(eng):
    """Schema additions that create_all may not cover on existing SQLite DBs."""
    with eng.connect() as conn:
        _add_column_if_missing(conn, "learningpath", "created_by", "TEXT")
        _add_column_if_missing(conn, "learningpath", "visibility", "TEXT NOT NULL DEFAULT 'public'")
        _add_column_if_missing(conn, "learningpath", "share_token", "TEXT")
        # Message metadata for production observability
        _add_column_if_missing(conn, "chatmessage", "message_meta", "TEXT")
        _add_column_if_missing(conn, "explorationmessage", "message_meta", "TEXT")
        conn.commit()


def create_db_and_tables():
    """Create all tables (tests / dev fallback). Prefer run_migrations() in production."""
    SQLModel.metadata.create_all(engine)
    if "sqlite" in settings.database_url:
        _run_sqlite_migrations(engine)


def run_migrations() -> None:
    """Apply Alembic migrations to head (production startup)."""
    from pathlib import Path

    from alembic import command
    from alembic.config import Config

    backend_dir = Path(__file__).resolve().parent.parent
    alembic_cfg = Config(str(backend_dir / "alembic.ini"))
    command.upgrade(alembic_cfg, "head")


def get_session():
    with Session(engine) as session:
        yield session
