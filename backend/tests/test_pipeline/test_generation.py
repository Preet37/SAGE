"""Stage 5: Content generation — dedup, structural notes, lesson bundle."""

import pytest

from app.services.course_generator import (
    deduplicate_youtube_ids,
    file_structural_note,
    generate_lesson_bundle,
    load_wiki_context,
)
from .conftest import load_llm_response


class TestDeduplicateYoutubeIds:
    def test_caps_at_max_appearances(self):
        lessons = {
            "lesson-1": {"youtube_id": "abc123def45", "video_title": "V1"},
            "lesson-2": {"youtube_id": "abc123def45", "video_title": "V1"},
            "lesson-3": {"youtube_id": "abc123def45", "video_title": "V1"},
        }

        deduplicate_youtube_ids(lessons)

        yt_present = sum(1 for l in lessons.values() if l.get("youtube_id"))
        assert yt_present == 2

    def test_uses_alt_videos_as_fallback(self):
        lessons = {
            "lesson-1": {"youtube_id": "abc123def45"},
            "lesson-2": {"youtube_id": "abc123def45"},
            "lesson-3": {"youtube_id": "abc123def45"},
        }
        alt_videos = {
            "lesson-3": [("xyz987uvw65", "Alternative Video")],
        }

        deduplicate_youtube_ids(lessons, alt_videos=alt_videos)

        assert lessons["lesson-3"].get("youtube_id") == "xyz987uvw65"
        assert lessons["lesson-3"].get("video_title") == "Alternative Video"

    def test_no_change_when_under_limit(self):
        lessons = {
            "lesson-1": {"youtube_id": "abc123def45"},
            "lesson-2": {"youtube_id": "xyz987uvw65"},
        }

        deduplicate_youtube_ids(lessons)

        assert lessons["lesson-1"]["youtube_id"] == "abc123def45"
        assert lessons["lesson-2"]["youtube_id"] == "xyz987uvw65"

    def test_handles_missing_youtube_ids(self):
        lessons = {
            "lesson-1": {"content": "No video"},
            "lesson-2": {"youtube_id": "abc123def45"},
        }

        deduplicate_youtube_ids(lessons)
        assert "youtube_id" not in lessons["lesson-1"]
        assert lessons["lesson-2"]["youtube_id"] == "abc123def45"

    def test_returns_same_dict(self):
        lessons = {"a": {"youtube_id": "abc123def45"}}
        result = deduplicate_youtube_ids(lessons)
        assert result is lessons


class TestFileStructuralNote:
    def test_writes_pending_item(self, patch_wiki_dir, mini_wiki):
        pending_dir = mini_wiki["wiki_dir"] / ".pending"

        result = file_structural_note(
            "attention-mechanism",
            concept="Attention Variants",
            sub_concepts=["sparse attention", "linear attention"],
            course_title="Test Course",
        )
        assert result is True

        # Page should NOT be modified directly
        content = (mini_wiki["topics_dir"] / "attention-mechanism.md").read_text()
        assert "Attention Variants" not in content

        # Pending item should exist
        import json
        pending_files = list(pending_dir.glob("*_structural_note_attention-mechanism.json"))
        assert len(pending_files) == 1
        item = json.loads(pending_files[0].read_text())
        assert item["type"] == "structural_note"
        assert item["data"]["concept"] == "Attention Variants"
        assert "sparse attention" in item["data"]["sub_concepts"]
        assert "Test Course" in item["data"]["note_text"]

    def test_always_returns_true(self, patch_wiki_dir, mini_wiki):
        result = file_structural_note(
            "nonexistent-topic",
            concept="Test",
            sub_concepts=["sub1"],
        )
        assert result is True


class TestGenerateLessonBundle:
    async def test_mocked_returns_content_and_kb(
        self, patch_wiki_dir, mock_generator_llm
    ):
        content_resp = load_llm_response("generate_bundle.json")
        kb_text = "# Reference KB\n\nAttention mechanism reference material..."

        mock_generator_llm["_call_llm_json"].return_value = content_resp
        mock_generator_llm["_call_llm"].return_value = kb_text

        lesson = {
            "title": "The Attention Mechanism",
            "slug": "the-attention-mechanism",
            "summary": "How attention works",
            "concepts": ["attention mechanism", "bahdanau attention"],
        }
        wiki_ctx = load_wiki_context(
            ["attention mechanism"],
            topic_slugs={"attention-mechanism"},
        )

        bundle = await generate_lesson_bundle(lesson, wiki_ctx)

        assert "content" in bundle
        assert "reference_kb" in bundle
        assert "wiki_meta" in bundle

        content = bundle["content"]
        assert content["title"] == "The Attention Mechanism"
        assert content["slug"] == "the-attention-mechanism"
        assert "error" not in content

        assert isinstance(bundle["reference_kb"], str)
        assert len(bundle["reference_kb"]) > 0

    async def test_handles_llm_failure_gracefully(
        self, patch_wiki_dir, mock_generator_llm
    ):
        mock_generator_llm["_call_llm_json"].side_effect = RuntimeError("API error")
        mock_generator_llm["_call_llm"].side_effect = RuntimeError("API error")

        lesson = {
            "title": "Test",
            "slug": "test",
            "concepts": ["attention mechanism"],
        }
        wiki_ctx = load_wiki_context(
            ["attention mechanism"],
            topic_slugs={"attention-mechanism"},
        )

        bundle = await generate_lesson_bundle(lesson, wiki_ctx)

        assert "error" in bundle["content"]
        assert bundle["reference_kb"] == ""
