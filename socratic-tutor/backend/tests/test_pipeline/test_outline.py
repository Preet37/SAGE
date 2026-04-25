"""Stage 2: Outline generation — SSE events, structure validation."""

import pytest

from app.services.course_generator import generate_outline
from .conftest import collect_sse, load_llm_response


class TestGenerateOutlineMocked:
    async def test_produces_sse_events(self, patch_wiki_dir, mock_generator_llm):
        mock_generator_llm["_call_llm_json"].return_value = load_llm_response(
            "generate_outline.json"
        )

        events = await collect_sse(generate_outline("Test course on attention", "prompt"))

        types = [e["type"] for e in events]
        assert "status" in types
        assert "outline" in types
        assert "done" in types

    async def test_outline_has_modules_and_lessons(
        self, patch_wiki_dir, mock_generator_llm
    ):
        mock_generator_llm["_call_llm_json"].return_value = load_llm_response(
            "generate_outline.json"
        )

        events = await collect_sse(generate_outline("Test course on attention", "prompt"))
        outline_event = next(e for e in events if e["type"] == "outline")
        outline = outline_event["data"]

        assert "title" in outline
        assert "modules" in outline
        modules = outline["modules"]
        assert len(modules) >= 2

        for mod in modules:
            assert "title" in mod
            assert "lessons" in mod
            for lesson in mod["lessons"]:
                assert "title" in lesson
                assert "slug" in lesson
                assert "concepts" in lesson
                assert isinstance(lesson["concepts"], list)

    async def test_error_event_on_llm_failure(
        self, patch_wiki_dir, mock_generator_llm
    ):
        mock_generator_llm["_call_llm_json"].side_effect = RuntimeError("LLM unavailable")

        events = await collect_sse(generate_outline("Test course", "prompt"))
        types = [e["type"] for e in events]
        assert "error" in types
        assert "done" not in types


@pytest.mark.llm
class TestGenerateOutlineReal:
    async def test_real_llm_produces_valid_outline(self, patch_wiki_dir):
        """Run with real LLM — structural assertions only."""
        events = await collect_sse(
            generate_outline(
                "Create a short 2-lesson course on the basics of attention mechanisms.",
                "prompt",
            )
        )
        outline_events = [e for e in events if e["type"] == "outline"]
        assert len(outline_events) == 1

        outline = outline_events[0]["data"]
        assert "modules" in outline
        assert len(outline["modules"]) >= 1
