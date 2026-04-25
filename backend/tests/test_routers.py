"""Integration tests for the FastAPI router surface.

Tests run against an in-memory-style sqlite (the seeded `sage.db` is reused
between tests). Each test is isolated by registering a fresh user.
"""

from __future__ import annotations

import os
import secrets

import pytest
from fastapi.testclient import TestClient

# Ensure tests use a dedicated DB so they don't clobber developer state.
os.environ.setdefault("DATABASE_URL", "sqlite:///./sage_test.db")

from app.main import app  # noqa: E402


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def auth(client: TestClient) -> tuple[str, dict[str, str]]:
    """Register a unique user and return (email, headers)."""
    email = f"u-{secrets.token_hex(4)}@sage.example.com"
    password = "test-password-123"
    r = client.post("/auth/register", json={"email": email, "name": "Tester", "password": password})
    assert r.status_code == 201, r.text
    r = client.post("/auth/login", data={"username": email, "password": password})
    assert r.status_code == 200, r.text
    return email, {"Authorization": f"Bearer {r.json()['access_token']}"}


# ----- Health / root ------------------------------------------------------


def test_health_ok(client: TestClient) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_root_describes_features(client: TestClient) -> None:
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "sage"
    assert "tutor-streaming" in body["features"]


def test_request_id_header_round_trips(client: TestClient) -> None:
    r = client.get("/health", headers={"X-Request-Id": "abc-123"})
    assert r.headers.get("X-Request-Id") == "abc-123"


# ----- Auth ---------------------------------------------------------------


def test_me_requires_auth(client: TestClient) -> None:
    assert client.get("/auth/me").status_code == 401


def test_register_login_me(client: TestClient, auth: tuple[str, dict[str, str]]) -> None:
    email, headers = auth
    r = client.get("/auth/me", headers=headers)
    assert r.status_code == 200
    assert r.json()["email"] == email
    assert r.json()["teaching_mode"] == "default"


def test_update_teaching_mode(client: TestClient, auth: tuple[str, dict[str, str]]) -> None:
    _, headers = auth
    r = client.patch("/auth/me/mode", headers=headers, json={"mode": "eli5"})
    assert r.status_code == 200, r.text
    assert r.json()["teaching_mode"] == "eli5"


def test_update_teaching_mode_rejects_unknown(
    client: TestClient, auth: tuple[str, dict[str, str]]
) -> None:
    _, headers = auth
    r = client.patch("/auth/me/mode", headers=headers, json={"mode": "rubber-duck"})
    assert r.status_code == 422


# ----- Courses ------------------------------------------------------------


def test_courses_create_list_get_delete(
    client: TestClient, auth: tuple[str, dict[str, str]]
) -> None:
    _, headers = auth
    r = client.post(
        "/courses",
        headers=headers,
        json={"title": "Test Lesson", "subject": "CS", "objective": "x"},
    )
    assert r.status_code == 201, r.text
    cid = r.json()["id"]

    listing = client.get("/courses", headers=headers).json()
    assert any(c["id"] == cid for c in listing)

    detail = client.get(f"/courses/{cid}", headers=headers).json()
    assert detail["title"] == "Test Lesson"

    assert client.delete(f"/courses/{cid}", headers=headers).status_code == 204


# ----- Tutor + replay end-to-end -----------------------------------------


def test_chat_persists_messages_and_concepts(
    client: TestClient, auth: tuple[str, dict[str, str]]
) -> None:
    _, headers = auth
    course = client.post(
        "/courses",
        headers=headers,
        json={
            "title": "Chlorophyll",
            "subject": "Biology",
            "objective": "Chlorophyll absorbs light during photosynthesis.",
        },
    ).json()
    sid = client.post(
        "/tutor/sessions", headers=headers, json={"lesson_id": course["id"]}
    ).json()["id"]

    r = client.get(
        f"/tutor/chat?session_id={sid}&message=Why+is+chlorophyll+green",
        headers=headers,
    )
    assert r.status_code == 200
    events = {l.split(":", 1)[1].strip() for l in r.text.split("\n") if l.startswith("event:")}
    assert {"agent_event", "token", "verification", "done"} <= events

    replay = client.get(f"/replay/{sid}", headers=headers).json()
    assert len(replay["messages"]) >= 2
    assistant = [m for m in replay["messages"] if m["role"] == "assistant"][0]
    assert "agent_trace" in assistant
    assert "plan" in assistant["agent_trace"]


def test_session_for_unknown_lesson_404(
    client: TestClient, auth: tuple[str, dict[str, str]]
) -> None:
    _, headers = auth
    r = client.post("/tutor/sessions", headers=headers, json={"lesson_id": 99_999})
    assert r.status_code == 404


# ----- Concept map --------------------------------------------------------


def test_concept_mastery_bump_clamps(client: TestClient, auth: tuple[str, dict[str, str]]) -> None:
    _, headers = auth
    course = client.post(
        "/courses", headers=headers, json={"title": "M", "subject": "x", "objective": "x"}
    ).json()
    sid = client.post(
        "/tutor/sessions", headers=headers, json={"lesson_id": course["id"]}
    ).json()["id"]
    client.get(
        f"/tutor/chat?session_id={sid}&message=Tell+me+about+vectors",
        headers=headers,
    )
    cm = client.get(f"/concept-map/{sid}", headers=headers).json()
    if not cm:
        pytest.skip("concept extractor produced nothing for stub answer")
    cid = cm[0]["id"]
    r = client.patch(
        f"/concept-map/{sid}/concepts/{cid}/mastery",
        headers=headers,
        json={"delta": 5.0},
    )
    # delta is clamped at the schema layer
    assert r.status_code == 422


# ----- Notes --------------------------------------------------------------


def test_study_plan_returns_markdown(client: TestClient, auth: tuple[str, dict[str, str]]) -> None:
    _, headers = auth
    sid = client.post("/tutor/sessions", headers=headers, json={"lesson_id": None}).json()["id"]
    r = client.post(f"/notes/{sid}/study-plan", headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["filename"].endswith(".md")
    assert "Study plan" in body["markdown"]


# ----- Network ------------------------------------------------------------


def test_peer_match_waiting_then_matched(
    client: TestClient, auth: tuple[str, dict[str, str]]
) -> None:
    _, h1 = auth
    # Second user
    email2 = f"u-{secrets.token_hex(4)}@sage.example.com"
    client.post(
        "/auth/register", json={"email": email2, "name": "Two", "password": "test-password-123"}
    )
    tok2 = client.post(
        "/auth/login", data={"username": email2, "password": "test-password-123"}
    ).json()["access_token"]
    h2 = {"Authorization": f"Bearer {tok2}"}

    r1 = client.post("/network/peer-match", headers=h1, json={"concept": "X-test"}).json()
    assert r1["state"] == "waiting"
    r2 = client.post("/network/peer-match", headers=h2, json={"concept": "X-test"}).json()
    assert r2["state"] == "matched"
    assert r2["room_token"] == r1["room_token"]


# ----- Dashboard ----------------------------------------------------------


def test_course_dashboard(client: TestClient, auth: tuple[str, dict[str, str]]) -> None:
    _, headers = auth
    course = client.post(
        "/courses", headers=headers, json={"title": "D", "subject": "x", "objective": "x"}
    ).json()
    r = client.get(f"/dashboard/course/{course['id']}", headers=headers)
    assert r.status_code == 200
    assert r.json()["course"]["id"] == course["id"]
