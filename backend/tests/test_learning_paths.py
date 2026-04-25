import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_learning_paths_empty(client: AsyncClient, auth_headers: dict):
    resp = await client.get("/learning-paths", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_get_nonexistent_learning_path(client: AsyncClient, auth_headers: dict):
    resp = await client.get("/learning-paths/no-such-slug", headers=auth_headers)
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_nonexistent_lesson(client: AsyncClient, auth_headers: dict):
    resp = await client.get("/learning-paths/lessons/no-such-id", headers=auth_headers)
    assert resp.status_code == 404
