import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_projects_empty(client: AsyncClient, auth_headers: dict):
    resp = await client.get("/projects", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_get_nonexistent_project(client: AsyncClient, auth_headers: dict):
    resp = await client.get("/projects/no-such-slug", headers=auth_headers)
    assert resp.status_code == 404
