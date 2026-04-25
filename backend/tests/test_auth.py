import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_new_user(client: AsyncClient):
    resp = await client.post(
        "/auth/register",
        json={
            "email": "new@example.com",
            "username": "newuser",
            "password": "securepass",
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    payload = {
        "email": "dup@example.com",
        "username": "user1",
        "password": "pass123",
    }
    resp1 = await client.post("/auth/register", json=payload)
    assert resp1.status_code == 200

    resp2 = await client.post(
        "/auth/register",
        json={**payload, "username": "user2"},
    )
    assert resp2.status_code == 400
    assert "already registered" in resp2.json()["detail"].lower()


@pytest.mark.asyncio
async def test_register_duplicate_username(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={
            "email": "a@example.com",
            "username": "samename",
            "password": "pass",
        },
    )
    resp = await client.post(
        "/auth/register",
        json={
            "email": "b@example.com",
            "username": "samename",
            "password": "pass",
        },
    )
    assert resp.status_code == 400
    assert "username" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_correct_credentials(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "username": "loginuser",
            "password": "mypassword",
        },
    )
    resp = await client.post(
        "/auth/login",
        json={"email": "login@example.com", "password": "mypassword"},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={
            "email": "wrong@example.com",
            "username": "wronguser",
            "password": "rightpass",
        },
    )
    resp = await client.post(
        "/auth/login",
        json={"email": "wrong@example.com", "password": "badpass"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_protected_route_without_token(client: AsyncClient):
    resp = await client.get("/learning-paths")
    assert resp.status_code in (401, 403)
