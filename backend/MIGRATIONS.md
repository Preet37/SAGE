# Database migrations (Alembic)

Schema changes are managed with [Alembic](https://alembic.sqlalchemy.org/). The app runs `alembic upgrade head` on startup (see `app/db.py` and `app/main.py`). Pytests set `SKIP_DB_MIGRATIONS=1` and use an in-memory database.

## Commands (from `backend/`)

| Command | Purpose |
|--------|---------|
| `uv run alembic upgrade head` | Apply all pending migrations |
| `uv run alembic revision --autogenerate -m "short description"` | Create a migration from SQLModel changes |
| `uv run alembic stamp head` | Mark the current DB as up-to-date **without** running SQL (use when the DB already matches the models) |
| `uv run alembic downgrade -1` | Roll back one revision |
| `uv run alembic current` | Show current revision |

## After changing models

1. Edit models under `app/models/`.
2. `uv run alembic revision --autogenerate -m "add field x to lesson"`.
3. Review the generated file under `migrations/versions/` (autogenerate is not perfect).
4. `uv run alembic upgrade head` locally.
5. Commit the migration file.

## Existing databases before Alembic

If you already had a `tutor.db` created with `create_all` and you add the first migration, either:

- Run `uv run alembic stamp head` once if the schema already matches the migration, or
- Start from a fresh DB and run `uv run alembic upgrade head`.

## CLI without JWT

`alembic` reads the database URL from `settings.yaml` only (see `migrations/env.py`), so you do not need `JWT_SECRET` to run migrations.
