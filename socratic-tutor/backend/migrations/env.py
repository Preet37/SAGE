"""Alembic environment — uses SQLModel metadata; URL from settings.yaml (no JWT required)."""

from __future__ import annotations

import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import create_engine, pool
from sqlmodel import SQLModel

# Ensure backend/ is on path, then register all models on SQLModel.metadata
_backend_dir = Path(__file__).resolve().parent.parent
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))
import app.models  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def _get_sync_database_url() -> str:
    """Match app.db URL resolution without importing app.db (avoids Settings/JWT at import)."""
    import yaml

    backend_dir = Path(__file__).resolve().parent.parent
    settings_path = backend_dir / "settings.yaml"
    with open(settings_path) as f:
        cfg = yaml.safe_load(f)
    url: str = cfg["database"]["url"]
    if url.startswith("sqlite:///./"):
        rel = url.replace("sqlite:///./", "")
        return f"sqlite:///{(backend_dir / rel).resolve()}"
    return url


def run_migrations_offline() -> None:
    url = _get_sync_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    url = _get_sync_database_url()
    connectable = create_engine(
        url,
        connect_args={"check_same_thread": False} if "sqlite" in url else {},
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
