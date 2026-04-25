"""Shared fixtures and helpers for pipeline tests."""

import json
import shutil
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

_FIXTURES = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict:
    """Load a JSON fixture from the fixtures directory."""
    return json.loads((_FIXTURES / name).read_text())


def load_llm_response(name: str) -> dict:
    """Load a canned LLM response from fixtures/llm_responses/."""
    return load_fixture(f"llm_responses/{name}")


async def collect_sse(async_gen) -> list[dict]:
    """Consume an SSE async generator and return parsed event dicts."""
    events = []
    async for raw in async_gen:
        raw = raw.strip()
        if raw.startswith("data: "):
            try:
                events.append(json.loads(raw[6:]))
            except json.JSONDecodeError:
                pass
    return events


@pytest.fixture()
def mini_wiki(tmp_path):
    """Create a minimal wiki tree in tmp_path and monkeypatch module paths.

    Yields a dict with the wiki root path and topic slugs available.
    """
    wiki_dir = tmp_path / "content" / "pedagogy-wiki"
    topics_dir = wiki_dir / "resources" / "by-topic"
    topics_dir.mkdir(parents=True)

    # Copy concept map
    shutil.copy(_FIXTURES / "concept_map.md", wiki_dir / "concept-map.md")

    # Copy topic pages
    for page in ("attention-mechanism.md", "self-attention.md"):
        shutil.copy(_FIXTURES / page, topics_dir / page)

    # Copy source subdirectories
    for slug in ("attention-mechanism", "self-attention"):
        src_fixture = _FIXTURES / "sources" / slug
        if src_fixture.is_dir():
            dest = topics_dir / slug
            shutil.copytree(src_fixture, dest)

    return {
        "wiki_dir": wiki_dir,
        "topics_dir": topics_dir,
        "slugs": ["attention-mechanism", "self-attention"],
    }


@pytest.fixture()
def patch_wiki_dir(mini_wiki, monkeypatch):
    """Monkeypatch _WIKI_DIR and _CONCEPT_MAP_PATH in generator and downloader modules."""
    wiki_dir = mini_wiki["wiki_dir"]

    import app.services.course_generator as gen_mod
    import app.services.wiki_downloader as dl_mod

    monkeypatch.setattr(gen_mod, "_WIKI_DIR", wiki_dir)
    monkeypatch.setattr(gen_mod, "_CONCEPT_MAP_PATH", wiki_dir / "concept-map.md")
    # Reset the cached concept map so _load_concept_map re-reads from patched path
    monkeypatch.setattr(gen_mod, "_wiki_concept_map", None)

    monkeypatch.setattr(dl_mod, "_WIKI_DIR", wiki_dir)
    monkeypatch.setattr(dl_mod, "_CONCEPT_MAP_PATH", wiki_dir / "concept-map.md")
    monkeypatch.setattr(dl_mod, "_PENDING_DIR", wiki_dir / ".pending")

    return mini_wiki


@pytest.fixture()
def mock_generator_llm(monkeypatch):
    """Patch _call_llm_json and _call_llm in course_generator with controllable mocks.

    Returns a dict of the mocks so tests can set return values.
    """
    import app.services.course_generator as mod

    llm_json_mock = AsyncMock(name="_call_llm_json")
    llm_mock = AsyncMock(name="_call_llm")

    monkeypatch.setattr(mod, "_call_llm_json", llm_json_mock)
    monkeypatch.setattr(mod, "_call_llm", llm_mock)

    return {"_call_llm_json": llm_json_mock, "_call_llm": llm_mock}


@pytest.fixture()
def mock_enricher_llm(monkeypatch):
    """Patch _call_llm_json and _call_llm in course_enricher."""
    import app.services.course_enricher as mod

    llm_json_mock = AsyncMock(name="_call_llm_json")
    llm_mock = AsyncMock(name="_call_llm")

    monkeypatch.setattr(mod, "_call_llm_json", llm_json_mock)
    monkeypatch.setattr(mod, "_call_llm", llm_mock)

    return {"_call_llm_json": llm_json_mock, "_call_llm": llm_mock}


@pytest.fixture()
def mock_search(monkeypatch):
    """Patch _search in course_enricher."""
    import app.services.course_enricher as mod

    search_mock = AsyncMock(name="_search")
    monkeypatch.setattr(mod, "_search", search_mock)
    return search_mock


@pytest.fixture()
def mock_downloader_llm(monkeypatch):
    """Patch the LLM used by wiki_downloader (locally imported from course_enricher)."""
    import app.services.course_enricher as enricher_mod

    llm_json_mock = AsyncMock(name="_call_llm_json")
    monkeypatch.setattr(enricher_mod, "_call_llm_json", llm_json_mock)
    return llm_json_mock


@pytest.fixture()
def sample_outline() -> dict:
    return load_fixture("sample_outline.json")


@pytest.fixture()
def sample_assessment() -> dict:
    data = load_fixture("sample_assessment.json")
    # Restore sets that were serialized as lists
    for bucket in ("fully_covered", "needs_research", "no_match"):
        for entry in data.get(bucket, []):
            if "resolved_topics" in entry:
                entry["resolved_topics"] = set(entry["resolved_topics"])
    return data
