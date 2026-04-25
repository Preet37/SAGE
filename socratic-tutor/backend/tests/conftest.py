import os

os.environ.setdefault("JWT_SECRET", "test-secret-for-pytest")
# Skip Alembic on app startup — tests use an in-memory DB + create_all in the client fixture.
os.environ["SKIP_DB_MIGRATIONS"] = "1"

import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine
from httpx import AsyncClient, ASGITransport

import app.models  # noqa: F401 — register all models with SQLModel metadata
from app.main import app
from app.db import get_session
from app.config import get_settings


@pytest.fixture()
async def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def override_get_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture()
async def auth_headers(client: AsyncClient) -> dict[str, str]:
    resp = await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123",
        },
    )
    assert resp.status_code == 200, resp.text
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def _low_usage_limit():
    """Temporarily lower the daily message limit to 2 for testing."""
    settings = get_settings()
    original = settings.daily_message_limit
    settings.daily_message_limit = 2
    yield
    settings.daily_message_limit = original
