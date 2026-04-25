"""Stage 1: Wiki readiness — concept map parsing, wiki context loading, dedup."""

import pytest

from app.services.course_generator import (
    _load_concept_map,
    resolve_topics_exact,
    load_wiki_context,
    resolve_topics_llm,
)
from .conftest import load_llm_response


class TestLoadConceptMap:
    def test_parses_slugs(self, patch_wiki_dir):
        cmap = _load_concept_map()

        assert "attention mechanism" in cmap
        assert cmap["attention mechanism"] == "attention-mechanism"
        assert "self-attention" in cmap
        assert cmap["self-attention"] == "self-attention"
        assert "transformer" in cmap
        assert cmap["transformer"] == "transformer-architecture"

    def test_returns_dict_of_strings(self, patch_wiki_dir):
        cmap = _load_concept_map()
        assert isinstance(cmap, dict)
        for concept, slug in cmap.items():
            assert isinstance(concept, str)
            assert isinstance(slug, str)
            assert concept == concept.lower()

    def test_empty_when_no_file(self, tmp_path, monkeypatch):
        import app.services.course_generator as mod

        monkeypatch.setattr(mod, "_CONCEPT_MAP_PATH", tmp_path / "nonexistent.md")
        monkeypatch.setattr(mod, "_wiki_concept_map", None)

        cmap = _load_concept_map()
        assert cmap == {}


class TestResolveTopicsExact:
    def test_maps_known_concepts(self, patch_wiki_dir):
        result = resolve_topics_exact(["attention mechanism", "self-attention"])
        assert "attention-mechanism" in result["topic_slugs"]
        assert "self-attention" in result["topic_slugs"]
        assert result["unmapped"] == []

    def test_reports_unmapped(self, patch_wiki_dir):
        result = resolve_topics_exact(["attention mechanism", "quantum computing"])
        assert "quantum computing" in result["unmapped"]
        assert "attention-mechanism" in result["topic_slugs"]

    def test_case_insensitive(self, patch_wiki_dir):
        result = resolve_topics_exact(["Attention Mechanism", "SELF-ATTENTION"])
        assert "attention-mechanism" in result["topic_slugs"]
        assert "self-attention" in result["topic_slugs"]


class TestResolveTopicsLLM:
    async def test_mocked_returns_structure(self, patch_wiki_dir, mock_generator_llm):
        mock_generator_llm["_call_llm_json"].return_value = load_llm_response(
            "resolve_topics.json"
        )

        result = await resolve_topics_llm(
            ["attention mechanism", "self-attention", "sparse attention"],
            lesson_title="Test Lesson",
        )

        assert isinstance(result["topic_slugs"], set)
        assert "attention-mechanism" in result["topic_slugs"]
        assert "self-attention" in result["topic_slugs"]
        assert "sparse attention" in result["unmapped"]

    async def test_falls_back_on_llm_error(self, patch_wiki_dir, mock_generator_llm):
        mock_generator_llm["_call_llm_json"].side_effect = RuntimeError("API down")

        result = await resolve_topics_llm(
            ["attention mechanism", "self-attention"],
            lesson_title="Test Lesson",
        )

        assert "attention-mechanism" in result["topic_slugs"]
        assert "self-attention" in result["topic_slugs"]

    async def test_empty_concepts_returns_empty(self, patch_wiki_dir):
        result = await resolve_topics_llm([], lesson_title="Test")
        assert result["topic_slugs"] == set()
        assert result["unmapped"] == []


class TestLoadWikiContext:
    def test_returns_content(self, patch_wiki_dir):
        ctx = load_wiki_context(
            ["attention mechanism"],
            topic_slugs={"attention-mechanism"},
        )
        assert "attention-mechanism" in ctx["topics"]
        assert "attention-mechanism" in ctx["resource_pages"]
        assert len(ctx["resource_pages"]["attention-mechanism"]) > 0

    def test_loads_source_files(self, patch_wiki_dir):
        ctx = load_wiki_context(
            ["attention mechanism"],
            topic_slugs={"attention-mechanism"},
        )
        sources = ctx["source_content"].get("attention-mechanism", [])
        assert len(sources) >= 1
        assert any("jalammar" in s["file"] for s in sources)

    def test_extracts_youtube_ids(self, patch_wiki_dir):
        ctx = load_wiki_context(
            ["attention mechanism"],
            topic_slugs={"attention-mechanism"},
        )
        yt = ctx["youtube_ids"].get("attention-mechanism", [])
        yt_ids = [vid_id for vid_id, _ in yt]
        assert "eMlx5fFNoYc" in yt_ids

    def test_extracts_recommended_reading(self, patch_wiki_dir):
        ctx = load_wiki_context(
            ["attention mechanism"],
            topic_slugs={"attention-mechanism"},
        )
        reading = ctx["recommended_reading"].get("attention-mechanism", [])
        urls = [url for _, url in reading]
        assert any("jalammar.github.io" in u for u in urls)

    def test_dedup_across_topics(self, patch_wiki_dir):
        ctx = load_wiki_context(
            ["attention mechanism", "self-attention"],
            topic_slugs={"attention-mechanism", "self-attention"},
        )
        all_files = []
        for topic_sources in ctx["source_content"].values():
            for src in topic_sources:
                all_files.append(src["file"])

        assert len(all_files) == len(set(all_files)), "Duplicate source files detected"

    def test_falls_back_to_exact_when_no_slugs(self, patch_wiki_dir):
        ctx = load_wiki_context(["attention mechanism"])
        assert "attention-mechanism" in ctx["topics"]

    def test_unknown_slug_returns_empty(self, patch_wiki_dir):
        ctx = load_wiki_context(
            ["nonexistent"],
            topic_slugs={"nonexistent-topic"},
        )
        assert ctx["topics"] == ["nonexistent-topic"]
        assert ctx["resource_pages"] == {}
        assert ctx["source_content"] == {}
