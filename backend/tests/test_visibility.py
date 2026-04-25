"""Tests for course visibility scoping and sharing."""

import pytest
from httpx import AsyncClient
from jose import jwt

from app.config import get_settings
from app.db import get_session
from app.main import app as fastapi_app
from app.models.learning import LearningPath, Module, Lesson


def _user_id_from(headers: dict) -> str:
    token = headers["Authorization"].split(" ", 1)[1]
    s = get_settings()
    return jwt.decode(token, s.jwt_secret, algorithms=[s.jwt_algorithm])["sub"]


async def _register(client: AsyncClient, email: str, username: str) -> dict:
    resp = await client.post(
        "/auth/register",
        json={"email": email, "username": username, "password": "pass123"},
    )
    assert resp.status_code == 200, resp.text
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}


def _seed_course(slug: str, title: str, *,
                 visibility: str = "public", created_by: str | None = None):
    session_gen = fastapi_app.dependency_overrides[get_session]()
    session = next(session_gen)
    path = LearningPath(
        slug=slug, title=title, description=f"Desc: {title}",
        visibility=visibility, created_by=created_by,
    )
    session.add(path)
    session.flush()
    mod = Module(learning_path_id=path.id, title="Mod 1", order_index=0)
    session.add(mod)
    session.flush()
    session.add(Lesson(
        module_id=mod.id, title="Lesson 1", slug=f"{slug}-l1",
        order_index=0, content="Content", summary="Summary", concepts="[]",
    ))
    session.commit()
    return path


# ---- Visibility ----


@pytest.mark.anyio
async def test_public_courses_visible_to_all(client: AsyncClient, auth_headers: dict):
    _seed_course("public-1", "Public Course")
    resp = await client.get("/learning-paths", headers=auth_headers)
    slugs = [p["slug"] for p in resp.json()]
    assert "public-1" in slugs


@pytest.mark.anyio
async def test_private_course_visible_only_to_creator(client: AsyncClient):
    alice = await _register(client, "alice@t.com", "alice")
    bob = await _register(client, "bob@t.com", "bob")
    alice_id = _user_id_from(alice)

    _seed_course("alice-private", "Alice Private", visibility="private", created_by=alice_id)

    resp_a = await client.get("/learning-paths", headers=alice)
    assert any(p["slug"] == "alice-private" for p in resp_a.json())

    resp_b = await client.get("/learning-paths", headers=bob)
    assert not any(p["slug"] == "alice-private" for p in resp_b.json())


@pytest.mark.anyio
async def test_private_course_detail_404_for_others(client: AsyncClient):
    alice = await _register(client, "carol@t.com", "carol")
    bob = await _register(client, "dave@t.com", "dave")
    alice_id = _user_id_from(alice)

    _seed_course("carol-priv", "Carol Private", visibility="private", created_by=alice_id)

    resp = await client.get("/learning-paths/carol-priv", headers=bob)
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_is_mine_flag(client: AsyncClient):
    alice = await _register(client, "eve@t.com", "eve")
    alice_id = _user_id_from(alice)

    _seed_course("eve-course", "Eve Course", visibility="private", created_by=alice_id)
    _seed_course("platform-1", "Platform Course")

    resp = await client.get("/learning-paths", headers=alice)
    for p in resp.json():
        if p["slug"] == "eve-course":
            assert p["is_mine"] is True
        elif p["slug"] == "platform-1":
            assert p["is_mine"] is False


# ---- Sharing by email ----


@pytest.mark.anyio
async def test_share_makes_course_visible(client: AsyncClient):
    alice = await _register(client, "fay@t.com", "fay")
    bob = await _register(client, "gus@t.com", "gus")
    alice_id = _user_id_from(alice)

    _seed_course("fay-share", "Fay Course", visibility="private", created_by=alice_id)

    resp_before = await client.get("/learning-paths", headers=bob)
    assert not any(p["slug"] == "fay-share" for p in resp_before.json())

    share_resp = await client.post(
        "/learning-paths/fay-share/share",
        json={"email": "gus@t.com"},
        headers=alice,
    )
    assert share_resp.status_code == 200
    assert share_resp.json()["status"] == "shared"

    resp_after = await client.get("/learning-paths", headers=bob)
    assert any(p["slug"] == "fay-share" for p in resp_after.json())


@pytest.mark.anyio
async def test_unshare_removes_access(client: AsyncClient):
    alice = await _register(client, "hal@t.com", "hal")
    bob = await _register(client, "ira@t.com", "ira")
    alice_id = _user_id_from(alice)
    bob_id = _user_id_from(bob)

    _seed_course("hal-unshr", "Hal Course", visibility="private", created_by=alice_id)

    await client.post("/learning-paths/hal-unshr/share", json={"email": "ira@t.com"}, headers=alice)
    await client.delete(f"/learning-paths/hal-unshr/share/{bob_id}", headers=alice)

    resp = await client.get("/learning-paths", headers=bob)
    assert not any(p["slug"] == "hal-unshr" for p in resp.json())


@pytest.mark.anyio
async def test_list_shares(client: AsyncClient):
    alice = await _register(client, "jan@t.com", "jan")
    await _register(client, "kim@t.com", "kim")
    alice_id = _user_id_from(alice)

    _seed_course("jan-list", "Jan Course", visibility="private", created_by=alice_id)
    await client.post("/learning-paths/jan-list/share", json={"email": "kim@t.com"}, headers=alice)

    resp = await client.get("/learning-paths/jan-list/shares", headers=alice)
    assert resp.status_code == 200
    entries = resp.json()
    assert len(entries) == 1
    assert entries[0]["email"] == "kim@t.com"


@pytest.mark.anyio
async def test_non_owner_cannot_share(client: AsyncClient):
    alice = await _register(client, "leo@t.com", "leo")
    await _register(client, "max@t.com", "max")

    _seed_course("pub-course", "Public Course")

    resp = await client.post(
        "/learning-paths/pub-course/share",
        json={"email": "max@t.com"},
        headers=alice,
    )
    assert resp.status_code == 404


# ---- Share link ----


@pytest.mark.anyio
async def test_share_link_flow(client: AsyncClient):
    alice = await _register(client, "ned@t.com", "ned")
    bob = await _register(client, "oak@t.com", "oak")
    alice_id = _user_id_from(alice)

    _seed_course("ned-link", "Ned Course", visibility="private", created_by=alice_id)

    link_resp = await client.post("/learning-paths/ned-link/share-link", headers=alice)
    assert link_resp.status_code == 200
    share_token = link_resp.json()["share_token"]
    assert share_token

    join_resp = await client.post(f"/learning-paths/join/{share_token}", headers=bob)
    assert join_resp.status_code == 200
    assert join_resp.json()["status"] == "joined"
    assert join_resp.json()["slug"] == "ned-link"

    resp = await client.get("/learning-paths", headers=bob)
    assert any(p["slug"] == "ned-link" for p in resp.json())


@pytest.mark.anyio
async def test_invalid_share_token(client: AsyncClient, auth_headers: dict):
    resp = await client.post("/learning-paths/join/bogus-token", headers=auth_headers)
    assert resp.status_code == 404
