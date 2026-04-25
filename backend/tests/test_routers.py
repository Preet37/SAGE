"""Integration tests for the current FastAPI router surface."""

from __future__ import annotations

import asyncio
import os
import secrets
from pathlib import Path

from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite:///./sage_test.db")
os.environ.setdefault("RATE_LIMIT_DISABLED", "1")
Path("sage_test.db").unlink(missing_ok=True)

from app.database import AsyncSessionLocal, create_tables  # noqa: E402
from app.main import app  # noqa: E402
from app.models.concept import ConceptEdge, ConceptNode  # noqa: E402
from app.models.lesson import Course, Lesson, LessonChunk  # noqa: E402


def _run(coro):
    return asyncio.run(coro)


async def _seed_course(title: str = "Biology") -> dict[str, int | str]:
    await create_tables()
    slug = f"course-{secrets.token_hex(4)}"
    lesson_slug = f"lesson-{secrets.token_hex(4)}"
    async with AsyncSessionLocal() as db:
        course = Course(
            slug=slug,
            title=title,
            description="Seeded test course",
            level="beginner",
            tags=["test"],
        )
        db.add(course)
        await db.flush()
        lesson = Lesson(
            course_id=course.id,
            slug=lesson_slug,
            title="Photosynthesis",
            order=1,
            summary="How plants convert light.",
            content_md="Photosynthesis converts light energy into chemical energy. Chlorophyll absorbs light.",
            key_concepts=["Photosynthesis", "Chlorophyll"],
            estimated_minutes=15,
        )
        db.add(lesson)
        await db.flush()
        db.add(LessonChunk(lesson_id=lesson.id, chunk_index=0, text=lesson.content_md))
        n1 = ConceptNode(course_id=course.id, lesson_id=lesson.id, label="Photosynthesis")
        n2 = ConceptNode(course_id=course.id, lesson_id=lesson.id, label="Chlorophyll")
        db.add_all([n1, n2])
        await db.flush()
        db.add(ConceptEdge(source_id=n1.id, target_id=n2.id, edge_type="relates", weight=1.0))
        await db.commit()
        return {
            "course_id": course.id,
            "course_slug": slug,
            "lesson_id": lesson.id,
            "lesson_slug": lesson_slug,
            "concept_id": n1.id,
        }


def _register(client: TestClient) -> tuple[str, dict[str, str]]:
    email = f"u-{secrets.token_hex(4)}@sage.example.com"
    password = "test-password-123"
    r = client.post(
        "/auth/register",
        json={
            "email": email,
            "username": email.split("@")[0],
            "display_name": "Tester",
            "password": password,
        },
    )
    assert r.status_code == 200, r.text
    r = client.post("/auth/token", data={"username": email, "password": password})
    assert r.status_code == 200, r.text
    return email, {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_health_root_and_request_id() -> None:
    with TestClient(app) as client:
        assert client.get("/health").json()["status"] == "ok"
        root = client.get("/").json()
        assert root["service"] == "sage"
        assert "tutor-streaming" in root["features"]
        r = client.get("/health", headers={"X-Request-Id": "abc-123"})
        assert r.headers["X-Request-Id"] == "abc-123"
        r = client.get("/health", headers={"X-Request-Id": "bad\nid"})
        assert "\n" not in r.headers["X-Request-Id"]


def test_auth_register_login_me_and_mode() -> None:
    with TestClient(app) as client:
        email, headers = _register(client)
        me = client.get("/auth/me", headers=headers)
        assert me.status_code == 200
        assert me.json()["email"] == email
        mode = client.patch("/auth/me/mode", headers=headers, json={"mode": "eli5"})
        assert mode.status_code == 200
        assert mode.json()["teaching_mode"] == "eli5"
        assert client.patch("/auth/me/mode", headers=headers, json={"mode": "bad"}).status_code == 422


def test_courses_lessons_and_concept_map() -> None:
    seeded = _run(_seed_course())
    with TestClient(app) as client:
        _, headers = _register(client)
        courses = client.get("/courses/").json()
        assert any(c["id"] == seeded["course_id"] for c in courses)
        lesson = client.get(
            f"/courses/{seeded['course_slug']}/lessons/{seeded['lesson_slug']}"
        ).json()
        assert lesson["course_id"] == seeded["course_id"]
        assert "Photosynthesis converts" in lesson["content_md"]
        concept_map = client.get(f"/concept-map/{seeded['course_id']}", headers=headers).json()
        assert len(concept_map["nodes"]) >= 2
        mastery = client.post(
            "/concept-map/mastery",
            headers=headers,
            json={"concept_id": seeded["concept_id"], "score": 1.5},
        ).json()
        assert mastery["score"] == 1.0
        next_concepts = client.get(f"/concept-map/next/{seeded['course_id']}", headers=headers).json()
        assert isinstance(next_concepts, list)


def test_tutor_stream_persists_replay(monkeypatch) -> None:
    seeded = _run(_seed_course())

    async def fake_stream(system_prompt, messages):
        yield "Photosynthesis converts light energy. "
        yield "Chlorophyll absorbs light in plants."

    monkeypatch.setattr("app.routers.tutor._stream_anthropic", fake_stream)
    monkeypatch.setattr("app.routers.tutor._stream_openai", fake_stream)

    with TestClient(app) as client:
        _, headers = _register(client)
        s = client.post(
            "/tutor/session",
            headers=headers,
            json={"lesson_id": seeded["lesson_id"], "teaching_mode": "default"},
        )
        assert s.status_code == 200, s.text
        session_id = s.json()["session_id"]
        r = client.post(
            "/tutor/chat",
            headers=headers,
            json={
                "lesson_id": seeded["lesson_id"],
                "session_id": session_id,
                "message": "Why is chlorophyll useful?",
                "history": [],
            },
        )
        assert r.status_code == 200
        events = {line.split(":", 1)[1].strip() for line in r.text.splitlines() if line.startswith("event:")}
        assert {"agent_event", "token", "verification", "done"} <= events
        replay = client.get(f"/replay/sessions/{session_id}", headers=headers).json()
        assert len(replay["turns"]) == 2
        assert replay["turns"][1]["agent_trace"]["events"]


def test_network_dashboard_accessibility_and_notes(monkeypatch) -> None:
    seeded = _run(_seed_course("Network"))

    async def fake_complete(prompt: str, system: str = "", max_tokens: int = 512) -> str:
        if "Return ONLY this JSON" in prompt:
            return '{"revised":"Improved notes","gaps_identified":[],"concept_connections":[],"misconceptions":[],"strength_score":0.8,"suggestions":["Add examples"]}'
        return "# Study plan\n\nUse chlorophyll examples."

    monkeypatch.setattr("app.agents.base.asi1_complete", fake_complete)

    with TestClient(app) as client:
        _, h1 = _register(client)
        _, h2 = _register(client)
        wait = client.post(
            "/network/peer-match",
            headers=h1,
            json={"concept_id": seeded["concept_id"], "lesson_id": seeded["lesson_id"]},
        ).json()
        match = client.post(
            "/network/peer-match",
            headers=h2,
            json={"concept_id": seeded["concept_id"], "lesson_id": seeded["lesson_id"]},
        ).json()
        assert wait["waiting"] is True
        assert match["matched"] is True

        overview = client.get("/dashboard/overview", headers=h1)
        assert overview.status_code == 200
        course = client.get(f"/dashboard/course/{seeded['course_id']}", headers=h1)
        assert course.status_code == 200

        saved = client.post(
            "/accessibility/me",
            headers=h1,
            json={"disabilities": ["adhd"], "strengths": ["visual_learner"], "custom_note": "brief"},
        )
        assert saved.status_code == 200

        revised = client.post(
            "/notes/revise",
            headers=h1,
            json={"lesson_id": seeded["lesson_id"], "content": "chlorophyll notes"},
        )
        assert revised.status_code == 200
        assert revised.json()["revised"] == "Improved notes"

        plan = client.post(f"/notes/generate-plan?lesson_id={seeded['lesson_id']}", headers=h1)
        assert plan.status_code == 200
        assert plan.json()["download_filename"].endswith(".md")
