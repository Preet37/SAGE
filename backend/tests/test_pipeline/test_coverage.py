"""Stage 3: Coverage assessment — local outline checking + LLM-assessed coverage."""

import pytest

from app.services.course_generator import (
    _assess_one_lesson,
    assess_wiki_coverage,
    assess_wiki_coverage_stream,
    check_outline_coverage,
)
from .conftest import collect_sse, load_fixture, load_llm_response


class TestCheckOutlineCoverage:
    """Pure local function — no LLM needed."""

    def test_identifies_mapped_concepts(self, patch_wiki_dir, sample_outline):
        result = check_outline_coverage(sample_outline)

        assert result["lessons_checked"] == 4
        assert isinstance(result["wiki_topics_used"], list)
        assert "attention-mechanism" in result["wiki_topics_used"]

    def test_reports_unmapped_concepts(self, patch_wiki_dir):
        outline = {
            "modules": [
                {
                    "title": "Test",
                    "lessons": [
                        {
                            "title": "Quantum Attention",
                            "slug": "quantum-attention",
                            "concepts": ["quantum entanglement", "attention mechanism"],
                        }
                    ],
                }
            ]
        }
        result = check_outline_coverage(outline)
        assert "quantum entanglement" in result["concepts_not_in_wiki"]

    def test_empty_outline_returns_zero_lessons(self, patch_wiki_dir):
        result = check_outline_coverage({"modules": []})
        assert result["lessons_checked"] == 0
        assert result["gaps"] == []


class TestAssessWikiCoverage:
    """LLM-assessed coverage — mocked."""

    async def test_categorizes_into_three_buckets(
        self, patch_wiki_dir, mock_generator_llm
    ):
        resolve_resp = load_llm_response("resolve_topics.json")
        coverage_needs = load_llm_response("assess_coverage.json")
        coverage_full = load_llm_response("assess_coverage_full.json")

        call_count = 0

        async def _side_effect(prompt, **kwargs):
            nonlocal call_count
            call_count += 1
            if "concept_map_text" in prompt.lower() or "concept → topic map" in prompt.lower():
                return resolve_resp
            if "self-attention" in prompt.lower() and "covered" not in prompt.lower():
                return resolve_resp
            if "self-attention" in prompt.lower():
                return coverage_full
            return coverage_needs

        mock_generator_llm["_call_llm_json"].side_effect = _side_effect

        lessons = [
            {
                "title": "The Attention Mechanism",
                "slug": "the-attention-mechanism",
                "summary": "How attention works",
                "concepts": ["attention mechanism", "bahdanau attention"],
            },
            {
                "title": "Self-Attention",
                "slug": "self-attention-kqv",
                "summary": "Self-attention computation",
                "concepts": ["self-attention", "masked self-attention"],
            },
        ]

        assessment = await assess_wiki_coverage(lessons)

        assert "fully_covered" in assessment
        assert "needs_research" in assessment
        assert "no_match" in assessment
        total = (
            len(assessment["fully_covered"])
            + len(assessment["needs_research"])
            + len(assessment["no_match"])
        )
        assert total == 2

    async def test_no_match_when_no_topics(self, patch_wiki_dir, mock_generator_llm):
        mock_generator_llm["_call_llm_json"].side_effect = RuntimeError("API down")

        lessons = [
            {
                "title": "Quantum Computing Basics",
                "slug": "quantum-computing",
                "summary": "Intro to quantum computing",
                "concepts": ["qubit", "quantum gate"],
            }
        ]

        assessment = await assess_wiki_coverage(lessons)
        assert len(assessment["no_match"]) == 1
        assert assessment["no_match"][0]["lesson"]["slug"] == "quantum-computing"

    async def test_resolved_topics_preserved(self, patch_wiki_dir, mock_generator_llm):
        resolve_resp = load_llm_response("resolve_topics.json")
        coverage_resp = load_llm_response("assess_coverage.json")

        async def _side_effect(prompt, **kwargs):
            if "concept_map_text" in prompt.lower() or "concept → topic map" in prompt.lower():
                return resolve_resp
            return coverage_resp

        mock_generator_llm["_call_llm_json"].side_effect = _side_effect

        lessons = [
            {
                "title": "Attention",
                "slug": "attention",
                "concepts": ["attention mechanism"],
            }
        ]

        assessment = await assess_wiki_coverage(lessons)
        for bucket in ("fully_covered", "needs_research"):
            for entry in assessment[bucket]:
                assert isinstance(entry["resolved_topics"], set)


class TestAssessOneLessonShared:
    """Tests for the shared _assess_one_lesson helper."""

    async def test_returns_verdict_key(self, patch_wiki_dir, mock_generator_llm):
        resolve_resp = load_llm_response("resolve_topics.json")
        coverage_resp = load_llm_response("assess_coverage.json")

        async def _side_effect(prompt, **kwargs):
            if "concept_map_text" in prompt.lower() or "concept → topic map" in prompt.lower():
                return resolve_resp
            return coverage_resp

        mock_generator_llm["_call_llm_json"].side_effect = _side_effect

        lesson = {
            "title": "Attention",
            "slug": "attention",
            "concepts": ["attention mechanism"],
        }

        result = await _assess_one_lesson(lesson)

        assert "_verdict" in result
        assert result["_verdict"] in ("fully_covered", "needs_research", "no_match")
        assert result["lesson"] is lesson

    async def test_includes_source_count_and_files(self, patch_wiki_dir, mock_generator_llm):
        resolve_resp = load_llm_response("resolve_topics.json")
        coverage_resp = load_llm_response("assess_coverage.json")

        async def _side_effect(prompt, **kwargs):
            if "concept_map_text" in prompt.lower() or "concept → topic map" in prompt.lower():
                return resolve_resp
            return coverage_resp

        mock_generator_llm["_call_llm_json"].side_effect = _side_effect

        lesson = {
            "title": "Attention",
            "slug": "attention",
            "concepts": ["attention mechanism"],
        }

        result = await _assess_one_lesson(lesson)

        assert "source_count" in result
        assert "sources" in result
        assert isinstance(result["sources"], list)
        assert result["source_count"] == len(result["sources"])

    async def test_no_match_for_unknown_concepts(self, patch_wiki_dir, mock_generator_llm):
        mock_generator_llm["_call_llm_json"].side_effect = RuntimeError("API down")

        lesson = {
            "title": "Quantum Stuff",
            "slug": "quantum",
            "concepts": ["qubit"],
        }

        result = await _assess_one_lesson(lesson)
        assert result["_verdict"] == "no_match"
        assert "unmapped" in result


class TestAssessWikiCoverageStream:
    """Streaming version of assess — emits per-lesson SSE events."""

    async def test_emits_events_per_lesson(self, patch_wiki_dir, mock_generator_llm):
        resolve_resp = load_llm_response("resolve_topics.json")
        coverage_needs = load_llm_response("assess_coverage.json")

        async def _side_effect(prompt, **kwargs):
            if "concept_map_text" in prompt.lower() or "concept → topic map" in prompt.lower():
                return resolve_resp
            return coverage_needs

        mock_generator_llm["_call_llm_json"].side_effect = _side_effect

        lessons = [
            {"title": "Attention", "slug": "att", "concepts": ["attention mechanism"]},
            {"title": "Transformer", "slug": "tfm", "concepts": ["self-attention"]},
        ]

        events = await collect_sse(assess_wiki_coverage_stream(lessons))

        assert events[0]["type"] == "status"
        lesson_events = [e for e in events if e["type"] == "lesson_assessed"]
        assert len(lesson_events) == 2

        for ev in lesson_events:
            assert "slug" in ev
            assert "verdict" in ev
            assert "source_count" in ev
            assert ev["verdict"] in ("fully_covered", "needs_research", "no_match")

        complete = [e for e in events if e["type"] == "assessment_complete"]
        assert len(complete) == 1
        s = complete[0]["summary"]
        assert s["fully_covered"] + s["needs_research"] + s["no_match"] == 2

        assert events[-1]["type"] == "done"

    async def test_stream_matches_batch_results(self, patch_wiki_dir, mock_generator_llm):
        """Streaming and batch assessment should produce the same verdicts."""
        resolve_resp = load_llm_response("resolve_topics.json")
        coverage_resp = load_llm_response("assess_coverage.json")

        async def _side_effect(prompt, **kwargs):
            if "concept_map_text" in prompt.lower() or "concept → topic map" in prompt.lower():
                return resolve_resp
            return coverage_resp

        mock_generator_llm["_call_llm_json"].side_effect = _side_effect

        lessons = [
            {"title": "Attention", "slug": "att", "concepts": ["attention mechanism"]},
        ]

        batch = await assess_wiki_coverage(lessons)
        events = await collect_sse(assess_wiki_coverage_stream(lessons))

        lesson_events = [e for e in events if e["type"] == "lesson_assessed"]
        stream_slugs = {e["slug"] for e in lesson_events}

        batch_slugs = set()
        for bucket in ("fully_covered", "needs_research", "no_match"):
            for entry in batch[bucket]:
                batch_slugs.add(entry["lesson"]["slug"])

        assert stream_slugs == batch_slugs

    async def test_no_match_lesson_emits_unmapped(self, patch_wiki_dir, mock_generator_llm):
        mock_generator_llm["_call_llm_json"].side_effect = RuntimeError("API down")

        lessons = [
            {"title": "Quantum", "slug": "quantum", "concepts": ["qubit"]},
        ]

        events = await collect_sse(assess_wiki_coverage_stream(lessons))
        lesson_events = [e for e in events if e["type"] == "lesson_assessed"]

        assert len(lesson_events) == 1
        assert lesson_events[0]["verdict"] == "no_match"
        assert "qubit" in lesson_events[0]["unmapped"]
