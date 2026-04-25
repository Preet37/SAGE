"""Stage 4: Enrichment — query generation, bootstrap, curation, proposals."""

import json
from pathlib import Path

import pytest

from app.services.course_enricher import generate_queries, run_search
from app.services.wiki_downloader import (
    _extract_youtube_id,
    _save_video_stub,
    bootstrap_new_wiki_topic,
    enrich_wiki_topic,
    get_existing_source_urls,
    _get_existing_source_details,
    save_proposals,
    save_curation_report,
    curate_best_sources,
    audit_curation,
)
from .conftest import collect_sse, load_llm_response


class TestGenerateQueriesConceptGaps:
    """When concept_gaps are provided, query generation skips LLM entirely."""

    async def test_concept_gaps_path_no_llm(self):
        lessons = [
            {
                "title": "Attention Basics",
                "slug": "attention-basics",
                "concepts": ["attention mechanism"],
            }
        ]
        concept_gaps = {
            "attention-basics": ["additive attention", "alignment models"],
        }

        events = await collect_sse(
            generate_queries(
                lessons,
                wiki_available=True,
                concept_gaps=concept_gaps,
            )
        )

        progress = [e for e in events if e.get("type") == "progress"]
        assert len(progress) == 1
        assert progress[0]["status"] == "done"
        assert progress[0]["query_count"] == 2

        queries_event = next(e for e in events if e["type"] == "queries")
        data = queries_event["data"]
        assert "attention-basics" in data
        assert "enrichment" in data["attention-basics"]
        assert len(data["attention-basics"]["enrichment"]) == 2

    async def test_query_text_contains_gap(self):
        lessons = [{"title": "T", "slug": "t", "concepts": []}]
        concept_gaps = {"t": ["flash attention optimization"]}

        events = await collect_sse(
            generate_queries(lessons, concept_gaps=concept_gaps)
        )
        queries_event = next(e for e in events if e["type"] == "queries")
        q_text = queries_event["data"]["t"]["enrichment"][0]
        assert "flash attention optimization" in q_text


class TestRunSearch:
    async def test_returns_search_results(self, mock_search):
        mock_search.return_value = {
            "content": "Attention is a mechanism...",
            "citations": [
                {"url": "https://example.com/attn", "title": "Attention Guide"}
            ],
            "content_length": 500,
        }

        queries = {
            "attention-basics": {
                "enrichment": ["best teaching resource: additive attention"],
            }
        }

        events = await collect_sse(run_search(queries))

        result_event = next(e for e in events if e["type"] == "search_results")
        assert "attention-basics" in result_event["data"]

        done_events = [e for e in events if e["type"] == "done"]
        assert len(done_events) == 1


class TestBootstrapNewWikiTopic:
    def test_writes_pending_item_and_creates_subdir(self, patch_wiki_dir, mini_wiki):
        topics_dir = mini_wiki["topics_dir"]
        pending_dir = mini_wiki["wiki_dir"] / ".pending"

        slug = bootstrap_new_wiki_topic(
            "flash-attention",
            ["flash attention", "io-aware attention"],
            "Flash Attention Optimization",
        )

        assert slug == "flash-attention"
        # Page should NOT be created directly
        page = topics_dir / "flash-attention.md"
        assert not page.exists()
        # Subdirectory for downloads should exist
        assert (topics_dir / "flash-attention").is_dir()
        # Concept map should NOT be updated directly
        cm = (mini_wiki["wiki_dir"] / "concept-map.md").read_text()
        assert "flash-attention" not in cm
        # Pending item should exist
        assert pending_dir.exists()
        pending_files = list(pending_dir.glob("*_new_topic_flash-attention.json"))
        assert len(pending_files) == 1
        import json
        item = json.loads(pending_files[0].read_text())
        assert item["type"] == "new_topic"
        assert item["topic_slug"] == "flash-attention"
        assert "Flash Attention Optimization" in item["data"]["page_content"]
        assert "flash-attention" in item["data"]["concept_map_entry"]

    def test_idempotent_if_page_exists(self, patch_wiki_dir, mini_wiki):
        topics_dir = mini_wiki["topics_dir"]
        existing = topics_dir / "attention-mechanism.md"
        before = existing.read_text()

        slug = bootstrap_new_wiki_topic(
            "attention-mechanism",
            ["attention mechanism"],
            "Attention",
        )
        assert slug == "attention-mechanism"
        assert existing.read_text() == before


class TestGetExistingSourceUrls:
    def test_scans_source_headers(self, patch_wiki_dir):
        urls = get_existing_source_urls("attention-mechanism")
        assert "https://jalammar.github.io/illustrated-transformer/" in urls

    def test_empty_for_missing_dir(self, patch_wiki_dir):
        urls = get_existing_source_urls("nonexistent-topic")
        assert urls == set()


class TestGetExistingSourceDetails:
    def test_returns_url_and_title(self, patch_wiki_dir):
        details = _get_existing_source_details("attention-mechanism")
        assert len(details) >= 1
        assert any(d["url"].startswith("https://") for d in details)
        assert all("title" in d for d in details)


class TestSaveProposals:
    def test_write_and_append(self, patch_wiki_dir, mini_wiki):
        proposals = [
            {"url": "https://example.com/a", "title": "Source A"},
            {"url": "https://example.com/b", "title": "Source B"},
        ]

        save_proposals("attention-mechanism", proposals, run_label="test-run-1")

        path = mini_wiki["topics_dir"] / "attention-mechanism" / "proposals.json"
        assert path.exists()
        data = json.loads(path.read_text())
        assert len(data) == 1
        assert data[0]["run_label"] == "test-run-1"
        assert len(data[0]["sources"]) == 2

        # Append a second run
        save_proposals("attention-mechanism", [{"url": "https://example.com/c"}], run_label="test-run-2")
        data = json.loads(path.read_text())
        assert len(data) == 2


class TestSaveCurationReport:
    def test_creates_markdown_report(self, patch_wiki_dir, mini_wiki):
        curation = {
            "picks": [{"url": "https://example.com/pick", "title": "Pick", "role": "paper", "why": "Good"}],
            "near_misses": [{"title": "NM", "why_not": "Overlap"}],
            "uncovered_gaps": ["gap1"],
            "reasoning": "Test reasoning",
            "all_candidates": [],
        }
        audit = {
            "verdict": "good",
            "summary": "All good",
            "promotions": [],
        }

        save_curation_report(
            "attention-mechanism",
            "Test Lesson",
            curation=curation,
            audit=audit,
            existing_details=[],
            download_result={"saved": 1, "failed": 0},
        )

        report_path = mini_wiki["topics_dir"] / "attention-mechanism" / "curation-report.md"
        assert report_path.exists()
        content = report_path.read_text()
        assert "Test Lesson" in content


class TestCurateBestSources:
    async def test_mocked_returns_picks(self, patch_wiki_dir, mock_downloader_llm):
        mock_downloader_llm.return_value = load_llm_response("curate_sources.json")

        result = await curate_best_sources(
            "Attention Basics",
            ["additive attention"],
            {"additive attention": [{"content": "...", "citations": [{"url": "https://arxiv.org/abs/1409.0473", "title": "Bahdanau"}]}]},
            set(),
            topic_slug="attention-mechanism",
        )

        assert "picks" in result
        assert len(result["picks"]) >= 1
        assert "all_candidates" in result
        assert "near_misses" in result

    async def test_empty_when_no_candidates(self, patch_wiki_dir, mock_downloader_llm):
        result = await curate_best_sources(
            "Attention",
            ["gap1"],
            {"gap1": []},
            set(),
        )
        assert result["picks"] == []


class TestAuditCuration:
    async def test_mocked_returns_verdict(self, patch_wiki_dir, mock_downloader_llm):
        mock_downloader_llm.return_value = load_llm_response("audit_curation.json")

        curation_result = {
            "picks": [{"url": "https://example.com", "title": "T", "role": "paper"}],
            "near_misses": [],
            "uncovered_gaps": ["gap1"],
            "all_candidates": [],
        }

        result = await audit_curation(
            "Test Lesson",
            curation_result,
            all_candidates_by_url={"https://example.com": {"url": "https://example.com", "title": "T", "snippet": "..."}},
            existing_details=[],
        )

        assert result["verdict"] == "good"
        assert "promotions" in result
        assert isinstance(result["promotions"], list)


# ---------------------------------------------------------------------------
# Video metadata path tests
# ---------------------------------------------------------------------------

class TestExtractYoutubeId:
    def test_standard_watch_url(self):
        assert _extract_youtube_id("https://www.youtube.com/watch?v=TzJecWCbex0") == "TzJecWCbex0"

    def test_short_url(self):
        assert _extract_youtube_id("https://youtu.be/H6LchswC74Y") == "H6LchswC74Y"

    def test_embed_url(self):
        assert _extract_youtube_id("https://www.youtube.com/embed/7sRV5rcMVTY") == "7sRV5rcMVTY"

    def test_with_extra_params(self):
        assert _extract_youtube_id("https://www.youtube.com/watch?v=abc123def45&t=120") == "abc123def45"

    def test_non_youtube_url(self):
        assert _extract_youtube_id("https://example.com/page") is None

    def test_empty_string(self):
        assert _extract_youtube_id("") is None


class TestSaveVideoStub:
    async def test_creates_stub_with_oembed(self, patch_wiki_dir, mini_wiki, monkeypatch):
        import app.services.wiki_downloader as dl_mod

        async def mock_oembed(yt_id):
            return {"title": "Great Tutorial", "author_name": "Anthropic"}

        monkeypatch.setattr(dl_mod, "_fetch_oembed", mock_oembed)
        monkeypatch.setattr(dl_mod, "_fetch_transcript", lambda yt_id: "Hello world this is a transcript")

        result = await _save_video_stub(
            "https://www.youtube.com/watch?v=TzJecWCbex0",
            "attention-mechanism",
            title="Test Video",
        )

        assert result["saved"] is True
        assert result["via"] == "video-metadata"
        content = Path(result["path"]).read_text()
        assert "# youtube_id: TzJecWCbex0" in content
        assert "# Type: video" in content
        assert "# Author: Anthropic" in content
        assert "Hello world this is a transcript" in content

    async def test_idempotent_skip(self, patch_wiki_dir, mini_wiki, monkeypatch):
        import app.services.wiki_downloader as dl_mod

        async def mock_oembed(yt_id):
            return {"title": "T", "author_name": "A"}

        monkeypatch.setattr(dl_mod, "_fetch_oembed", mock_oembed)
        monkeypatch.setattr(dl_mod, "_fetch_transcript", lambda yt_id: "text")

        r1 = await _save_video_stub("https://youtu.be/TzJecWCbex0", "attention-mechanism")
        assert r1["saved"] is True

        r2 = await _save_video_stub("https://youtu.be/TzJecWCbex0", "attention-mechanism")
        assert r2["saved"] is False
        assert r2["reason"] == "already exists"

    async def test_non_youtube_still_creates_stub(self, patch_wiki_dir, mini_wiki, monkeypatch):
        import app.services.wiki_downloader as dl_mod

        async def mock_oembed(yt_id):
            return {}

        monkeypatch.setattr(dl_mod, "_fetch_oembed", mock_oembed)
        monkeypatch.setattr(dl_mod, "_fetch_transcript", lambda yt_id: "")

        result = await _save_video_stub(
            "https://vimeo.com/12345",
            "attention-mechanism",
            title="Vimeo Video",
        )

        assert result["saved"] is True
        content = Path(result["path"]).read_text()
        assert "# Type: video" in content
        assert "youtube_id" not in content


class TestEnrichWikiTopicVideoRouting:
    async def test_video_role_uses_stub_path(self, patch_wiki_dir, mini_wiki, monkeypatch):
        import app.services.wiki_downloader as dl_mod

        async def mock_oembed(yt_id):
            return {"title": "Claude Skills Tutorial", "author_name": "Anthropic"}

        monkeypatch.setattr(dl_mod, "_fetch_oembed", mock_oembed)
        monkeypatch.setattr(dl_mod, "_fetch_transcript", lambda yt_id: "Some transcript content")

        sources = [
            {"url": "https://www.youtube.com/watch?v=TzJecWCbex0",
             "title": "Claude Tutorial", "role": "video_tutorial"},
        ]
        result = await enrich_wiki_topic("attention-mechanism", sources)

        assert result["saved"] == 1
        detail = result["details"][0]
        assert detail["via"] == "video-metadata"
        assert "TzJecWCbex0" in Path(detail["path"]).read_text()
