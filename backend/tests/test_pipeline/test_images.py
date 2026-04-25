"""Image pipeline tests — extraction, filtering, annotation, context building, and serving."""

import json
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from app.services.wiki_images import (
    extract_images_from_html,
    heuristic_filter_images,
    load_images_json,
)
from app.services.course_generator import _build_image_context


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_HTML = """\
<html><body>
<h2>Attention Mechanism</h2>
<p>The encoder-decoder architecture passes hidden states through an alignment model.</p>
<figure>
  <img src="https://example.com/images/attention-diagram.png"
       alt="Bahdanau attention alignment" width="600" height="400">
  <figcaption>Attention alignment visualisation from Bahdanau et al.</figcaption>
</figure>
<p>Scores are computed between the decoder state and every encoder hidden state.</p>
<img src="https://example.com/images/softmax-weights.jpg"
     alt="Softmax weight distribution" width="500" height="300">
<p>The softmax produces a probability distribution over source positions.</p>
</body></html>
"""

JUNK_HTML = """\
<html><body>
<nav><img src="https://example.com/logo.png" alt="Logo" width="50" height="50"></nav>
<img src="https://example.com/favicon.ico" alt="">
<img src="https://example.com/tracking/pixel.gif" width="1" height="1">
<img src="https://example.com/avatar/user123.jpg" alt="User photo" width="64" height="64">
<figure>
  <img src="https://example.com/diagrams/transformer.png"
       alt="Transformer architecture" width="800" height="600">
  <figcaption>The Transformer model architecture</figcaption>
</figure>
</body></html>
"""


@pytest.fixture()
def images_wiki(tmp_path):
    """Create a mini wiki with images.json and concept map for testing."""
    topic = "attention-mechanism"
    images_dir = tmp_path / "resources" / "by-topic" / topic / "images"
    images_dir.mkdir(parents=True)

    # Concept map so load_wiki_context can resolve concepts to topics
    concept_map = (
        "# Concept -> Topic Map\n\n"
        "# attention-mechanism\n"
        "**Attention Mechanism** — 2 subtopics, 4 concepts\n\n"
        "## attention-core\n"
        "- bahdanau attention\n"
        "- alignment model\n\n"
        "## attention-variants\n"
        "- encoder-decoder\n"
        "- additive attention\n"
    )
    (tmp_path / "concept-map.md").write_text(concept_map)

    # Topic overview page (needed by load_wiki_context)
    topics_dir = tmp_path / "resources" / "by-topic"
    (topics_dir / f"{topic}.md").write_text(f"# {topic}\nOverview of attention mechanism.\n")

    entries = [
        {
            "file": "attention-diagram.png",
            "source_url": "https://example.com/images/attention-diagram.png",
            "description": "Bahdanau attention alignment diagram",
            "concepts": ["bahdanau attention", "alignment model", "encoder-decoder"],
            "when_to_show": "When explaining how Bahdanau attention computes alignment scores",
            "suggested_caption": "Attention alignment — Bahdanau et al. 2015",
            "keep": True,
        },
        {
            "file": "softmax-weights.jpg",
            "source_url": "https://example.com/images/softmax-weights.jpg",
            "description": "Softmax weight distribution over source positions",
            "concepts": ["softmax", "attention weights"],
            "when_to_show": "When discussing how attention weights are normalised",
            "suggested_caption": "Softmax attention weight distribution",
            "keep": True,
        },
        {
            "file": "transformer-arch.png",
            "source_url": "https://example.com/images/transformer-arch.png",
            "description": "Full Transformer model architecture",
            "concepts": ["multi-head attention", "self-attention", "transformer"],
            "when_to_show": "When introducing the full Transformer architecture",
            "suggested_caption": "Transformer architecture — Vaswani et al. 2017",
            "keep": True,
        },
    ]
    (images_dir / "images.json").write_text(json.dumps(entries))

    # Create dummy image files so file-existence checks pass
    for e in entries:
        (images_dir / e["file"]).write_bytes(b"\x89PNG\r\n")

    return {
        "wiki_dir": tmp_path,
        "topic": topic,
        "images_dir": images_dir,
        "entries": entries,
    }


# ---------------------------------------------------------------------------
# Tier 1: Unit tests — no LLM, no wiki
# ---------------------------------------------------------------------------

class TestExtractImagesFromHtml:
    def test_extracts_content_images(self):
        candidates = extract_images_from_html(SAMPLE_HTML, "https://example.com/post")
        assert len(candidates) == 2
        assert candidates[0]["src"] == "https://example.com/images/attention-diagram.png"
        assert candidates[1]["src"] == "https://example.com/images/softmax-weights.jpg"

    def test_captures_alt_text(self):
        candidates = extract_images_from_html(SAMPLE_HTML, "https://example.com/post")
        assert "Bahdanau" in candidates[0]["alt"]

    def test_captures_figcaption(self):
        candidates = extract_images_from_html(SAMPLE_HTML, "https://example.com/post")
        assert "alignment" in candidates[0]["caption"].lower()

    def test_captures_dimensions(self):
        candidates = extract_images_from_html(SAMPLE_HTML, "https://example.com/post")
        assert candidates[0]["width"] == 600
        assert candidates[0]["height"] == 400

    def test_captures_surrounding_text(self):
        candidates = extract_images_from_html(SAMPLE_HTML, "https://example.com/post")
        assert len(candidates[0]["surrounding_text"]) > 0

    def test_deduplicates_same_src(self):
        html = """<html><body>
        <img src="https://example.com/img.png">
        <img src="https://example.com/img.png">
        </body></html>"""
        candidates = extract_images_from_html(html, "https://example.com")
        assert len(candidates) == 1

    def test_skips_data_uris(self):
        html = '<html><body><img src="data:image/png;base64,abc123"></body></html>'
        candidates = extract_images_from_html(html, "https://example.com")
        assert len(candidates) == 0

    def test_resolves_relative_urls(self):
        html = '<html><body><img src="/images/fig1.png" alt="Figure 1"></body></html>'
        candidates = extract_images_from_html(html, "https://example.com/blog/post")
        assert candidates[0]["src"] == "https://example.com/images/fig1.png"


class TestHeuristicFilter:
    def test_removes_junk_images(self):
        candidates = extract_images_from_html(JUNK_HTML, "https://example.com/post")
        filtered = heuristic_filter_images(candidates)
        srcs = [c["src"] for c in filtered]
        assert not any("logo" in s for s in srcs)
        assert not any("favicon" in s for s in srcs)
        assert not any("pixel" in s for s in srcs)

    def test_keeps_content_images(self):
        candidates = extract_images_from_html(JUNK_HTML, "https://example.com/post")
        filtered = heuristic_filter_images(candidates)
        assert any("transformer.png" in c["src"] for c in filtered)

    def test_removes_tiny_images(self):
        candidates = [
            {"src": "https://example.com/small.png", "width": 30, "height": 30,
             "alt": "", "in_content_area": True, "caption": "", "title": ""},
        ]
        filtered = heuristic_filter_images(candidates)
        assert len(filtered) == 0

    def test_keeps_large_diagrams(self):
        candidates = [
            {"src": "https://example.com/diagram.png", "width": 800, "height": 600,
             "alt": "Architecture diagram", "in_content_area": True, "caption": "",
             "title": ""},
        ]
        filtered = heuristic_filter_images(candidates)
        assert len(filtered) == 1


class TestLoadImagesJson:
    def test_loads_existing_index(self, images_wiki, monkeypatch):
        import app.services.wiki_images as mod
        monkeypatch.setattr(mod, "_WIKI_DIR", images_wiki["wiki_dir"])

        entries = load_images_json(images_wiki["topic"])
        assert len(entries) == 3
        assert entries[0]["file"] == "attention-diagram.png"

    def test_returns_empty_for_missing_topic(self, images_wiki, monkeypatch):
        import app.services.wiki_images as mod
        monkeypatch.setattr(mod, "_WIKI_DIR", images_wiki["wiki_dir"])

        entries = load_images_json("nonexistent-topic")
        assert entries == []

    def test_returns_empty_for_invalid_json(self, images_wiki, monkeypatch):
        import app.services.wiki_images as mod
        monkeypatch.setattr(mod, "_WIKI_DIR", images_wiki["wiki_dir"])

        json_path = images_wiki["images_dir"] / "images.json"
        json_path.write_text("{invalid json")

        entries = load_images_json(images_wiki["topic"])
        assert entries == []


# ---------------------------------------------------------------------------
# Tier 1: _build_image_context unit tests
# ---------------------------------------------------------------------------

class TestBuildImageContext:
    def test_returns_empty_when_no_images(self):
        wiki_ctx = {"topics": ["attention"], "images": {}}
        result = _build_image_context(wiki_ctx, ["attention"])
        assert result == ""

    def test_includes_all_topic_images_even_without_concept_overlap(self):
        """Images from matched topics are always included (ranked lower)."""
        wiki_ctx = {
            "topics": ["attention"],
            "images": {
                "attention": [
                    {"file": "img.png", "concepts": ["transformer", "bert"],
                     "suggested_caption": "A diagram", "when_to_show": "Always"},
                ],
            },
        }
        result = _build_image_context(wiki_ctx, ["recurrent neural network"])
        assert "img.png" in result

    def test_includes_matching_images(self):
        wiki_ctx = {
            "topics": ["attention"],
            "images": {
                "attention": [
                    {"file": "attn.png", "concepts": ["attention", "alignment"],
                     "suggested_caption": "Attention diagram",
                     "when_to_show": "When explaining alignment"},
                ],
            },
        }
        result = _build_image_context(wiki_ctx, ["attention", "softmax"])
        assert "AVAILABLE EDUCATIONAL IMAGES" in result
        assert "attn.png" in result
        assert "/api/wiki-images/" in result

    def test_respects_max_images(self):
        images = [
            {"file": f"img{i}.png", "concepts": ["attention"],
             "suggested_caption": f"Image {i}", "when_to_show": "Always"}
            for i in range(20)
        ]
        wiki_ctx = {"topics": ["attention"], "images": {"attention": images}}
        result = _build_image_context(wiki_ctx, ["attention"], max_images=3)
        assert result.count("**img") == 3

    def test_ranks_by_concept_overlap(self):
        wiki_ctx = {
            "topics": ["attention"],
            "images": {
                "attention": [
                    {"file": "low.png", "concepts": ["softmax"],
                     "suggested_caption": "Low match", "when_to_show": "X"},
                    {"file": "high.png", "concepts": ["attention", "softmax", "alignment"],
                     "suggested_caption": "High match", "when_to_show": "Y"},
                ],
            },
        }
        result = _build_image_context(
            wiki_ctx, ["attention", "softmax", "alignment"], max_images=1,
        )
        assert "high.png" in result
        assert "low.png" not in result

    def test_includes_when_to_show(self):
        wiki_ctx = {
            "topics": ["attention"],
            "images": {
                "attention": [
                    {"file": "x.png", "concepts": ["attention"],
                     "suggested_caption": "Caption",
                     "when_to_show": "When teaching alignment scores"},
                ],
            },
        }
        result = _build_image_context(wiki_ctx, ["attention"])
        assert "When teaching alignment scores" in result

    def test_correct_path_format(self):
        wiki_ctx = {
            "topics": ["self-attention"],
            "images": {
                "self-attention": [
                    {"file": "self-attn.png", "concepts": ["self-attention"],
                     "suggested_caption": "Self-attention", "when_to_show": "Intro"},
                ],
            },
        }
        result = _build_image_context(wiki_ctx, ["self-attention"])
        assert "/api/wiki-images/self-attention/images/self-attn.png" in result

    def test_skips_entries_without_file(self):
        wiki_ctx = {
            "topics": ["attention"],
            "images": {
                "attention": [
                    {"concepts": ["attention"], "suggested_caption": "No file"},
                    {"file": "ok.png", "concepts": ["attention"],
                     "suggested_caption": "Has file", "when_to_show": "Always"},
                ],
            },
        }
        result = _build_image_context(wiki_ctx, ["attention"])
        assert "ok.png" in result
        assert "No file" not in result


# ---------------------------------------------------------------------------
# Tier 1: load_wiki_context returns images
# ---------------------------------------------------------------------------

class TestLoadWikiContextImages:
    def test_images_key_present(self, images_wiki, monkeypatch):
        import app.services.course_generator as gen_mod
        import app.services.wiki_images as img_mod

        monkeypatch.setattr(gen_mod, "_WIKI_DIR", images_wiki["wiki_dir"])
        monkeypatch.setattr(gen_mod, "_CONCEPT_MAP_PATH",
                            images_wiki["wiki_dir"] / "concept-map.md")
        monkeypatch.setattr(gen_mod, "_wiki_concept_map", None)
        monkeypatch.setattr(img_mod, "_WIKI_DIR", images_wiki["wiki_dir"])

        from app.services.course_generator import load_wiki_context
        ctx = load_wiki_context(
            ["attention"],
            topic_slugs={images_wiki["topic"]},
        )
        assert "images" in ctx
        assert images_wiki["topic"] in ctx["images"]
        assert len(ctx["images"][images_wiki["topic"]]) == 3


# ---------------------------------------------------------------------------
# Tier 2: Mocked LLM annotation tests
# ---------------------------------------------------------------------------

class TestAnnotateImages:
    @pytest.mark.asyncio
    async def test_annotate_batch_calls_llm(self, monkeypatch):
        from app.services.wiki_images import _annotate_batch

        llm_mock = AsyncMock(return_value={
            "images": [
                {"index": 1, "keep": True, "description": "Attention diagram",
                 "teaching_value": "Shows alignment", "concepts": ["attention"],
                 "when_to_show": "During intro", "suggested_caption": "Attention"},
                {"index": 2, "keep": False},
            ]
        })
        import app.services.course_enricher as enricher_mod
        monkeypatch.setattr(enricher_mod, "_call_llm_json", llm_mock)

        candidates = [
            {"src": "https://ex.com/a.png", "alt": "Attention", "caption": "",
             "section_heading": "Intro", "surrounding_text": "Attention is...",
             "width": 600, "height": 400},
            {"src": "https://ex.com/b.png", "alt": "Logo", "caption": "",
             "section_heading": "", "surrounding_text": "",
             "width": 50, "height": 50},
        ]

        results = await _annotate_batch("Test Page", "https://ex.com", "Author", candidates, 0)
        assert len(results) == 2
        assert results[0]["keep"] is True
        assert results[0]["concepts"] == ["attention"]
        assert results[1]["keep"] is False
        llm_mock.assert_called_once()

    @pytest.mark.asyncio
    async def test_annotate_images_batches(self, monkeypatch):
        from app.services.wiki_images import annotate_images

        call_count = 0

        async def mock_llm_json(prompt, **kwargs):
            nonlocal call_count
            call_count += 1
            return {"images": [{"index": 1, "keep": True, "description": "D",
                                "concepts": ["c"], "when_to_show": "W",
                                "suggested_caption": "S", "teaching_value": "T"}]}

        import app.services.course_enricher as enricher_mod
        monkeypatch.setattr(enricher_mod, "_call_llm_json", mock_llm_json)

        candidates = [
            {"src": f"https://ex.com/img{i}.png", "alt": f"Image {i}", "caption": "",
             "section_heading": "", "surrounding_text": "Context",
             "width": 600, "height": 400}
            for i in range(15)
        ]

        results = await annotate_images("Page", "https://ex.com", "Author", candidates)
        assert call_count == 2  # 15 images / batch_size 10 = 2 batches
        assert len(results) > 0


# ---------------------------------------------------------------------------
# Tier 2: Image context in prompt formatting
# ---------------------------------------------------------------------------

class TestImageContextInPrompts:
    def test_content_prompt_includes_image_context(self, images_wiki, monkeypatch):
        """Verify that CONTENT_FROM_WIKI_PROMPT.format() accepts image_context."""
        from app.services.course_generator import CONTENT_FROM_WIKI_PROMPT

        result = CONTENT_FROM_WIKI_PROMPT.format(
            title="Test Lesson",
            summary="A test",
            concepts="attention, softmax",
            source_count=2,
            wiki_source_context="Source text...",
            resource_page_excerpt="Resource...",
            image_context="AVAILABLE EDUCATIONAL IMAGES:\n1. **img.png**\n   Caption: \"Test\"",
            course_profile="",
        )
        assert "AVAILABLE EDUCATIONAL IMAGES" in result
        assert "img.png" in result

    def test_kb_prompt_includes_image_context(self):
        from app.services.course_generator import REFERENCE_KB_FROM_WIKI_PROMPT

        result = REFERENCE_KB_FROM_WIKI_PROMPT.format(
            title="Test",
            summary="A test",
            concepts="attention",
            source_count=1,
            wiki_source_context="Source...",
            resource_page_excerpt="Resource...",
            image_context="AVAILABLE EDUCATIONAL IMAGES:\n1. **diagram.png**",
            resource_summary="",
            course_profile="",
        )
        assert "AVAILABLE EDUCATIONAL IMAGES" in result
        assert "Visual Aids" in result

    def test_prompts_accept_empty_image_context(self):
        from app.services.course_generator import (
            CONTENT_FROM_WIKI_PROMPT,
            REFERENCE_KB_FROM_WIKI_PROMPT,
        )

        content_result = CONTENT_FROM_WIKI_PROMPT.format(
            title="Test", summary="S", concepts="c",
            source_count=0, wiki_source_context="",
            resource_page_excerpt="", image_context="",
            course_profile="",
        )
        assert isinstance(content_result, str)

        kb_result = REFERENCE_KB_FROM_WIKI_PROMPT.format(
            title="Test", summary="S", concepts="c",
            source_count=0, wiki_source_context="",
            resource_page_excerpt="", image_context="",
            resource_summary="", course_profile="",
        )
        assert isinstance(kb_result, str)


# ---------------------------------------------------------------------------
# Tier 3: Live LLM + wiki tests (opt-in)
# ---------------------------------------------------------------------------

@pytest.mark.llm
@pytest.mark.wiki
class TestImagePipelineLive:
    @pytest.mark.asyncio
    async def test_process_source_images_live(self):
        """End-to-end image processing on real HTML with real LLM annotation."""
        from app.services.wiki_images import process_source_images

        html = """<html><body>
        <h1>Understanding Attention</h1>
        <p>The attention mechanism allows models to focus on relevant parts of input.</p>
        <figure>
            <img src="https://jalammar.github.io/images/t/transformer_self-attention_visualization.png"
                 alt="Self-attention visualization" width="800" height="400">
            <figcaption>Self-attention visualization from Jay Alammar</figcaption>
        </figure>
        <p>Each word attends to every other word with learned weights.</p>
        </body></html>"""

        result = await process_source_images(
            topic_slug="test-live-images",
            page_title="Understanding Attention",
            page_url="https://jalammar.github.io/illustrated-transformer/",
            raw_html=html,
        )
        assert "extracted" in result
        assert "kept" in result
        assert isinstance(result.get("extracted"), int)


# ---------------------------------------------------------------------------
# Tutor image tool tests
# ---------------------------------------------------------------------------

class TestGetRelevantImages:
    def test_returns_images_for_matching_concepts(self, images_wiki, monkeypatch):
        import app.services.course_generator as gen_mod
        import app.services.wiki_images as img_mod

        monkeypatch.setattr(gen_mod, "_WIKI_DIR", images_wiki["wiki_dir"])
        monkeypatch.setattr(gen_mod, "_CONCEPT_MAP_PATH",
                            images_wiki["wiki_dir"] / "concept-map.md")
        monkeypatch.setattr(gen_mod, "_wiki_concept_map", None)
        monkeypatch.setattr(img_mod, "_WIKI_DIR", images_wiki["wiki_dir"])

        from app.agent.tool_handlers import _get_relevant_images

        result = _get_relevant_images(["bahdanau attention", "alignment model"])
        assert result["image_count"] > 0
        assert len(result["images"]) > 0

        img = result["images"][0]
        assert "path" in img
        assert img["path"].startswith("/api/wiki-images/")
        assert "caption" in img
        assert "description" in img
        assert "when_to_show" in img
        assert "concepts" in img
        assert "topic" in img

    def test_returns_empty_for_no_matches(self, images_wiki, monkeypatch):
        import app.services.course_generator as gen_mod
        import app.services.wiki_images as img_mod

        monkeypatch.setattr(gen_mod, "_WIKI_DIR", images_wiki["wiki_dir"])
        monkeypatch.setattr(gen_mod, "_CONCEPT_MAP_PATH",
                            images_wiki["wiki_dir"] / "concept-map.md")
        monkeypatch.setattr(gen_mod, "_wiki_concept_map", None)
        monkeypatch.setattr(img_mod, "_WIKI_DIR", images_wiki["wiki_dir"])

        from app.agent.tool_handlers import _get_relevant_images

        result = _get_relevant_images(["quantum computing", "superconductivity"])
        assert result["image_count"] == 0
        assert result["images"] == []

    def test_returns_error_for_empty_concepts(self):
        from app.agent.tool_handlers import _get_relevant_images

        result = _get_relevant_images([])
        assert "error" in result

    def test_limits_result_count(self, images_wiki, monkeypatch):
        import app.services.course_generator as gen_mod
        import app.services.wiki_images as img_mod

        # Add many images to the fixture
        many_entries = [
            {"file": f"img{i}.png", "source_url": f"https://ex.com/{i}.png",
             "description": f"Image {i}", "concepts": ["bahdanau attention"],
             "when_to_show": "Always", "suggested_caption": f"Caption {i}",
             "keep": True}
            for i in range(20)
        ]
        (images_wiki["images_dir"] / "images.json").write_text(json.dumps(many_entries))
        for e in many_entries:
            (images_wiki["images_dir"] / e["file"]).write_bytes(b"\x89PNG\r\n")

        monkeypatch.setattr(gen_mod, "_WIKI_DIR", images_wiki["wiki_dir"])
        monkeypatch.setattr(gen_mod, "_CONCEPT_MAP_PATH",
                            images_wiki["wiki_dir"] / "concept-map.md")
        monkeypatch.setattr(gen_mod, "_wiki_concept_map", None)
        monkeypatch.setattr(img_mod, "_WIKI_DIR", images_wiki["wiki_dir"])

        from app.agent.tool_handlers import _get_relevant_images

        result = _get_relevant_images(["bahdanau attention"])
        assert result["image_count"] <= 6

    def test_tool_definition_exists(self):
        from app.agent.tools import TUTOR_TOOLS

        names = [t["function"]["name"] for t in TUTOR_TOOLS]
        assert "get_relevant_images" in names

        tool = next(t for t in TUTOR_TOOLS if t["function"]["name"] == "get_relevant_images")
        params = tool["function"]["parameters"]
        assert "concepts" in params["properties"]
        assert params["required"] == ["concepts"]
