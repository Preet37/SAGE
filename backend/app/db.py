"""SQLAlchemy engine, session, declarative base, and lightweight schema sync.

For MVP, `init_db()` does two things:
  1. Create any tables that don't exist yet (`Base.metadata.create_all`).
  2. ALTER existing tables to add columns we've added since the last boot,
     so an old `sage.db` file keeps working without a destructive reset.

For production, prefer Alembic migrations (see `alembic.ini`).
"""

from __future__ import annotations

import logging

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

log = logging.getLogger("sage.db")

engine: Engine = create_engine(
    settings.database_url,
    connect_args=(
        {"check_same_thread": False}
        if settings.database_url.startswith("sqlite")
        else {}
    ),
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----- Lightweight schema sync (MVP only) ---------------------------------


def _ensure_columns(table: str, expected: dict[str, str]) -> None:
    """Add columns from `expected` that don't yet exist in `table`.

    `expected` maps column-name -> SQL type-and-default, e.g.
    `{"teaching_mode": "VARCHAR(32) DEFAULT 'default'"}`.

    SQLite supports `ALTER TABLE ADD COLUMN` for simple defaults; this is
    sufficient for the additive changes the MVP makes.
    """
    insp = inspect(engine)
    if table not in insp.get_table_names():
        return
    have = {c["name"] for c in insp.get_columns(table)}
    missing = [(name, ddl) for name, ddl in expected.items() if name not in have]
    if not missing:
        return
    with engine.begin() as conn:
        for name, ddl in missing:
            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {name} {ddl}"))
            log.info("added missing column %s.%s", table, name)


def init_db() -> None:
    # Ensure all model modules are imported so their tables register.
    from app.models import concept, lesson, message, session, user  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _ensure_columns(
        "users",
        {"teaching_mode": "VARCHAR(32) DEFAULT 'default' NOT NULL"},
    )
