"""Stage 6: Resource recommendation tool — curated resources from wiki."""

import pytest

from app.agent.tool_handlers import _get_curated_resources


class TestGetCuratedResources:
    def test_empty_concepts_returns_error(self):
        result = _get_curated_resources([])
        assert result.get("error")
        assert result["resources"] == []

    def test_with_mini_wiki(self, patch_wiki_dir):
        result = _get_curated_resources(["attention mechanism", "self-attention"])

        assert "resources" in result
        resources = result["resources"]
        assert isinstance(resources, list)

        if resources:
            for r in resources:
                assert "type" in r
                assert r["type"] in ("video", "blog")
                if r["type"] == "video":
                    assert "youtube_id" in r
                else:
                    assert "url" in r

    def test_returns_topics_list(self, patch_wiki_dir):
        result = _get_curated_resources(["attention mechanism"])
        assert "topics" in result
        assert "attention-mechanism" in result["topics"]


@pytest.mark.wiki
class TestGetCuratedResourcesRealWiki:
    def test_real_wiki_has_attention_resources(self):
        """Uses real pedagogy-wiki on disk — skipped in CI."""
        result = _get_curated_resources(
            ["attention mechanism", "self-attention", "multi-head attention"]
        )
        assert len(result["resources"]) > 0
        types = {r["type"] for r in result["resources"]}
        assert "video" in types or "blog" in types
