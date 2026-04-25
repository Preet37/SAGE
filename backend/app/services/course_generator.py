"""
Course Creator — Phase 1 & 2 service.

Handles outline generation, per-lesson content generation,
terminology cleanup, and quality gate evaluation.
"""

import asyncio
import json
import logging
import re
from typing import AsyncGenerator

logger = logging.getLogger(__name__)

import httpx

from ..config import get_settings

# ---------------------------------------------------------------------------
# LLM helpers
# ---------------------------------------------------------------------------

_llm_semaphore = asyncio.Semaphore(5)


async def _call_llm(
    prompt: str,
    *,
    max_tokens: int = 4096,
    temperature: float = 0.2,
    model: str | None = None,
) -> str:
    settings = get_settings()
    chosen_model = model or settings.llm_model
    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": chosen_model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    try:
        async with _llm_semaphore:
            async with httpx.AsyncClient(timeout=300.0) as client:
                resp = await client.post(
                    f"{settings.llm_base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                resp.raise_for_status()
                data = resp.json()
    except (httpx.HTTPStatusError, httpx.TimeoutException) as e:
        fallback = settings.fallback_llm_model
        if fallback and chosen_model != fallback and model is None:
            logger.warning(
                "Primary model %s failed (%s), retrying with fallback %s",
                chosen_model, type(e).__name__, fallback,
            )
            payload["model"] = fallback
            async with _llm_semaphore:
                async with httpx.AsyncClient(timeout=300.0) as client:
                    resp = await client.post(
                        f"{settings.llm_base_url}/chat/completions",
                        headers=headers,
                        json=payload,
                    )
                    resp.raise_for_status()
                    data = resp.json()
        else:
            raise

    raw = data["choices"][0]["message"]["content"].strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()
    return raw


async def _call_llm_json(prompt: str, **kwargs) -> dict:
    raw = await _call_llm(prompt, **kwargs)
    return json.loads(raw)


async def _stream_llm(
    prompt: str,
    *,
    max_tokens: int = 4096,
    temperature: float = 0.2,
    model: str | None = None,
) -> AsyncGenerator[str, None]:
    """Stream LLM response tokens. Yields text chunks."""
    settings = get_settings()
    chosen_model = model or settings.llm_model
    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": chosen_model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": True,
    }
    async with _llm_semaphore:
        async with httpx.AsyncClient(timeout=300.0) as client:
            async with client.stream(
                "POST",
                f"{settings.llm_base_url}/chat/completions",
                headers=headers,
                json=payload,
            ) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    data_str = line[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                        delta = chunk["choices"][0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            yield content
                    except (json.JSONDecodeError, KeyError, IndexError):
                        continue


def _strip_md_fences(text: str) -> str:
    """Remove leading ```json / ``` and trailing ``` from LLM output."""
    s = text.strip()
    if s.startswith("```"):
        s = s.split("\n", 1)[1] if "\n" in s else s[3:]
        if s.endswith("```"):
            s = s[:-3]
        s = s.strip()
    return s


def _extract_partial_outline(raw_text: str) -> tuple[str | None, list[dict]]:
    """Extract course title and completed module objects from partial JSON.

    Uses bracket-counting with string-literal awareness so that braces
    inside JSON string values are not miscounted.
    """
    text = raw_text.lstrip()
    if text.startswith("```"):
        nl = text.find("\n")
        text = text[nl + 1:] if nl >= 0 else text[3:]

    title = None
    modules_pos = text.find('"modules"')
    search_region = text[:modules_pos] if modules_pos > 0 else text
    title_match = re.search(r'"title"\s*:\s*"((?:[^"\\]|\\.)*)"', search_region)
    if title_match:
        title = title_match.group(1)

    if modules_pos < 0:
        return title, []

    bracket_start = text.find("[", modules_pos)
    if bracket_start < 0:
        return title, []

    modules: list[dict] = []
    i = bracket_start + 1

    while i < len(text):
        while i < len(text) and text[i] in " \t\n\r,":
            i += 1
        if i >= len(text) or text[i] != "{":
            break

        depth = 0
        obj_start = i
        in_string = False
        escape_next = False

        while i < len(text):
            c = text[i]
            if escape_next:
                escape_next = False
                i += 1
                continue
            if c == "\\" and in_string:
                escape_next = True
                i += 1
                continue
            if c == '"':
                in_string = not in_string
            elif not in_string:
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        try:
                            module = json.loads(text[obj_start : i + 1])
                            modules.append(module)
                        except json.JSONDecodeError:
                            pass
                        i += 1
                        break
            i += 1
        else:
            break

    return title, modules


# ---------------------------------------------------------------------------
# Outline generation
# ---------------------------------------------------------------------------

OUTLINE_FROM_PROMPT = """\
You are an expert course designer. Given a topic description, create a \
structured course outline.

Produce a JSON object with:
- "title": course title (if the user hasn't specified one clearly, create one)
- "description": 1-2 sentence course description
- "level": "beginner", "intermediate", or "advanced"
- "course_profile": object describing who this course is for and how to \
  source material (infer entirely from the topic description):
  - "audience": free-text description of who this course is for \
    (e.g. "ML engineers familiar with PyTorch", "non-technical managers")
  - "tone": one of "practical-hands-on", "technical-precise", or \
    "conceptual-theoretical"
  - "source_types": array of preferred source types, ordered by priority. \
    Choose from: "official-docs", "tutorials", "videos", "blog-posts", \
    "papers", "api-references", "benchmarks", "code-examples"
  - "deprioritize": array of source types to avoid or rank lower. \
    Same options as source_types. Empty array if none.
  - "vendor": the primary product vendor if the course is about a \
    specific product/tool (e.g. "Anthropic", "OpenAI", "Google"), \
    or null for general technical topics
- "modules": array of modules, each with:
  - "title": module title
  - "order_index": integer starting at 0
  - "lessons": array of lessons, each with:
    - "title": lesson title
    - "slug": URL-friendly slug (lowercase, hyphens)
    - "order_index": integer starting at 0
    - "summary": 1-2 sentence description of what this lesson covers
    - "concepts": array of 4-8 key technical concepts (lowercase)

Design 3-6 modules with 3-5 lessons each. Return ONLY valid JSON.

TOPIC:
{source_text}
"""

OUTLINE_FROM_TRANSCRIPT = """\
You are an expert course designer. Given a transcript from a training video \
or series, analyze its content and create a structured course outline.

Identify the logical sections and topics covered, then organize them into \
a coherent course structure.

Produce a JSON object with:
- "title": course title
- "description": 1-2 sentence course description
- "level": "beginner", "intermediate", or "advanced"
- "course_profile": object describing who this course is for and how to \
  source material (infer from the transcript content and style):
  - "audience": free-text description of who this course is for \
    (e.g. "ML engineers familiar with PyTorch", "non-technical managers")
  - "tone": one of "practical-hands-on", "technical-precise", or \
    "conceptual-theoretical"
  - "source_types": array of preferred source types, ordered by priority. \
    Choose from: "official-docs", "tutorials", "videos", "blog-posts", \
    "papers", "api-references", "benchmarks", "code-examples"
  - "deprioritize": array of source types to avoid or rank lower. \
    Same options as source_types. Empty array if none.
  - "vendor": the primary product vendor if the course is about a \
    specific product/tool (e.g. "Anthropic", "OpenAI", "Google"), \
    or null for general technical topics
- "modules": array of modules, each with:
  - "title": module title
  - "order_index": integer starting at 0
  - "lessons": array of lessons, each with:
    - "title": lesson title
    - "slug": URL-friendly slug (lowercase, hyphens)
    - "order_index": integer starting at 0
    - "summary": 1-2 sentence description of what this lesson covers
    - "concepts": array of 4-8 key technical concepts (lowercase)

Design 3-6 modules with 3-5 lessons each. Return ONLY valid JSON.

TRANSCRIPT:
{source_text}
"""


def _format_course_profile(profile: dict | None) -> str:
    """Format a course_profile dict as a text block for injection into prompts."""
    if not profile:
        return ""
    lines = ["COURSE PROFILE:"]
    if profile.get("audience"):
        lines.append(f"- Audience: {profile['audience']}")
    if profile.get("tone"):
        lines.append(f"- Tone: {profile['tone']}")
    if profile.get("source_types"):
        lines.append(f"- Preferred sources: {', '.join(profile['source_types'])}")
    if profile.get("deprioritize"):
        lines.append(f"- Deprioritize: {', '.join(profile['deprioritize'])}")
    if profile.get("vendor"):
        lines.append(f"- Vendor/Product: {profile['vendor']}")
    return "\n".join(lines)


async def generate_outline(
    source_text: str,
    source_type: str,
) -> AsyncGenerator[str, None]:
    """Generate a course outline from a prompt or transcript. Yields SSE events."""
    yield _sse({"type": "status", "message": "Generating course outline..."})

    if source_type == "transcript":
        prompt = OUTLINE_FROM_TRANSCRIPT.format(source_text=source_text)
    else:
        prompt = OUTLINE_FROM_PROMPT.format(source_text=source_text)

    try:
        accumulated = ""
        prev_module_count = 0
        title_sent = False

        async for chunk in _stream_llm(prompt, max_tokens=8096):
            accumulated += chunk

            title, modules = _extract_partial_outline(accumulated)

            if title and not title_sent:
                yield _sse({"type": "partial_outline", "data": {"title": title, "modules": []}})
                title_sent = True

            if len(modules) > prev_module_count:
                prev_module_count = len(modules)
                yield _sse({
                    "type": "partial_outline",
                    "data": {"title": title or "", "modules": modules},
                })
                yield _sse({
                    "type": "status",
                    "message": f"Generated module {len(modules)}: {modules[-1].get('title', '')}",
                })

        raw = _strip_md_fences(accumulated)
        outline = json.loads(raw)
        yield _sse({"type": "outline", "data": outline})
        yield _sse({"type": "done"})
    except Exception as e:
        logger.exception("Outline generation failed")
        yield _sse({"type": "error", "message": str(e) or f"{type(e).__name__}: (no detail)"})


# ---------------------------------------------------------------------------
# Wiki loader — maps lesson concepts to wiki resources + downloaded content
# ---------------------------------------------------------------------------

from pathlib import Path as _Path

from ..config import WIKI_DIR as _WIKI_DIR  # noqa: E402
_CONCEPT_MAP_PATH = _WIKI_DIR / "concept-map.md"

_wiki_concept_map: dict[str, str] | None = None


def _load_concept_map() -> dict[str, str]:
    """Parse concept-map.md → {concept: topic_slug}. Cached after first call."""
    global _wiki_concept_map
    if _wiki_concept_map is not None:
        return _wiki_concept_map

    mapping: dict[str, str] = {}
    if not _CONCEPT_MAP_PATH.exists():
        _wiki_concept_map = mapping
        return mapping

    current_topic = ""
    for line in _CONCEPT_MAP_PATH.read_text().splitlines():
        if line.startswith("# ") and not line.startswith("# Concept"):
            current_topic = line[2:].strip()
        elif line.startswith("- ") and current_topic:
            concept = line[2:].strip().lower()
            mapping[concept] = current_topic

    _wiki_concept_map = mapping
    return mapping


_CONCEPT_MAPPER_PROMPT = """\
You are a knowledge-base librarian. Given a lesson's metadata and a \
concept-map of available wiki topics, determine which wiki topics are \
relevant to this lesson's concepts.

LESSON CONTEXT:
- Title: {lesson_title}
- Summary: {lesson_summary}
- Concepts: {concepts}

AVAILABLE WIKI TOPICS AND THEIR CONCEPTS:
{concept_map_text}

TASK: For each lesson concept, decide which wiki topic slug(s) it \
genuinely belongs to based on SEMANTIC meaning, not surface word overlap.

IMPORTANT:
- "alignment model" in an attention lesson means Bahdanau sequence \
  alignment, NOT RLHF alignment.
- "sliding window" in an attention lesson means sliding-window attention, \
  NOT context-window management.
- Only match to topics where the wiki content would genuinely help \
  explain this concept in the context of this lesson.
- If a concept has NO good match, mark it as unmapped — do NOT force a \
  match to a loosely related topic.

Return a JSON object:
{{
  "mappings": {{
    "<concept>": ["<topic_slug>", ...] or []
  }},
  "unmapped": ["<concept>", ...]
}}

Return ONLY valid JSON.
"""


async def resolve_topics_llm(
    concepts: list[str],
    *,
    lesson_title: str = "",
    lesson_summary: str = "",
) -> dict:
    """Resolve concepts to wiki topic slugs using an LLM.

    Returns:
        {
            "topic_slugs": set of matched topic slugs,
            "unmapped": list of concepts with no wiki match,
            "mappings": {concept: [topic_slugs]} for diagnostics,
        }
    """
    if not concepts:
        return {"topic_slugs": set(), "unmapped": [], "mappings": {}}

    concept_map_text = ""
    if _CONCEPT_MAP_PATH.exists():
        concept_map_text = _CONCEPT_MAP_PATH.read_text()

    if not concept_map_text.strip():
        return {"topic_slugs": set(), "unmapped": list(concepts), "mappings": {}}

    prompt = _CONCEPT_MAPPER_PROMPT.format(
        lesson_title=lesson_title,
        lesson_summary=lesson_summary,
        concepts=", ".join(concepts),
        concept_map_text=concept_map_text,
    )

    try:
        result = await _call_llm_json(prompt, max_tokens=2048, temperature=0.0)
    except Exception as e:
        logger.warning("LLM concept mapper failed, falling back to exact match: %s", e)
        return resolve_topics_exact(concepts)

    mappings = result.get("mappings", {})
    unmapped = result.get("unmapped", [])

    topic_slugs: set[str] = set()
    for concept, slugs in mappings.items():
        if isinstance(slugs, list):
            topic_slugs.update(slugs)

    return {"topic_slugs": topic_slugs, "unmapped": unmapped, "mappings": mappings}


def resolve_topics_exact(concepts: list[str]) -> dict:
    """Resolve concepts to wiki topic slugs using the concept-map.

    Used by sync callers (tool handlers, tutor context builder).
    """
    concept_map = _load_concept_map()
    topic_slugs: set[str] = set()
    unmapped: list[str] = []
    mappings: dict[str, list[str]] = {}

    for raw_concept in concepts:
        concept = raw_concept.lower().strip()
        slug = concept_map.get(concept)
        if slug:
            topic_slugs.add(slug)
            mappings[concept] = [slug]
        else:
            unmapped.append(raw_concept)
            mappings[concept] = []

    return {"topic_slugs": topic_slugs, "unmapped": unmapped, "mappings": mappings}


def load_wiki_context(
    concepts: list[str],
    *,
    topic_slugs: set[str] | None = None,
    track: str = "pedagogy",
) -> dict:
    """Load wiki context for a set of lesson concepts.

    If ``topic_slugs`` is provided, uses them directly (from a prior
    ``resolve_topics_llm`` call). Otherwise falls back to exact
    concept-map matching for synchronous callers.

    When ``track="reference"``, reads source files from the
    ``reference/`` subdirectory under each topic folder.  The topic
    overview page (``{slug}.md``) is always read from the parent
    directory since it's shared context.

    Returns:
        {
            "topics": [topic_slug, ...],
            "resource_pages": {topic_slug: markdown_content, ...},
            "source_content": {topic_slug: [{"file": name, "content": text}, ...]},
            "youtube_ids": {topic_slug: [(yt_id, title_line), ...]},
            "recommended_reading": {topic_slug: [(title, url), ...]},
        }
    """
    topics_dir = _WIKI_DIR / "resources" / "by-topic"
    if topic_slugs is None:
        resolved = resolve_topics_exact(concepts)
        topic_slugs = resolved["topic_slugs"]

    resource_pages: dict[str, str] = {}
    source_content: dict[str, list[dict]] = {}
    youtube_ids: dict[str, list[tuple[str, str]]] = {}
    recommended_reading: dict[str, list[tuple[str, str]]] = {}

    yt_re = re.compile(r'youtube_id[=:\s]+([A-Za-z0-9_-]{11})')
    url_re = re.compile(r'(?:url|URL)[=:\s]+(https?://[^\s\]\)>]+)', re.IGNORECASE)

    seen_files: set[str] = set()
    seen_yt_ids: set[str] = set()

    for slug in sorted(topic_slugs):
        # Topic overview page is always in the parent directory
        page_path = topics_dir / f"{slug}.md"
        if not page_path.exists():
            continue

        page_text = page_path.read_text()
        resource_pages[slug] = page_text

        for m in yt_re.finditer(page_text):
            yt_id = m.group(1)
            if yt_id in seen_yt_ids:
                continue
            seen_yt_ids.add(yt_id)
            ctx_start = max(0, m.start() - 200)
            ctx = page_text[ctx_start:m.start()]
            title_line = ""
            for line in ctx.splitlines():
                if line.strip().startswith("- **"):
                    title_line = line.strip()
            youtube_ids.setdefault(slug, []).append((yt_id, title_line))

        for m in url_re.finditer(page_text):
            url = m.group(1).rstrip(".,;:")
            ctx_start = max(0, m.start() - 200)
            ctx = page_text[ctx_start:m.start()]
            title_line = ""
            for line in ctx.splitlines():
                if line.strip().startswith("- **"):
                    title_line = line.strip()
            recommended_reading.setdefault(slug, []).append(
                (title_line, url)
            )

        # Source files: pedagogy reads from slug/, reference from slug/reference/
        _AUDIT_FILES = {"curation-report.md", "proposals.json", "ramps.json"}
        if track == "reference":
            dl_dir = topics_dir / slug / "reference"
        else:
            dl_dir = topics_dir / slug
        if dl_dir.is_dir():
            # For reference track: prefer .card.md over full .md sources.
            # Build a set of stems that have cards so we can skip the raw file.
            card_stems: set[str] = set()
            if track == "reference":
                for f in dl_dir.iterdir():
                    if f.name.endswith(".card.md"):
                        card_stems.add(f.name.removesuffix(".card.md"))

            for src_file in sorted(dl_dir.iterdir()):
                if src_file.suffix not in (".md", ".txt"):
                    continue
                if src_file.name in _AUDIT_FILES:
                    continue
                # Skip raw source when a card exists for it
                if track == "reference" and not src_file.name.endswith(".card.md"):
                    stem = src_file.stem
                    if stem in card_stems:
                        continue
                if src_file.stat().st_size <= 200:
                    continue
                if src_file.name in seen_files:
                    continue
                seen_files.add(src_file.name)
                text = src_file.read_text()
                source_content.setdefault(slug, []).append({
                    "file": src_file.name,
                    "content": text,
                })
                # Extract youtube_id from video stub headers
                for header_line in text.split("\n")[:10]:
                    if header_line.startswith("# youtube_id:"):
                        stub_yt_id = header_line.split(":", 1)[1].strip()
                        if stub_yt_id and stub_yt_id not in seen_yt_ids:
                            seen_yt_ids.add(stub_yt_id)
                            stub_title = ""
                            for tl in text.split("\n")[:10]:
                                if tl.startswith("# Title:"):
                                    stub_title = tl.split(":", 1)[1].strip()
                                    break
                            youtube_ids.setdefault(slug, []).append(
                                (stub_yt_id, f"- **{stub_title}**" if stub_title else "")
                            )
                        break

    # Load image metadata from images.json per topic
    from .wiki_images import load_images_json

    images: dict[str, list[dict]] = {}
    for slug in sorted(topic_slugs):
        topic_images = load_images_json(slug)
        if topic_images:
            images[slug] = topic_images

    return {
        "topics": sorted(topic_slugs),
        "resource_pages": resource_pages,
        "source_content": source_content,
        "youtube_ids": youtube_ids,
        "recommended_reading": recommended_reading,
        "images": images,
    }


_CONCEPT_COVERAGE_PROMPT = """\
You are auditing whether a wiki knowledge base has sufficient content \
to teach a specific lesson. You must be STRICT — the default verdict \
is "needs_research". Only mark a concept as "covered" if the source \
material substantively explains it (definitions, mechanics, examples), \
not merely mentions it in passing.

LESSON: {lesson_title}
SUMMARY: {lesson_summary}

CONCEPTS TO CHECK:
{concepts_list}

AVAILABLE WIKI CONTENT (first ~2000 chars per source):
{wiki_content_summary}

For EACH concept, assess:
- "covered": the wiki content substantively explains this concept with \
  enough depth for a tutor to teach from it
- "thin": the concept is mentioned but not explained in sufficient depth
- "missing": the concept is not present in the wiki content at all

Return a JSON object:
{{
  "concept_verdicts": {{
    "<concept>": {{"verdict": "covered"|"thin"|"missing", "reason": "brief explanation"}}
  }},
  "lesson_verdict": "fully_covered"|"needs_research",
  "research_topics": ["specific topics to research for thin/missing concepts"]
}}

IMPORTANT: The lesson is "fully_covered" ONLY if EVERY concept is "covered". \
If even one concept is "thin" or "missing", the lesson "needs_research".

Return ONLY valid JSON.
"""


async def _assess_one_lesson(lesson: dict) -> dict:
    """Assess a single lesson's wiki coverage. Returns a result dict with ``_verdict``.

    Shared implementation used by both ``assess_wiki_coverage`` (batch)
    and ``assess_wiki_coverage_stream`` (SSE).
    """
    title = lesson.get("title", "Untitled")
    concepts = lesson.get("concepts", [])
    summary = lesson.get("summary", "")

    resolved = await resolve_topics_llm(
        concepts, lesson_title=title, lesson_summary=summary,
    )
    topic_slugs = resolved["topic_slugs"]
    unmapped_from_map = resolved["unmapped"]

    if not topic_slugs:
        proposed = re.sub(r'[^a-z0-9]+', '-', title.lower().strip()).strip('-')[:60]
        return {
            "_verdict": "no_match",
            "lesson": lesson,
            "unmapped": unmapped_from_map or concepts,
            "proposed_topic": proposed,
        }

    wiki_ctx = load_wiki_context(concepts, topic_slugs=topic_slugs)

    source_files = []
    for topic_slug in wiki_ctx.get("topics", []):
        for src in wiki_ctx.get("source_content", {}).get(topic_slug, []):
            source_files.append(src["file"])

    content_summary_parts = []
    char_budget = 16000
    total_chars = 0
    for topic_slug in wiki_ctx.get("topics", []):
        for src in wiki_ctx.get("source_content", {}).get(topic_slug, []):
            available = char_budget - total_chars
            if available <= 200:
                break
            header = src["content"].split("\n", 3)
            source_label = next(
                (l for l in header if l.startswith("# Source:") or l.startswith("# Transcript:")),
                src["file"],
            )
            snippet = src["content"][:min(1500, available)]
            content_summary_parts.append(f"--- {source_label} ---\n{snippet}")
            total_chars += len(snippet)
        if total_chars >= char_budget:
            break

    wiki_content_summary = "\n\n".join(content_summary_parts) if content_summary_parts else "(no content)"
    concepts_list = "\n".join(f"- {c}" for c in concepts)

    prompt = _CONCEPT_COVERAGE_PROMPT.format(
        lesson_title=title,
        lesson_summary=summary,
        concepts_list=concepts_list,
        wiki_content_summary=wiki_content_summary,
    )

    try:
        result = await _call_llm_json(prompt, max_tokens=2048, temperature=0.0)
    except Exception as e:
        logger.warning("Coverage assessment LLM failed for %r: %s", title, e)
        return {
            "_verdict": "needs_research",
            "lesson": lesson,
            "topics": list(topic_slugs),
            "resolved_topics": topic_slugs,
            "concept_verdicts": {},
            "research_topics": concepts,
            "source_count": len(source_files),
            "sources": source_files,
            "error": str(e),
        }

    verdicts = result.get("concept_verdicts", {})
    lesson_verdict = result.get("lesson_verdict", "needs_research")
    research_topics = result.get("research_topics", [])

    entry = {
        "lesson": lesson,
        "topics": list(topic_slugs),
        "resolved_topics": topic_slugs,
        "concept_verdicts": verdicts,
        "source_count": len(source_files),
        "sources": source_files,
    }

    if lesson_verdict == "fully_covered":
        entry["_verdict"] = "fully_covered"
    else:
        entry["_verdict"] = "needs_research"
        entry["research_topics"] = research_topics

    return entry


def _classify_assessment(result: dict) -> str:
    """Pop ``_verdict`` from an assessment result and return the verdict string."""
    return result.pop("_verdict")


async def assess_wiki_coverage(
    lessons: list[dict],
) -> dict:
    """Concept-level wiki coverage assessment for each lesson.

    For each lesson, uses LLM to check whether the wiki's downloaded
    content substantively covers each individual concept — not just
    whether the lesson maps to a topic with general content.

    Returns:
        {
            "fully_covered": [{lesson, topics, resolved_topics, concept_verdicts}, ...],
            "needs_research": [{lesson, topics, resolved_topics, concept_verdicts, research_topics}, ...],
            "no_match": [{lesson, unmapped, proposed_topic}, ...],
        }

    ``resolved_topics`` is the set of wiki topic slugs from LLM resolution,
    cached so downstream stages can call ``load_wiki_context(concepts,
    topic_slugs=entry["resolved_topics"])`` without re-resolving.
    """
    fully_covered: list[dict] = []
    needs_research: list[dict] = []
    no_match: list[dict] = []

    futures = [asyncio.ensure_future(_assess_one_lesson(les)) for les in lessons]
    results = await asyncio.gather(*futures)

    for result in results:
        verdict = _classify_assessment(result)
        if verdict == "no_match":
            no_match.append(result)
        elif verdict == "fully_covered":
            fully_covered.append(result)
        else:
            needs_research.append(result)

    return {
        "fully_covered": fully_covered,
        "needs_research": needs_research,
        "no_match": no_match,
    }


async def assess_wiki_coverage_stream(
    lessons: list[dict],
) -> AsyncGenerator[str, None]:
    """Streaming version of ``assess_wiki_coverage`` — yields SSE events
    as each lesson is assessed (via ``as_completed``).
    """
    total = len(lessons)
    yield _sse({"type": "status", "message": f"Assessing {total} lessons..."})

    fully_covered: list[dict] = []
    needs_research: list[dict] = []
    no_match: list[dict] = []
    completed = 0

    futures = [asyncio.ensure_future(_assess_one_lesson(les)) for les in lessons]

    for coro in asyncio.as_completed(futures):
        result = await coro
        completed += 1
        verdict = _classify_assessment(result)
        lesson = result["lesson"]

        if verdict == "no_match":
            no_match.append(result)
        elif verdict == "fully_covered":
            fully_covered.append(result)
        else:
            needs_research.append(result)

        yield _sse({
            "type": "lesson_assessed",
            "slug": lesson.get("slug", ""),
            "title": lesson.get("title", "Untitled"),
            "verdict": verdict,
            "topics": result.get("topics", []),
            "concept_verdicts": result.get("concept_verdicts", {}),
            "source_count": result.get("source_count", 0),
            "sources": result.get("sources", []),
            "research_topics": result.get("research_topics", []),
            "unmapped": result.get("unmapped", []),
            "index": completed,
            "total": total,
        })

    yield _sse({
        "type": "assessment_complete",
        "summary": {
            "fully_covered": len(fully_covered),
            "needs_research": len(needs_research),
            "no_match": len(no_match),
        },
    })
    yield _sse({"type": "done"})


async def _collect_sse(async_gen) -> list[dict]:
    """Collect SSE events from an async generator into a list of dicts."""
    events = []
    async for raw in async_gen:
        raw = raw.strip()
        if raw.startswith("data: "):
            try:
                events.append(json.loads(raw[6:]))
            except json.JSONDecodeError:
                pass
    return events


async def ensure_wiki_coverage(
    lessons: list[dict],
    course_description: str = "",
    *,
    enrich: bool = True,
    sample: int | None = None,
    course_profile: dict | None = None,
) -> dict:
    """Assess wiki coverage and optionally enrich gaps.

    Runs the assess-enrich pipeline (stages 3-4 of the course creation
    pipeline) as a reusable function:

    1. ``assess_wiki_coverage`` — LLM-based concept-level check
    2. ``bootstrap_new_wiki_topic`` — for lessons with no wiki match
    3. Search + curate + download — for lessons needing research
    4. Reference track enrichment — precision sources for KB generation

    Returns the assessment dict (same shape as ``assess_wiki_coverage``),
    with ``resolved_topics`` per entry that callers pass to
    ``load_wiki_context``.
    """
    from .wiki_downloader import (
        bootstrap_new_wiki_topic,
        curate_best_sources,
        audit_curation,
        enrich_wiki_topic,
        get_existing_source_urls,
        _get_existing_source_details,
        save_proposals,
        save_curation_report,
        regenerate_resource_page,
    )
    from .course_enricher import (
        generate_queries,
        run_search,
        enrich_reference_track,
    )

    assessment = await assess_wiki_coverage(lessons)

    fully_covered = assessment.get("fully_covered", [])
    needs_research = assessment.get("needs_research", [])
    no_match = assessment.get("no_match", [])

    logger.info(
        "Wiki coverage: %d fully covered, %d needs research, %d no match",
        len(fully_covered), len(needs_research), len(no_match),
    )

    if not enrich:
        return assessment

    # --- Bootstrap missing topics ---
    if no_match:
        logger.info("Bootstrapping %d new wiki topic pages...", len(no_match))
        for entry in no_match:
            les = entry["lesson"]
            proposed = entry.get("proposed_topic", "unknown")
            concepts = entry.get("unmapped", les.get("concepts", []))
            slug = bootstrap_new_wiki_topic(proposed, concepts, les.get("title", ""))
            logger.info("  Created topic: %s (%d concepts)", slug, len(concepts))
            needs_research.append({
                "lesson": les,
                "topics": [slug],
                "resolved_topics": {slug},
                "concept_verdicts": {},
                "research_topics": les.get("concepts", []),
            })
        assessment["no_match"] = []

    if not needs_research:
        logger.info("All lessons fully covered — no enrichment needed")
        return assessment

    # --- Build concept gaps ---
    concept_gaps: dict[str, list[str]] = {}
    seen_research_topics: set[str] = set()
    lessons_for_query = []

    for entry in needs_research:
        les = entry["lesson"]
        slug = les.get("slug", "")
        if not slug:
            slug = les.get("title", "").lower().replace(" ", "-")[:40]
        research_topics = entry.get("research_topics", [])
        unique_topics = []
        for rt in research_topics:
            rt_key = rt.lower().strip()
            if rt_key not in seen_research_topics:
                seen_research_topics.add(rt_key)
                unique_topics.append(rt)
        if unique_topics:
            concept_gaps[slug] = unique_topics
        lessons_for_query.append({
            "title": les.get("title", ""),
            "slug": slug,
            "summary": les.get("summary", ""),
            "concepts": les.get("concepts", []),
        })

    total_gaps = sum(len(v) for v in concept_gaps.values())
    logger.info("Generating queries for %d concept gaps...", total_gaps)

    events = await _collect_sse(
        generate_queries(
            lessons_for_query,
            course_description=course_description,
            wiki_available=True,
            concept_gaps=concept_gaps,
            course_profile=course_profile,
        )
    )

    all_queries = {}
    for ev in events:
        if ev.get("type") == "queries":
            all_queries = ev.get("data", {})

    # --- Search ---
    search_slugs = list(all_queries.keys())
    if sample and sample < len(search_slugs):
        search_slugs = search_slugs[:sample]
    search_queries = {s: all_queries[s] for s in search_slugs}

    logger.info("Running web search for %d lessons...", len(search_slugs))
    search_results = {}
    events = await _collect_sse(run_search(search_queries))
    for ev in events:
        if ev.get("type") == "search_results":
            search_results = ev.get("data", {})

    # --- Map lesson slugs to metadata ---
    slug_to_topics: dict[str, list[str]] = {}
    slug_to_gaps: dict[str, list[str]] = {}
    slug_to_title: dict[str, str] = {}
    for entry in needs_research:
        les = entry["lesson"]
        slug = les.get("slug", "")
        topics = entry.get("topics", [])
        if slug:
            slug_to_topics[slug] = topics
            slug_to_gaps[slug] = entry.get("research_topics", [])
            slug_to_title[slug] = les.get("title", slug)

    # --- Curate + audit + download per lesson ---
    total_picks = 0
    total_downloads = 0

    for lesson_slug in search_slugs:
        lesson_results = search_results.get(lesson_slug, {})
        title = slug_to_title.get(lesson_slug, lesson_slug)
        gaps = slug_to_gaps.get(lesson_slug, [])
        topic_slugs = slug_to_topics.get(lesson_slug, [])
        target_topic = topic_slugs[0] if topic_slugs else lesson_slug

        existing_urls = get_existing_source_urls(target_topic)
        existing_details = _get_existing_source_details(target_topic)

        enrichment_results = []
        if isinstance(lesson_results, dict):
            for cat_results in lesson_results.values():
                if isinstance(cat_results, list):
                    enrichment_results.extend(cat_results)

        results_by_gap: dict[str, list[dict]] = {}
        for i, gap in enumerate(gaps):
            if i < len(enrichment_results):
                results_by_gap[gap] = [enrichment_results[i]]

        if not results_by_gap:
            continue

        logger.info("  %s: %d gaps, %d existing sources", lesson_slug, len(gaps), len(existing_urls))

        curation = await curate_best_sources(
            title, gaps, results_by_gap, existing_urls,
            topic_slug=target_topic,
            course_profile=course_profile,
        )

        picks = curation["picks"]
        candidates = curation["all_candidates"]
        total_picks += len(picks)

        candidates_by_url: dict[str, dict] = {}
        for gap, results in results_by_gap.items():
            for r in results:
                snippet = r.get("content", "")[:1000]
                for c in r.get("citations", []):
                    url = c.get("url", "") if isinstance(c, dict) else str(c)
                    t = c.get("title", "") if isinstance(c, dict) else ""
                    if url and url not in existing_urls and url not in candidates_by_url:
                        candidates_by_url[url] = {
                            "url": url, "title": t,
                            "snippet": snippet, "gaps": [gap],
                        }
                    elif url in candidates_by_url:
                        if gap not in candidates_by_url[url].get("gaps", []):
                            candidates_by_url[url]["gaps"].append(gap)

        audit = await audit_curation(
            title, curation, candidates_by_url, existing_details,
        )

        promotions = audit.get("promotions", [])
        if promotions:
            picks.extend(promotions)

        if picks:
            sources = [
                {"url": p["url"], "title": p.get("title", ""),
                 "audience": p.get("audience", ""), "role": p.get("role", "")}
                for p in picks
            ]
            dl_result = await enrich_wiki_topic(target_topic, sources, extract_images=True)
            total_downloads += dl_result.get("saved", 0)
            logger.info("    Downloaded: %d saved, %d skipped",
                        dl_result.get("saved", 0), dl_result.get("skipped", 0))
        else:
            dl_result = None

        save_curation_report(
            target_topic, title,
            curation=curation, audit=audit,
            existing_details=existing_details,
            download_result=dl_result,
        )
        if candidates:
            save_proposals(target_topic, candidates,
                           run_label=f"ensure-coverage:{lesson_slug}")

    logger.info("Pedagogy enrichment: %d picks, %d downloads", total_picks, total_downloads)

    # --- Reference track enrichment ---
    ref_total_downloads = 0
    for lesson_slug in search_slugs:
        entry = next(
            (e for e in needs_research
             if e["lesson"].get("slug", "") == lesson_slug),
            None,
        )
        if not entry:
            continue
        les = entry["lesson"]
        title = les.get("title", "Untitled")
        concepts = les.get("concepts", [])
        topic_slugs_list = slug_to_topics.get(lesson_slug, [])
        target_topic = topic_slugs_list[0] if topic_slugs_list else lesson_slug

        ref_result = await enrich_reference_track(
            title, target_topic, concepts,
            lesson_summary=les.get("summary", ""),
            course_profile=course_profile,
        )
        ref_total_downloads += ref_result.get("downloads", 0)
        logger.info("  Ref track %s: %d downloads, %d ramps",
                    lesson_slug, ref_result.get("downloads", 0),
                    len(ref_result.get("unfilled_needs", [])))

    # --- Structural notes for thin concepts ---
    for entry in needs_research:
        if entry["lesson"].get("slug", "") not in search_slugs:
            continue
        verdicts = entry.get("concept_verdicts", {})
        topics = entry.get("topics", [])
        thin_concepts = [
            c for c, v in verdicts.items()
            if isinstance(v, dict) and v.get("verdict") == "thin"
        ]
        if thin_concepts and topics:
            file_structural_note(
                topics[0],
                concept=entry["lesson"].get("title", ""),
                sub_concepts=thin_concepts,
                course_title=course_description[:80] or "course",
            )

    logger.info("Enrichment complete: %d pedagogy + %d reference downloads",
                total_downloads, ref_total_downloads)

    # Regenerate resource pages for enriched topics
    enriched_topics: set[str] = set()
    for topics_list in slug_to_topics.values():
        enriched_topics.update(topics_list)
    for topic in enriched_topics:
        try:
            await regenerate_resource_page(topic, course_profile=course_profile)
        except Exception as e:
            logger.warning("Resource page regen failed for %s: %s", topic, e)

    return assessment


async def ensure_wiki_coverage_stream(
    lessons: list[dict],
    course_description: str = "",
    *,
    sample: int | None = None,
    course_profile: dict | None = None,
) -> AsyncGenerator[str, None]:
    """Streaming version of ``ensure_wiki_coverage`` that yields SSE events.

    Uses the same ``assess_wiki_coverage`` for assessment, then runs the
    enrichment pipeline with per-step SSE events.  The enrichment loop
    mirrors ``ensure_wiki_coverage`` — kept in sync manually because the
    generator control flow (``yield`` between steps) prevents simple reuse.
    """
    from .wiki_downloader import (
        bootstrap_new_wiki_topic,
        curate_best_sources,
        audit_curation,
        enrich_wiki_topic,
        get_existing_source_urls,
        _get_existing_source_details,
        save_proposals,
        save_curation_report,
        regenerate_resource_page,
    )
    from .course_enricher import (
        generate_queries,
        run_search,
        enrich_reference_track,
    )

    yield _sse({"type": "status", "message": f"Assessing {len(lessons)} lessons..."})

    assessment = await assess_wiki_coverage(lessons)

    fully_covered = assessment.get("fully_covered", [])
    needs_research = assessment.get("needs_research", [])
    no_match = assessment.get("no_match", [])

    yield _sse({
        "type": "assessment_summary",
        "fully_covered": len(fully_covered),
        "needs_research": len(needs_research),
        "no_match": len(no_match),
    })

    # --- Bootstrap missing topics ---
    if no_match:
        for entry in no_match:
            les = entry["lesson"]
            proposed = entry.get("proposed_topic", "unknown")
            concepts = entry.get("unmapped", les.get("concepts", []))
            slug = bootstrap_new_wiki_topic(proposed, concepts, les.get("title", ""))
            yield _sse({
                "type": "bootstrap",
                "slug": les.get("slug", ""),
                "title": les.get("title", ""),
                "topic_created": slug,
                "concepts": concepts,
            })
            needs_research.append({
                "lesson": les,
                "topics": [slug],
                "resolved_topics": {slug},
                "concept_verdicts": {},
                "research_topics": les.get("concepts", []),
            })
        assessment["no_match"] = []

    if not needs_research:
        yield _sse({"type": "enrich_complete", "total_picks": 0, "total_downloads": 0})
        yield _sse({"type": "done"})
        return

    # --- Build concept gaps ---
    concept_gaps: dict[str, list[str]] = {}
    seen_research_topics: set[str] = set()
    lessons_for_query = []

    for entry in needs_research:
        les = entry["lesson"]
        slug = les.get("slug", "")
        if not slug:
            slug = les.get("title", "").lower().replace(" ", "-")[:40]
        research_topics = entry.get("research_topics", [])
        unique_topics = []
        for rt in research_topics:
            rt_key = rt.lower().strip()
            if rt_key not in seen_research_topics:
                seen_research_topics.add(rt_key)
                unique_topics.append(rt)
        if unique_topics:
            concept_gaps[slug] = unique_topics
        lessons_for_query.append({
            "title": les.get("title", ""),
            "slug": slug,
            "summary": les.get("summary", ""),
            "concepts": les.get("concepts", []),
        })

    total_gaps = sum(len(v) for v in concept_gaps.values())
    yield _sse({"type": "status", "message": f"Generating queries for {total_gaps} concept gaps..."})

    events = await _collect_sse(
        generate_queries(
            lessons_for_query,
            course_description=course_description,
            wiki_available=True,
            concept_gaps=concept_gaps,
            course_profile=course_profile,
        )
    )

    all_queries = {}
    for ev in events:
        if ev.get("type") == "queries":
            all_queries = ev.get("data", {})

    # Emit queries per lesson
    for lesson_slug, categories in all_queries.items():
        flat_queries = []
        for cat_queries in categories.values():
            flat_queries.extend(cat_queries)
        yield _sse({
            "type": "queries",
            "slug": lesson_slug,
            "queries": flat_queries,
            "category_count": len(categories),
        })

    # --- Search ---
    search_slugs = list(all_queries.keys())
    if sample and sample < len(search_slugs):
        search_slugs = search_slugs[:sample]
    search_queries = {s: all_queries[s] for s in search_slugs}

    yield _sse({"type": "status", "message": f"Running web search for {len(search_slugs)} lessons..."})

    search_results = {}
    events = await _collect_sse(run_search(search_queries))
    for ev in events:
        if ev.get("type") == "search_results":
            search_results = ev.get("data", {})

    for lesson_slug, results in search_results.items():
        result_count = 0
        citations = []
        if isinstance(results, dict):
            for cat_results in results.values():
                if isinstance(cat_results, list):
                    for r in cat_results:
                        result_count += 1
                        for c in r.get("citations", []):
                            url = c.get("url", "") if isinstance(c, dict) else str(c)
                            title = c.get("title", "") if isinstance(c, dict) else ""
                            if url:
                                citations.append({"url": url, "title": title})
        yield _sse({
            "type": "search_result",
            "slug": lesson_slug,
            "result_count": result_count,
            "citation_count": len(citations),
            "citations": citations[:20],
        })

    # --- Map lesson slugs to metadata ---
    slug_to_topics: dict[str, list[str]] = {}
    slug_to_gaps: dict[str, list[str]] = {}
    slug_to_title: dict[str, str] = {}
    for entry in needs_research:
        les = entry["lesson"]
        slug = les.get("slug", "")
        topics = entry.get("topics", [])
        if slug:
            slug_to_topics[slug] = topics
            slug_to_gaps[slug] = entry.get("research_topics", [])
            slug_to_title[slug] = les.get("title", slug)

    # --- Curate + audit + download per lesson ---
    total_picks = 0
    total_downloads = 0

    for lesson_slug in search_slugs:
        lesson_results = search_results.get(lesson_slug, {})
        title = slug_to_title.get(lesson_slug, lesson_slug)
        gaps = slug_to_gaps.get(lesson_slug, [])
        topic_slugs = slug_to_topics.get(lesson_slug, [])
        target_topic = topic_slugs[0] if topic_slugs else lesson_slug

        existing_urls = get_existing_source_urls(target_topic)
        existing_details = _get_existing_source_details(target_topic)

        enrichment_results = []
        if isinstance(lesson_results, dict):
            for cat_results in lesson_results.values():
                if isinstance(cat_results, list):
                    enrichment_results.extend(cat_results)

        results_by_gap: dict[str, list[dict]] = {}
        for i, gap in enumerate(gaps):
            if i < len(enrichment_results):
                results_by_gap[gap] = [enrichment_results[i]]

        if not results_by_gap:
            continue

        curation = await curate_best_sources(
            title, gaps, results_by_gap, existing_urls,
            topic_slug=target_topic,
            course_profile=course_profile,
        )

        picks = curation["picks"]
        candidates = curation["all_candidates"]
        total_picks += len(picks)
        dl_result = None

        candidates_by_url: dict[str, dict] = {}
        for gap, results in results_by_gap.items():
            for r in results:
                snippet = r.get("content", "")[:1000]
                for c in r.get("citations", []):
                    url = c.get("url", "") if isinstance(c, dict) else str(c)
                    t = c.get("title", "") if isinstance(c, dict) else ""
                    if url and url not in existing_urls and url not in candidates_by_url:
                        candidates_by_url[url] = {
                            "url": url, "title": t,
                            "snippet": snippet, "gaps": [gap],
                        }
                    elif url in candidates_by_url:
                        if gap not in candidates_by_url[url].get("gaps", []):
                            candidates_by_url[url]["gaps"].append(gap)

        audit = await audit_curation(
            title, curation, candidates_by_url, existing_details,
        )

        promotions = audit.get("promotions", [])
        if promotions:
            picks.extend(promotions)

        curator_near_misses = curation.get("near_misses", [])
        pick_urls = {p.get("url") for p in picks}

        yield _sse({
            "type": "curation",
            "slug": lesson_slug,
            "title": title,
            "topic": target_topic,
            "picks": [
                {
                    "url": p.get("url", ""),
                    "title": p.get("title", ""),
                    "role": p.get("role", ""),
                    "why": p.get("why", ""),
                    "gaps_covered": p.get("gaps_covered", []),
                    "level": p.get("level", ""),
                }
                for p in picks
            ],
            "near_misses": [
                {
                    "url": nm.get("url", ""),
                    "title": nm.get("title", ""),
                    "why_not": nm.get("why_not", ""),
                }
                for nm in curator_near_misses[:10]
            ],
            "total_candidates": len(candidates),
        })

        if picks:
            sources = [
                {"url": p["url"], "title": p.get("title", ""),
                 "audience": p.get("audience", ""), "role": p.get("role", "")}
                for p in picks
            ]
            dl_result = await enrich_wiki_topic(target_topic, sources, extract_images=True)
            total_downloads += dl_result.get("saved", 0)
            yield _sse({
                "type": "download",
                "slug": lesson_slug,
                "topic": target_topic,
                "saved": dl_result.get("saved", 0),
                "skipped": dl_result.get("skipped", 0),
            })

        save_curation_report(
            target_topic, title,
            curation=curation, audit=audit,
            existing_details=existing_details,
            download_result=dl_result if picks else None,
        )
        if candidates:
            save_proposals(target_topic, candidates,
                           run_label=f"ensure-coverage:{lesson_slug}")

    # --- Reference track enrichment ---
    ref_total_downloads = 0
    for lesson_slug in search_slugs:
        entry = next(
            (e for e in needs_research
             if e["lesson"].get("slug", "") == lesson_slug),
            None,
        )
        if not entry:
            continue
        les = entry["lesson"]
        title = les.get("title", "Untitled")
        concepts = les.get("concepts", [])
        topic_slugs_list = slug_to_topics.get(lesson_slug, [])
        target_topic = topic_slugs_list[0] if topic_slugs_list else lesson_slug

        ref_result = await enrich_reference_track(
            title, target_topic, concepts,
            lesson_summary=les.get("summary", ""),
            course_profile=course_profile,
        )
        ref_total_downloads += ref_result.get("downloads", 0)
        yield _sse({
            "type": "reference_enrichment",
            "slug": lesson_slug,
            "downloads": ref_result.get("downloads", 0),
            "unfilled_needs": ref_result.get("unfilled_needs", []),
        })

    # --- Structural notes for thin concepts ---
    for entry in needs_research:
        if entry["lesson"].get("slug", "") not in search_slugs:
            continue
        verdicts = entry.get("concept_verdicts", {})
        topics = entry.get("topics", [])
        thin_concepts = [
            c for c, v in verdicts.items()
            if isinstance(v, dict) and v.get("verdict") == "thin"
        ]
        if thin_concepts and topics:
            file_structural_note(
                topics[0],
                concept=entry["lesson"].get("title", ""),
                sub_concepts=thin_concepts,
                course_title=course_description[:80] or "course",
            )

    # Regenerate resource pages for enriched topics
    enriched_topics: set[str] = set()
    for topics_list in slug_to_topics.values():
        enriched_topics.update(topics_list)
    regen_count = 0
    for topic in enriched_topics:
        try:
            if await regenerate_resource_page(topic, course_profile=course_profile):
                regen_count += 1
        except Exception as e:
            logger.warning("Resource page regen failed for %s: %s", topic, e)

    yield _sse({
        "type": "enrich_complete",
        "total_picks": total_picks,
        "total_downloads": total_downloads + ref_total_downloads,
        "resource_pages_regenerated": regen_count,
    })
    yield _sse({"type": "done"})


def _score_source_relevance(content: str, concepts: list[str]) -> int:
    """Score a source by how many lesson concepts appear near the top.

    Checks the first ~500 words (title, abstract, headers, intro) for
    concept keyword matches.  Fast keyword heuristic — no LLM call.
    """
    words = content.split()
    searchable = " ".join(words[:500]).lower()
    return sum(1 for c in concepts if c.lower() in searchable)


def _truncate_to_words(text: str, max_words: int) -> str:
    """Truncate text to approximately max_words."""
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words])


def _extract_audience_tag(content: str) -> str:
    """Extract the ``# Audience:`` tag from a source file's header lines."""
    for line in content.split("\n", 8)[:8]:
        if line.startswith("# Audience:"):
            return line.replace("# Audience:", "").strip().lower()
    return ""


_AUDIENCE_AFFINITY = {
    "practical-hands-on": {"practitioner", "general", "all"},
    "technical-precise": {"technical", "all"},
    "conceptual-theoretical": {"technical", "all"},
}


def _build_wiki_source_context(
    wiki_ctx: dict, lesson_concepts: list[str], max_words: int = 15000,
    per_source_words: int = 500,
    course_profile: dict | None = None,
) -> str:
    """Build a source context string from wiki downloaded content for a lesson.

    Two-pass packing:
      1. **Coverage pass** — for each lesson concept, pick the single
         best source that mentions it (highest relevance, then word count).
         This guarantees every concept has at least one source in context.
      2. **Fill pass** — fill remaining budget with the highest-relevance
         sources that weren't already included.

    When ``course_profile`` is provided, sources whose ``# Audience:``
    header matches the profile's tone receive a soft relevance boost (+2).

    Budget is in words (~0.75 words per token).  Each source gets up to
    ``per_source_words`` words to maximise source diversity.
    """
    preferred_audiences = set()
    if course_profile:
        tone = course_profile.get("tone", "")
        preferred_audiences = _AUDIENCE_AFFINITY.get(tone, set())

    all_sources: list[tuple[int, int, str, str]] = []

    for slug in wiki_ctx.get("topics", []):
        for src in wiki_ctx.get("source_content", {}).get(slug, []):
            content = src["content"]
            header = content.split("\n", 4)
            source_line = next(
                (l for l in header if l.startswith("# Source:") or l.startswith("# Transcript:")),
                src["file"],
            )
            relevance = _score_source_relevance(content, lesson_concepts)

            if preferred_audiences:
                src_audience = _extract_audience_tag(content)
                if src_audience and src_audience in preferred_audiences:
                    relevance += 2

            word_count = len(content.split())
            all_sources.append((relevance, word_count, source_line, content))

    all_sources.sort(key=lambda x: (x[0], x[1]), reverse=True)

    # Pass 1: guarantee at least one source per concept
    selected_indices: set[int] = set()
    for concept in lesson_concepts:
        cl = concept.lower()
        for i, (_rel, _wc, _sl, content) in enumerate(all_sources):
            if i not in selected_indices and cl in " ".join(content.split()[:1000]).lower():
                selected_indices.add(i)
                break

    # Pass 2: fill remaining budget by relevance
    ordered = (
        [i for i in sorted(selected_indices)]
        + [i for i in range(len(all_sources)) if i not in selected_indices]
    )

    parts: list[str] = []
    total = 0
    for i in ordered:
        _rel, _wc, source_line, content = all_sources[i]
        available = max_words - total
        if available <= 50:
            break
        text = _truncate_to_words(content, min(available, per_source_words))
        word_count = len(text.split())
        parts.append(f"--- {source_line} ---\n{text}")
        total += word_count

    return "\n\n".join(parts)


def select_lesson_images(
    wiki_ctx: dict,
    lesson_concepts: list[str],
    *,
    source_urls: list[str] | None = None,
    max_images: int | None = None,
) -> list[dict]:
    """Select images for a lesson, matched through source pages.

    When ``source_urls`` is provided (from the lesson's sources_used),
    only images whose ``source_page`` matches one of those URLs are
    included — this is the tight lesson → source → image chain.

    When ``source_urls`` is None (e.g. during initial generation before
    sources_used exists), falls back to including all topic images.

    Concept overlap is used for ranking (best images first in prompt).
    ``max_images=None`` returns all matches (for DB storage).
    """
    concept_set = {c.lower() for c in lesson_concepts}

    # Normalize source URLs for matching (strip trailing slash, fragment)
    source_set: set[str] | None = None
    if source_urls:
        source_set = set()
        for url in source_urls:
            normalized = url.rstrip("/").split("#")[0]
            source_set.add(normalized)

    scored: list[tuple[int, str, dict]] = []

    for slug in wiki_ctx.get("topics", []):
        for img in wiki_ctx.get("images", {}).get(slug, []):
            if not img.get("file"):
                continue

            # Source-page filter: if we have source URLs, only include
            # images from those sources
            if source_set is not None:
                img_source = img.get("source_page", "").rstrip("/").split("#")[0]
                if img_source not in source_set:
                    continue

            img_concepts = {c.lower() for c in img.get("concepts", [])}
            overlap = len(concept_set & img_concepts)
            scored.append((overlap, slug, img))

    if not scored:
        return []

    scored.sort(key=lambda t: t[0], reverse=True)
    if max_images is not None:
        scored = scored[:max_images]
    return [
        {
            "file": img["file"],
            "topic": slug,
            "source_page": img.get("source_page", ""),
            "caption": img.get("suggested_caption", ""),
            "when_to_show": img.get("when_to_show", ""),
            "concepts": img.get("concepts", [])[:6],
            "description": img.get("description", ""),
        }
        for _, slug, img in scored
    ]


def _build_image_context(
    wiki_ctx: dict,
    lesson_concepts: list[str],
    *,
    max_images: int = 8,
) -> str:
    """Format top-ranked images as text for generation prompts."""
    selected = select_lesson_images(wiki_ctx, lesson_concepts, max_images=max_images)
    if not selected:
        return ""

    lines = ["AVAILABLE EDUCATIONAL IMAGES:"]
    for i, img in enumerate(selected, 1):
        # Guard: if 'file' contains a nested topic path (e.g. "other-topic/images/foo.png"),
        # use the nested path directly rather than double-nesting it.
        raw_file = img["file"]
        if "/images/" in raw_file:
            topic_part, _, filename = raw_file.partition("/images/")
            path = f"/api/wiki-images/{topic_part}/images/{filename}"
        else:
            path = f"/api/wiki-images/{img['topic']}/images/{raw_file}"
        caption = img.get("caption") or img.get("description", "")[:80]
        lines.append(f"\n{i}. **{img['file']}**")
        lines.append(f'   Caption: "{caption}"')
        if img.get("when_to_show"):
            lines.append(f"   When to show: {img['when_to_show']}")
        if img.get("concepts"):
            lines.append(f"   Concepts: {', '.join(img['concepts'][:6])}")
        lines.append(f"   Path: {path}")

    return "\n".join(lines)


def _build_wiki_metadata(wiki_ctx: dict) -> dict:
    """Extract youtube_id, video_title, all_videos, and recommended reading."""
    result: dict = {
        "youtube_id": None, "video_title": None,
        "all_videos": [],
        "reading": [],
    }

    for slug in wiki_ctx.get("topics", []):
        yt_list = wiki_ctx.get("youtube_ids", {}).get(slug, [])
        for yt_id, title_line in yt_list:
            cleaned_title = ""
            if title_line:
                cleaned_title = re.sub(r'^- \*\*[^*]+\*\*\s*[—–-]\s*', '', title_line)
                cleaned_title = cleaned_title.strip('"').strip()
            if not result["youtube_id"]:
                result["youtube_id"] = yt_id
                result["video_title"] = cleaned_title or None
            result["all_videos"].append((yt_id, cleaned_title))

        for title_line, url in wiki_ctx.get("recommended_reading", {}).get(slug, []):
            if len(result["reading"]) >= 5:
                break
            name = re.sub(r'^- \*\*([^*]+)\*\*.*', r'\1', title_line) if title_line else url
            result["reading"].append({"title": name.strip(), "url": url})

    return result


def _build_resource_summary(wiki_ctx: dict) -> str:
    """Build a formatted inventory of available resources for the KB prompt.

    Pulls YouTube videos and recommended reading from wiki context and formats
    them as a section the LLM can use to generate a ## Available Resources
    catalog in the reference KB.
    """
    meta = _build_wiki_metadata(wiki_ctx)
    lines: list[str] = []

    if meta["all_videos"]:
        lines.append("AVAILABLE VIDEOS:")
        for yt_id, title in meta["all_videos"][:5]:
            display = title if title else f"Video ({yt_id})"
            lines.append(f"- {display} — https://youtube.com/watch?v={yt_id}")

    if meta["reading"]:
        lines.append("\nAVAILABLE ARTICLES & TUTORIALS:")
        for item in meta["reading"]:
            lines.append(f"- {item['title']} — {item['url']}")

    return "\n".join(lines) if lines else ""


def _load_reference_ramps(topic_slugs: list[str]) -> str:
    """Load ramps.json from the reference track and format for the KB prompt.

    Ramps are unfilled reference needs — precision anchors that no curated
    source could provide.  They tell the KB prompt to include "search for X"
    guidance in the Available Resources section.
    """
    topics_dir = _WIKI_DIR / "resources" / "by-topic"
    all_ramps: list[dict] = []
    for slug in topic_slugs:
        ramps_path = topics_dir / slug / "reference" / "ramps.json"
        if ramps_path.exists():
            try:
                ramps = json.loads(ramps_path.read_text())
                all_ramps.extend(ramps)
            except (json.JSONDecodeError, ValueError):
                pass

    if not all_ramps:
        return ""

    lines = ["\n\nUNFILLED REFERENCE NEEDS (suggest the tutor search at runtime):"]
    for ramp in all_ramps[:8]:
        need_type = ramp.get("need_type", "UNKNOWN")
        description = ramp.get("description", "")
        search_hint = ramp.get("search_hint", "")
        hint_str = f' — search: "{search_hint}"' if search_hint else ""
        lines.append(f"- {need_type}: {description}{hint_str}")

    return "\n".join(lines)


_MAX_VIDEO_APPEARANCES = 2


def deduplicate_youtube_ids(
    lessons: dict[str, dict],
    *,
    alt_videos: dict[str, list[tuple[str, str]]] | None = None,
) -> dict[str, dict]:
    """Cap each YouTube video to at most _MAX_VIDEO_APPEARANCES across lessons.

    When a video is removed from a lesson, tries to assign the next best
    alternative from ``alt_videos[slug]`` (list of ``(yt_id, title)`` pairs).

    Modifies lessons in-place and returns the same dict.
    """
    yt_counts: dict[str, int] = {}

    # First pass: count appearances
    for slug, lesson in lessons.items():
        yt_id = lesson.get("youtube_id")
        if yt_id:
            yt_counts.setdefault(yt_id, 0)
            yt_counts[yt_id] += 1

    # Second pass: remove over-limit and try fallbacks
    final_counts: dict[str, int] = {}
    for slug, lesson in lessons.items():
        yt_id = lesson.get("youtube_id")
        if not yt_id:
            continue
        final_counts.setdefault(yt_id, 0)
        final_counts[yt_id] += 1
        if final_counts[yt_id] > _MAX_VIDEO_APPEARANCES:
            lesson.pop("youtube_id", None)
            lesson.pop("video_title", None)

            # Try alternatives
            if alt_videos and slug in alt_videos:
                for alt_id, alt_title in alt_videos[slug]:
                    if alt_id == yt_id:
                        continue
                    alt_count = final_counts.get(alt_id, 0)
                    if alt_count < _MAX_VIDEO_APPEARANCES:
                        lesson["youtube_id"] = alt_id
                        if alt_title:
                            lesson["video_title"] = alt_title
                        final_counts.setdefault(alt_id, 0)
                        final_counts[alt_id] += 1
                        break

    return lessons


# ---------------------------------------------------------------------------
# Wiki feedback — file new sources discovered during enrichment
# ---------------------------------------------------------------------------

import time as _time


def file_source_to_wiki(
    topic_slug: str,
    source: dict,
) -> bool:
    """Append a discovered source to a topic's resource page.

    Args:
        topic_slug: the wiki topic slug (e.g. 'attention-mechanism')
        source: {
            "type": "video" | "blog" | "paper" | "code",
            "title": str,
            "url": str,
            "educator": str (optional),
            "why": str,
            "confidence": "high" | "medium" | "low",
        }

    Returns True if filed, False if topic page doesn't exist.
    """
    topics_dir = _WIKI_DIR / "resources" / "by-topic"
    page_path = topics_dir / f"{topic_slug}.md"
    if not page_path.exists():
        logger.warning("Wiki feedback: no page for topic %r", topic_slug)
        return False

    content = page_path.read_text()

    educator = source.get("educator", "")
    title = source.get("title", "")
    url = source.get("url", "")
    why = source.get("why", "")
    confidence = source.get("confidence", "medium")
    stype = source.get("type", "resource")
    today = _time.strftime("%Y-%m-%d")

    entry = (
        f"\n> **[Filed from enrichment]** - "
        f"**{educator}** — [{title}]({url}) "
        f"({stype})\n"
        f"> *Why*: {why}\n"
        f"> *Confidence*: {confidence} | *Found*: {today}\n"
    )

    if "## Last Verified" in content:
        content = content.replace(
            "## Last Verified",
            f"{entry}\n## Last Verified",
        )
    else:
        content += entry

    page_path.write_text(content)
    logger.info(
        "Wiki feedback: filed %r to %s.md", title, topic_slug
    )
    return True


def file_structural_note(
    topic_slug: str,
    concept: str,
    sub_concepts: list[str],
    *,
    course_title: str = "",
) -> bool:
    """Stage a structural observation note for a topic's resource page.

    Instead of modifying the tracked page directly, writes a pending
    item for human-reviewed merge.
    """
    from .wiki_downloader import _write_pending_item

    today = _time.strftime("%Y-%m-%d")
    note_text = (
        f"\n> **[Structural note]** \"{concept}\" appears to have sub-concepts:\n"
        f"> {', '.join(sub_concepts)}\n"
        f"> *Discovered during enrichment for course \"{course_title}\" | {today}*\n"
    )

    _write_pending_item(
        "structural_note",
        topic_slug,
        {
            "concept": concept,
            "sub_concepts": sub_concepts,
            "note_text": note_text,
        },
        course=course_title,
    )
    logger.info("Staged structural note: %r has sub-concepts on %s", concept, topic_slug)
    return True


# ---------------------------------------------------------------------------
# Concept map scaffolding — coverage check after outline generation
# ---------------------------------------------------------------------------


def check_outline_coverage(outline: dict) -> dict:
    """Check an outline's concepts against the concept map for coverage gaps.

    Returns:
        {
            "lessons_checked": int,
            "gaps": [
                {
                    "lesson_title": str,
                    "lesson_slug": str,
                    "topic": str,
                    "missing_subtopics": [str, ...],
                    "suggestion": str,
                },
                ...
            ],
            "wiki_topics_used": [str, ...],
            "concepts_not_in_wiki": [str, ...],
        }
    """
    concept_map = _load_concept_map()

    concept_map_path = _CONCEPT_MAP_PATH
    topic_subtopics: dict[str, list[str]] = {}
    if concept_map_path.exists():
        current_topic = ""
        for line in concept_map_path.read_text().splitlines():
            if line.startswith("# ") and not line.startswith("# Concept"):
                current_topic = line[2:].strip()
            elif line.startswith("## ") and current_topic:
                topic_subtopics.setdefault(current_topic, []).append(
                    line[3:].strip()
                )

    modules = outline.get("modules", [])
    all_lessons: list[dict] = []
    for module in modules:
        if "lesson_slugs" in module:
            for slug in module["lesson_slugs"]:
                lesson_data = (outline.get("_lessons_dict") or {}).get(slug, {})
                all_lessons.append({
                    "title": lesson_data.get("title", slug),
                    "slug": slug,
                    "concepts": lesson_data.get("concepts", []),
                })
        else:
            for les in module.get("lessons", []):
                all_lessons.append(les)

    gaps = []
    wiki_topics: set[str] = set()
    unmapped: set[str] = set()

    for lesson in all_lessons:
        lesson_concepts = [c.lower().strip() for c in lesson.get("concepts", [])]
        lesson_topics: set[str] = set()

        for concept in lesson_concepts:
            topic = concept_map.get(concept)
            if topic:
                lesson_topics.add(topic)
                wiki_topics.add(topic)
            else:
                unmapped.add(concept)

        for topic in lesson_topics:
            subtopics = topic_subtopics.get(topic, [])
            if not subtopics:
                continue
            covered = set()
            for st in subtopics:
                st_lower = st.lower()
                if any(st_lower in c or c in st_lower for c in lesson_concepts):
                    covered.add(st)

            missing = [st for st in subtopics if st not in covered]
            if missing and len(missing) < len(subtopics):
                gaps.append({
                    "lesson_title": lesson.get("title", ""),
                    "lesson_slug": lesson.get("slug", ""),
                    "topic": topic,
                    "missing_subtopics": missing,
                    "suggestion": (
                        f"Consider covering: {', '.join(missing)} "
                        f"(from topic '{topic}')"
                    ),
                })

    return {
        "lessons_checked": len(all_lessons),
        "gaps": gaps,
        "wiki_topics_used": sorted(wiki_topics),
        "concepts_not_in_wiki": sorted(unmapped),
    }


# ---------------------------------------------------------------------------
# Phase 2: Content generation
# ---------------------------------------------------------------------------

CONTENT_FROM_WIKI_PROMPT = """\
You are an exceptional technical writer creating student-facing lesson \
notes. You write like the best educators — think Karpathy's blog posts, \
3Blue1Brown's scripts, or Alammar's illustrated guides. Your writing is \
warm, clear, builds concepts progressively, and makes the reader feel \
smart rather than overwhelmed.

The SOURCE MATERIAL below contains curated excerpts from top blogs, \
papers, and tutorials. Use them to inform WHAT you teach — the facts, \
the intuitions, the examples — but write in YOUR OWN narrative voice. \
Do NOT cite sources inline in the prose. The student should feel like \
they're reading a great explainer, not a literature review.

**Lesson Title:** {title}
**Summary:** {summary}
**Key Concepts:** {concepts}

{course_profile}

SOURCE MATERIAL ({source_count} curated resources):
{wiki_source_context}

WIKI RESOURCE NOTES:
{resource_page_excerpt}

{image_context}

WRITING GUIDELINES:
- Write naturally — vary your openings and structure across lessons. \
Sometimes a question works, sometimes jumping straight into "here's \
the problem" is better. Avoid a formulaic pattern.
- Build concepts progressively so each section unlocks the next
- Use analogies when they genuinely clarify — but don't force one into \
every section. Sometimes the concept speaks for itself.
- Include code examples when they crystallize understanding
- Use comparison tables when they genuinely clarify tradeoffs or \
alternatives (e.g. "RAG vs fine-tuning", "BPE vs WordPiece"). A concise \
table can convey structure that prose cannot — but only include one if \
the lesson naturally has things worth comparing side by side.
- Bold key terms on first use, but don't over-bold
- Keep the tone conversational but technically precise
- Target 400-600 words of Markdown content
- End with a brief ## Summary (2-3 sentences reinforcing the key insight)
- If AVAILABLE EDUCATIONAL IMAGES are listed above, include relevant ones \
using Markdown image syntax: ![caption](path). Place images where they \
genuinely aid understanding. Add a brief source attribution in the \
caption (e.g. "Adapted from Alammar"). Do NOT force images if none help.
- At the end, add a ## Recommended Reading section with 2-4 links from \
the sources: - [Title](url) — one-line description

CITATION RULES:
- Do NOT cite sources inline in the body text (no "[Source](url)" in prose)
- DO include source attribution in image captions and table footnotes
- The Recommended Reading section at the end is the only place for links
- The sources_used JSON field captures provenance — it does not need to \
appear in the visible content

Produce a JSON object with:
- "content": Structured Markdown (hook intro, ## headings, progressive \
concept building, code blocks, images with captions, ## Summary, \
## Recommended Reading at end)
- "summary": Refined 1-2 sentence summary
- "concepts": Refined array of 4-8 key concepts (lowercase)
- "sources_used": array of source URLs you drew facts from (for metadata, \
not displayed to student)
- "youtube_id": a YouTube video ID (11 chars) ONLY if the source material \
contains a video that is specifically about this lesson's topic. \
Most lessons will NOT have a matching video — return null in that case. \
Do NOT reuse a generic or loosely related video just to fill this field.
- "video_title": title of that video, or null if youtube_id is null

Return ONLY valid JSON.
"""

CONTENT_GENERATION_PROMPT = """\
You are a senior technical content specialist creating learning materials.

Create structured lesson content for the following lesson:

**Lesson Title:** {title}
**Summary:** {summary}
**Key Concepts:** {concepts}

{transcript_section}

Produce a JSON object with:
- "content": Structured Markdown (600-1000 words) with:
  - A 2-3 sentence intro paragraph
  - ## headings for major topics
  - Bullet points for key details
  - **Bold** important terms on first use
  - Backtick CLI commands and file paths
- "summary": Refined 1-2 sentence summary
- "concepts": Refined array of 4-8 key concepts (lowercase)

Return ONLY valid JSON.
"""

CONTENT_FROM_KB_PROMPT = """\
You are a senior technical content specialist creating student-facing \
learning materials from reference knowledge.

Create structured lesson content for the following lesson. Your content \
must be grounded in the REFERENCE KNOWLEDGE provided — do not invent \
facts or details not present in the reference material.

**Lesson Title:** {title}
**Summary:** {summary}
**Key Concepts:** {concepts}

REFERENCE KNOWLEDGE:
{reference_kb}

INSTRUCTIONS:
- Write clear, educational content for students learning this topic
- Ground every claim in the reference knowledge above
- Use a pedagogical structure: intro → core concepts → details → summary
- Keep the tone accessible but technically precise
- Target 600-1000 words of Markdown content

Produce a JSON object with:
- "content": Structured Markdown with:
  - A 2-3 sentence intro paragraph
  - ## headings for major topics
  - Bullet points for key details
  - **Bold** important terms on first use
  - Backtick CLI commands and file paths
- "summary": Refined 1-2 sentence summary
- "concepts": Refined array of 4-8 key concepts (lowercase)

Return ONLY valid JSON.
"""

async def generate_content(
    outline: dict,
    source_text: str,
    source_type: str,
    existing_lessons: list[dict] | None = None,
    reference_kb: dict[str, str] | None = None,
    wiki_context: dict | None = None,
    course_profile: dict | None = None,
) -> AsyncGenerator[str, None]:
    """Generate content for each lesson in the outline. Yields SSE events.

    Priority for content grounding:
      1. wiki_context — curated sources from pedagogy wiki (downloaded blogs/transcripts)
      2. reference_kb — per-lesson KB from the enrichment pipeline
      3. transcript / bare prompt — original fallback

    If existing_lessons is provided, lessons that already have content are
    emitted as "skipped" and not re-generated.
    """
    modules = outline.get("modules", [])

    all_lessons: list[dict] = []
    for module in modules:
        if "lesson_slugs" in module:
            for slug in module["lesson_slugs"]:
                lesson_data = (outline.get("_lessons_dict") or {}).get(slug, {})
                all_lessons.append({
                    "title": lesson_data.get("title", slug),
                    "slug": slug,
                    "summary": lesson_data.get("summary", ""),
                    "concepts": lesson_data.get("concepts", []),
                })
        else:
            for les in module.get("lessons", []):
                all_lessons.append(les)

    total_lessons = len(all_lessons)
    index = 0

    existing_by_slug: dict[str, dict] = {}
    existing_by_title: dict[str, dict] = {}
    if existing_lessons:
        for el in existing_lessons:
            slug = el.get("slug", "")
            title_norm = el.get("title", "").strip().lower()
            if el.get("content"):
                if slug:
                    existing_by_slug[slug] = el
                if title_norm:
                    existing_by_title[title_norm] = el
        logger.warning(
            "Resume mode: %d lessons cached by slug: %s",
            len(existing_by_slug), list(existing_by_slug.keys()),
        )

    # Emit skipped lessons immediately, collect lessons that need generation
    to_generate: list[tuple[int, dict]] = []
    for i, lesson in enumerate(all_lessons, 1):
        title = lesson.get("title", "Untitled")
        slug = lesson.get("slug", "")
        cached = existing_by_slug.get(slug) or existing_by_title.get(title.strip().lower())
        if cached:
            logger.info("SKIP %d/%d %r (slug=%r)", i, total_lessons, title, slug)
            yield _sse({
                "type": "progress",
                "lesson_title": title,
                "index": i,
                "total": total_lessons,
                "status": "done",
                "skipped": True,
                "word_count": len(cached.get("content", "").split()),
                "lesson": cached,
            })
        else:
            to_generate.append((i, lesson))

    if not to_generate:
        yield _sse({"type": "content", "data": outline})
        yield _sse({"type": "done"})
        return

    async def _generate_one(idx: int, lesson: dict) -> dict:
        title = lesson.get("title", "Untitled")
        slug = lesson.get("slug", "")

        lesson_concepts = lesson.get("concepts", [])
        lesson_wiki_ctx = None
        lesson_ref_ctx = None
        if wiki_context is None and lesson_concepts:
            resolved = await resolve_topics_llm(
                lesson_concepts,
                lesson_title=title,
                lesson_summary=lesson.get("summary", ""),
            )
            lesson_wiki_ctx = load_wiki_context(
                lesson_concepts,
                topic_slugs=resolved["topic_slugs"],
            )
            if not lesson_wiki_ctx.get("source_content"):
                lesson_wiki_ctx = None
            else:
                lesson_ref_ctx = load_wiki_context(
                    lesson_concepts,
                    topic_slugs=resolved["topic_slugs"],
                    track="reference",
                )
                if not lesson_ref_ctx.get("source_content"):
                    lesson_ref_ctx = None
        elif wiki_context and wiki_context.get("source_content"):
            lesson_wiki_ctx = wiki_context

        # Use bundle (notes + KB in parallel) when wiki sources exist
        if lesson_wiki_ctx and lesson_wiki_ctx.get("source_content"):
            try:
                bundle = await generate_lesson_bundle(
                    lesson, lesson_wiki_ctx,
                    reference_ctx=lesson_ref_ctx,
                    course_profile=course_profile,
                )
                content_result = bundle["content"]
                out = {
                    "idx": idx, "status": "done",
                    "title": title, "slug": slug,
                    "content": content_result.get("content", ""),
                    "summary": content_result.get("summary", lesson.get("summary", "")),
                    "concepts": content_result.get("concepts", lesson.get("concepts", [])),
                    "sources_used": content_result.get("sources_used", []),
                    "reference_kb": bundle.get("reference_kb", ""),
                    "image_metadata": bundle.get("image_metadata", []),
                }
                wiki_meta = bundle.get("wiki_meta") or {}
                yt_id = content_result.get("youtube_id") or wiki_meta.get("youtube_id")
                yt_title = content_result.get("video_title") or wiki_meta.get("video_title")
                if yt_id:
                    out["youtube_id"] = yt_id
                if yt_title:
                    out["video_title"] = yt_title
                return out
            except Exception as e:
                logger.warning("Bundle gen failed for %r, falling back: %s", title, e)

        # Fallback: notes only (no wiki context available)
        if reference_kb and reference_kb.get(slug, ""):
            prompt = CONTENT_FROM_KB_PROMPT.format(
                title=title,
                summary=lesson.get("summary", ""),
                concepts=", ".join(lesson_concepts),
                reference_kb=reference_kb[slug][:12000],
            )
        else:
            transcript_section = ""
            if source_type == "transcript" and source_text:
                transcript_section = (
                    "Use the following transcript as the primary source:\n\n"
                    f"TRANSCRIPT:\n{source_text[:8000]}"
                )
            prompt = CONTENT_GENERATION_PROMPT.format(
                title=title,
                summary=lesson.get("summary", ""),
                concepts=", ".join(lesson.get("concepts", [])),
                transcript_section=transcript_section,
            )

        last_error = None
        for attempt in range(2):
            try:
                result = await _call_llm_json(prompt)
                return {
                    "idx": idx, "status": "done",
                    "title": title, "slug": slug,
                    "content": result.get("content", ""),
                    "summary": result.get("summary", lesson.get("summary", "")),
                    "concepts": result.get("concepts", lesson.get("concepts", [])),
                    "sources_used": result.get("sources_used", []),
                }
            except Exception as e:
                last_error = e
                if attempt == 0:
                    logger.warning("Retry content gen for %r: %s", title, e)
                    await asyncio.sleep(2)
        return {
            "idx": idx, "status": "error",
            "title": title, "slug": slug,
            "error": str(last_error),
        }

    for idx, les in to_generate:
        yield _sse({
            "type": "progress",
            "lesson_title": les.get("title", "Untitled"),
            "index": idx,
            "total": total_lessons,
            "status": "generating",
        })

    futures = [
        asyncio.ensure_future(_generate_one(idx, les))
        for idx, les in to_generate
    ]

    completed = 0
    for coro in asyncio.as_completed(futures):
        result = await coro
        completed += 1
        idx = result["idx"]
        title = result["title"]
        slug = result["slug"]

        if result["status"] == "done":
            lesson_out = {
                "title": title,
                "slug": slug,
                "content": result["content"],
                "summary": result["summary"],
                "concepts": result["concepts"],
                "sources_used": result.get("sources_used", []),
            }
            if result.get("reference_kb"):
                lesson_out["reference_kb"] = result["reference_kb"]
            if result.get("youtube_id"):
                lesson_out["youtube_id"] = result["youtube_id"]
            if result.get("video_title"):
                lesson_out["video_title"] = result["video_title"]
            yield _sse({
                "type": "progress",
                "lesson_title": title,
                "index": idx,
                "total": total_lessons,
                "status": "done",
                "word_count": len(result["content"].split()),
                "has_reference_kb": bool(result.get("reference_kb")),
                "lesson": lesson_out,
            })
        else:
            yield _sse({
                "type": "progress",
                "lesson_title": title,
                "index": idx,
                "total": total_lessons,
                "status": "error",
                "error": result.get("error", "unknown"),
            })

    yield _sse({"type": "content", "data": outline})
    yield _sse({"type": "done"})


# ---------------------------------------------------------------------------
# Unified lesson bundle: student notes + tutor KB in one shot
# ---------------------------------------------------------------------------

async def generate_lesson_bundle(
    lesson: dict,
    wiki_ctx: dict,
    *,
    reference_ctx: dict | None = None,
    course_profile: dict | None = None,
) -> dict:
    """Generate both student-facing content and tutor reference KB in parallel.

    Takes a pre-loaded ``wiki_ctx`` (pedagogy track, from
    ``load_wiki_context``) and optionally a ``reference_ctx`` (reference
    track, from ``load_wiki_context(track="reference")``).

    When reference sources are available, the KB prompt gets blended
    context: reference sources first (14k chars), then pedagogy sources
    for teaching context (6k chars).  Student notes always use pedagogy
    sources only (unchanged).

    Returns::

        {
            "content": {...},       # student-facing lesson (same shape as generate_content output)
            "reference_kb": str,    # tutor's reference KB markdown
            "wiki_meta": {...},     # youtube_id, video_title, reading
        }
    """
    title = lesson.get("title", "Untitled")
    slug = lesson.get("slug", "")
    concepts = lesson.get("concepts", [])
    summary = lesson.get("summary", "")

    wiki_meta = _build_wiki_metadata(wiki_ctx)

    # --- Student notes: pedagogy-first, reference fallback when thin ---
    _MIN_NOTES_SOURCES = 3
    _MIN_NOTES_CHARS = 8000

    content_source_files = sum(len(v) for v in wiki_ctx.get("source_content", {}).values())
    pedagogy_thin = content_source_files < _MIN_NOTES_SOURCES

    if pedagogy_thin and reference_ctx and reference_ctx.get("source_content"):
        ped_text = _build_wiki_source_context(
            wiki_ctx, concepts, max_words=7500, course_profile=course_profile)
        ref_text = _build_wiki_source_context(
            reference_ctx, concepts, max_words=7500, course_profile=course_profile)
        content_source_text = (
            ped_text
            + "\n\n--- ADDITIONAL REFERENCE SOURCES ---\n\n"
            + ref_text
        )
        ref_file_count = sum(len(v) for v in reference_ctx.get("source_content", {}).values())
        content_source_files += ref_file_count
        logger.info(
            "Thin pedagogy (%d sources) for %r — blending %d reference sources into notes",
            content_source_files - ref_file_count, title, ref_file_count,
        )
    else:
        content_source_text = _build_wiki_source_context(
            wiki_ctx, concepts, max_words=15000, course_profile=course_profile)

    resource_excerpt_parts = []
    for t in wiki_ctx.get("topics", [])[:2]:
        page = wiki_ctx.get("resource_pages", {}).get(t, "")
        resource_excerpt_parts.append(page[:2000])
    resource_excerpt = "\n---\n".join(resource_excerpt_parts)

    lesson_images = select_lesson_images(wiki_ctx, concepts)
    image_ctx = _build_image_context(wiki_ctx, concepts)

    content_prompt = CONTENT_FROM_WIKI_PROMPT.format(
        title=title,
        summary=summary,
        concepts=", ".join(concepts),
        course_profile=_format_course_profile(course_profile),
        source_count=content_source_files,
        wiki_source_context=content_source_text,
        resource_page_excerpt=resource_excerpt[:1500],
        image_context=image_ctx,
    )

    # --- KB: blend reference + pedagogy when reference sources exist ---
    has_reference = (
        reference_ctx is not None
        and bool(reference_ctx.get("source_content"))
    )
    if has_reference:
        ref_text = _build_wiki_source_context(
            reference_ctx, concepts, max_words=10000, course_profile=course_profile)
        ped_text = _build_wiki_source_context(
            wiki_ctx, concepts, max_words=5000, course_profile=course_profile)
        kb_source_text = (
            ref_text
            + "\n\n--- PEDAGOGY CONTEXT (teaching sources) ---\n\n"
            + ped_text
        )
        kb_source_files = (
            sum(len(v) for v in reference_ctx.get("source_content", {}).values())
            + content_source_files
        )
    else:
        kb_source_text = _build_wiki_source_context(
            wiki_ctx, concepts, max_words=15000, course_profile=course_profile)
        kb_source_files = content_source_files

    kb_resource_summary = _build_resource_summary(wiki_ctx)

    # Load ramps from reference track if available
    ramps_text = ""
    if has_reference:
        ramps_text = _load_reference_ramps(wiki_ctx.get("topics", []))

    kb_prompt = REFERENCE_KB_FROM_WIKI_PROMPT.format(
        title=title,
        summary=summary,
        concepts=", ".join(concepts),
        course_profile=_format_course_profile(course_profile),
        source_count=kb_source_files,
        wiki_source_context=kb_source_text,
        resource_page_excerpt=resource_excerpt,
        image_context=image_ctx,
        resource_summary=kb_resource_summary + ramps_text,
    )

    async def _gen_content() -> dict:
        last_error = None
        for attempt in range(2):
            try:
                result = await _call_llm_json(content_prompt)
                out = {
                    "title": title, "slug": slug,
                    "content": result.get("content", ""),
                    "summary": result.get("summary", summary),
                    "concepts": result.get("concepts", concepts),
                    "sources_used": result.get("sources_used", []),
                }
                yt_id = result.get("youtube_id")
                yt_title = result.get("video_title")
                if wiki_meta:
                    if not yt_id and wiki_meta.get("youtube_id"):
                        yt_id = wiki_meta["youtube_id"]
                    if not yt_title and wiki_meta.get("video_title"):
                        yt_title = wiki_meta["video_title"]
                if yt_id:
                    out["youtube_id"] = yt_id
                if yt_title:
                    out["video_title"] = yt_title
                return out
            except Exception as e:
                last_error = e
                if attempt == 0:
                    logger.warning("Retry content gen for %r: %s", title, e)
                    await asyncio.sleep(2)
        return {"title": title, "slug": slug, "content": "", "error": str(last_error)}

    async def _gen_kb() -> str:
        last_error = None
        for attempt in range(2):
            try:
                return await _call_llm(kb_prompt, max_tokens=8192)
            except Exception as e:
                last_error = e
                if attempt == 0:
                    logger.warning(
                        "Retry wiki KB for %r: %s: %s",
                        title, type(e).__name__, repr(e),
                    )
                    await asyncio.sleep(2)
        logger.error("Wiki KB failed for %r: %s", title, repr(last_error))
        return ""

    content_result, kb_markdown = await asyncio.gather(
        _gen_content(), _gen_kb(),
    )

    return {
        "content": content_result,
        "reference_kb": kb_markdown,
        "wiki_meta": wiki_meta,
        "image_metadata": lesson_images,
    }


# ---------------------------------------------------------------------------
# Reference KB from wiki — tutor's primary grounding from curated content
# ---------------------------------------------------------------------------

REFERENCE_KB_FROM_WIKI_PROMPT = """\
You are building a **tutor reference document** — a structured knowledge \
base that an AI Socratic tutor will consult in real time during live \
student conversations. This is NOT a student-facing explainer. It is a \
lookup resource organized around what a tutor NEEDS mid-conversation: \
precise definitions to quote, multiple ways to explain the same concept, \
common student confusions to pre-empt, worked examples to reach for, and \
questions to ask that probe understanding.

LESSON TITLE: {title}
LESSON SUMMARY: {summary}
KEY CONCEPTS: {concepts}

{course_profile}

SOURCE MATERIAL ({source_count} curated resources):
{wiki_source_context}

WIKI RESOURCE NOTES:
{resource_page_excerpt}

{image_context}

{resource_summary}

ORGANIZE THE DOCUMENT around tutoring tasks. Use these sections — \
include only those that have meaningful content for this lesson:

## Core Definitions
Precise, quotable definitions for every key concept. One paragraph per \
concept. Written for accuracy — the tutor will quote these directly. \
Attribute to sources: "Vaswani et al. define...", "As Weng explains...".

## Key Formulas & Empirical Results
Only include if the source material contains equations, benchmark numbers, \
or specific implementation defaults. For each: write the formula or result, \
identify what the variables mean, and note the specific claim it supports. \
Also include important default hyperparameters (e.g. "TRL PPOConfig defaults: \
`kl_coef=0.05`, `cliprange=0.2`") — students ask about these constantly. \
If the source material has no formulas or numbers, skip this section. \
Do NOT fabricate formulas not present in the sources.

## How It Works
Step-by-step mechanical breakdown. What actually happens, in sequence. \
Use numbered steps for processes, code snippets for algorithms. Dense \
and exact — this is what the tutor reaches for when a student asks \
"walk me through how this actually works."

## Teaching Approaches
2-3 distinct ways to explain the same core idea at different levels. \
Label them: **Intuitive (no math)**, **Technical (with math)**, \
**Analogy-based**. The tutor picks whichever fits the student's level.

## Common Misconceptions
**This section is required — do not skip it.** Write 3-5 specific \
misconceptions students hold about this topic. For EACH: (1) state the \
wrong belief as a student would hold it ("I thought X..."), (2) explain \
exactly why it is wrong, (3) give the correct mental model. Be concrete — \
name the specific concept that breaks the wrong belief. Vague entries like \
"students may misunderstand complexity" do not count.

## Worked Examples
Concrete, runnable examples. Code where relevant. Step through at least \
one example completely. These are what the tutor uses when a student says \
"can you show me?"

## Comparisons & Trade-offs
Only include if the lesson has natural comparisons (e.g. BPE vs WordPiece, \
self-attention vs cross-attention, Adam vs SGD). Use a markdown table. \
Add a paragraph on when to choose each.

## Prerequisite Connections
What prior concepts does a student need to understand this lesson well? \
List 2-4 prerequisite ideas and one sentence explaining the dependency. \
Useful when the tutor needs to backtrack with a struggling student.

## Socratic Question Bank
6-8 questions the tutor can ask to probe whether the student truly \
understands — not recall questions, but questions that surface \
misconceptions or require applying the concept. Include a brief note \
on what a good answer looks like.

## Likely Student Questions
5-8 specific factual questions a student is LIKELY TO ASK mid-conversation, \
paired with precise, sourced answers the tutor can use immediately. These \
are not for testing the student — they are a lookup table for the tutor. \
Format: **Q: [question]** → **A: [precise answer with key numbers/names \
grounded in the source material].** Prioritize questions about specific \
formulas, numbers, comparisons, or "why" questions that require more than \
a definition (e.g. "What's the actual loss function?", "Why rankings instead \
of scores?", "How does X differ from Y in practice?").

## Available Resources
Only include if AVAILABLE VIDEOS or AVAILABLE ARTICLES are listed above. \
For each resource, write one line: the title as a link, then a \
"Surface when:" note — the specific student question or moment that makes \
this resource worth pointing to. Group into ### Videos and \
### Articles & Tutorials subsections. This is the tutor's catalog: \
it should know these exist and when to reach for them.

## Visual Aids
Only include if AVAILABLE EDUCATIONAL IMAGES are listed above. For each \
relevant image: `![caption](path)` followed by a "Show when:" note \
telling the tutor exactly which student question this image answers best.

## Key Sources
2-5 most authoritative references used. Format: [Title](url) — one line \
on why this source matters for this topic.

RULES:
1. Every factual claim must be grounded in the source material above.
2. DO NOT fabricate URLs — only use URLs from the source material.
3. DO NOT fabricate image paths — only use images from AVAILABLE EDUCATIONAL IMAGES.
4. No padding, no generic introductions, no "in this document we will cover..."
5. Target 2000-3500 words total. Dense is good — this is a reference, not an essay.
6. Skip any section that would be thin or forced for this particular lesson.
7. When source material contains formulas, benchmarks, or specific defaults — \
   include them. Precision is a feature, not a distraction.

Write the Markdown document now. No preamble — start with the first ## header.
"""


async def generate_reference_kb_from_wiki(
    lessons: list[dict],
    *,
    existing_kb: dict[str, str] | None = None,
    course_profile: dict | None = None,
) -> AsyncGenerator[str, None]:
    """Generate reference KB for each lesson from wiki downloads.

    For each lesson, loads wiki context for the lesson's concepts, then uses
    the downloaded blog posts / transcripts / papers as source material for
    a structured reference document.

    Yields SSE events per lesson, then final
    ``{"type": "reference_kb", "data": {slug: md}, "wiki_gaps": [...]}``.
    """
    existing_kb = existing_kb or {}
    total = len(lessons)

    yield _sse({
        "type": "status",
        "step": "wiki_reference_kb",
        "message": f"Generating reference KB from wiki for {total} lessons...",
    })

    wiki_gaps: list[dict] = []

    async def _synth_one(idx: int, lesson: dict) -> tuple[int, str, str, str, dict | None]:
        title = lesson.get("title", "Untitled")
        slug = lesson.get("slug", "")
        concepts = lesson.get("concepts", [])

        if slug in existing_kb and len(existing_kb[slug].split()) > 500:
            return idx, slug, title, existing_kb[slug], None

        resolved = await resolve_topics_llm(
            concepts, lesson_title=title,
            lesson_summary=lesson.get("summary", ""),
        )
        wiki_ctx = load_wiki_context(concepts, topic_slugs=resolved["topic_slugs"])
        if not wiki_ctx.get("source_content"):
            gap = {
                "lesson_title": title,
                "lesson_slug": slug,
                "concepts": concepts,
                "reason": "No wiki downloads found for any lesson concept",
            }
            return idx, slug, title, "", gap

        # Load reference track sources if available
        ref_ctx = load_wiki_context(
            concepts, topic_slugs=resolved["topic_slugs"], track="reference",
        )
        has_reference = bool(ref_ctx.get("source_content"))

        if has_reference:
            ref_text = _build_wiki_source_context(
                ref_ctx, concepts, max_words=10000, course_profile=course_profile)
            ped_text = _build_wiki_source_context(
                wiki_ctx, concepts, max_words=5000, course_profile=course_profile)
            wiki_source_text = (
                ref_text
                + "\n\n--- PEDAGOGY CONTEXT (teaching sources) ---\n\n"
                + ped_text
            )
            source_files = (
                sum(len(v) for v in ref_ctx.get("source_content", {}).values())
                + sum(len(v) for v in wiki_ctx.get("source_content", {}).values())
            )
        else:
            wiki_source_text = _build_wiki_source_context(
                wiki_ctx, concepts, max_words=15000,
                course_profile=course_profile,
            )
            source_files = sum(
                len(v) for v in wiki_ctx.get("source_content", {}).values()
            )

        if source_files == 0 or len(wiki_source_text.split()) < 200:
            gap = {
                "lesson_title": title,
                "lesson_slug": slug,
                "concepts": concepts,
                "topics_found": wiki_ctx.get("topics", []),
                "reason": "Wiki content too thin for reference KB",
            }
            return idx, slug, title, "", gap

        resource_excerpt_parts = []
        for t in wiki_ctx.get("topics", [])[:2]:
            page = wiki_ctx.get("resource_pages", {}).get(t, "")
            resource_excerpt_parts.append(page[:2000])
        resource_excerpt = "\n---\n".join(resource_excerpt_parts)

        kb_image_ctx = _build_image_context(wiki_ctx, concepts)
        kb_resource_summary = _build_resource_summary(wiki_ctx)
        ramps_text = _load_reference_ramps(wiki_ctx.get("topics", [])) if has_reference else ""
        prompt = REFERENCE_KB_FROM_WIKI_PROMPT.format(
            title=title,
            summary=lesson.get("summary", ""),
            concepts=", ".join(concepts),
            course_profile=_format_course_profile(course_profile),
            source_count=source_files,
            wiki_source_context=wiki_source_text,
            resource_page_excerpt=resource_excerpt,
            image_context=kb_image_ctx,
            resource_summary=kb_resource_summary + ramps_text,
        )

        last_error: Exception | None = None
        for attempt in range(3):
            try:
                markdown = await _call_llm(prompt, max_tokens=8192)
                if markdown and len(markdown.split()) >= 50:
                    return idx, slug, title, markdown, None
                logger.warning(
                    "Wiki KB synthesis for %r returned only %d words (attempt %d/3), retrying",
                    title, len((markdown or "").split()), attempt + 1,
                )
            except Exception as e:
                last_error = e
                logger.warning(
                    "Retry wiki KB synthesis for %r: %s: %s",
                    title, type(e).__name__, repr(e),
                )
            await asyncio.sleep(2)
        reason = (f"LLM error ({type(last_error).__name__}): {repr(last_error)}"
                  if last_error else "LLM returned empty/short content after 3 attempts")
        logger.error("Wiki KB synthesis failed for %r after 3 attempts: %s", title, reason)
        return idx, slug, title, "", {
            "lesson_title": title,
            "lesson_slug": slug,
            "concepts": concepts,
            "reason": reason,
        }

    futures = [
        asyncio.ensure_future(_synth_one(i, les))
        for i, les in enumerate(lessons)
    ]

    all_kb: dict[str, str] = {}
    completed = 0
    for coro in asyncio.as_completed(futures):
        idx, slug, title, markdown, gap = await coro
        completed += 1
        if gap:
            wiki_gaps.append(gap)
        if markdown:
            all_kb[slug] = markdown

        word_count = len(markdown.split()) if markdown else 0
        yield _sse({
            "type": "progress",
            "step": "wiki_reference_kb",
            "lesson_title": title,
            "lesson_slug": slug,
            "index": completed,
            "total": total,
            "status": "done" if markdown else "gap",
            "word_count": word_count,
        })

    total_words = sum(len(md.split()) for md in all_kb.values())
    yield _sse({
        "type": "wiki_kb_complete",
        "total_lessons": len(all_kb),
        "total_words": total_words,
        "gaps": wiki_gaps,
    })
    yield _sse({"type": "reference_kb", "data": all_kb, "wiki_gaps": wiki_gaps})
    yield _sse({"type": "done"})


# ---------------------------------------------------------------------------
# Wiki enrichment suggestions — recommend new content for the wiki
# ---------------------------------------------------------------------------


def suggest_wiki_enrichment(
    lessons: list[dict],
    existing_kb: dict[str, str] | None = None,
) -> list[dict]:
    """Identify gaps where the wiki should be enriched with new content.

    Analyzes each lesson's concepts against wiki coverage and returns
    specific suggestions for articles, videos, or papers to add.
    """
    existing_kb = existing_kb or {}
    suggestions: list[dict] = []

    for lesson in lessons:
        title = lesson.get("title", "Untitled")
        slug = lesson.get("slug", "")
        concepts = lesson.get("concepts", [])

        wiki_ctx = load_wiki_context(concepts)
        topics_found = wiki_ctx.get("topics", [])
        source_count = sum(
            len(v) for v in wiki_ctx.get("source_content", {}).values()
        )
        kb_words = len(existing_kb.get(slug, "").split())

        if source_count == 0:
            suggestions.append({
                "lesson_title": title,
                "lesson_slug": slug,
                "severity": "high",
                "concepts": concepts,
                "topics_found": topics_found,
                "suggestion": (
                    f"No wiki downloads cover this lesson's concepts. "
                    f"Consider adding topic pages and downloading key "
                    f"resources for: {', '.join(concepts[:5])}"
                ),
                "recommended_actions": [
                    f"Add concept-map entries for: {', '.join(concepts[:5])}",
                    f"Create wiki topic page if none exists",
                    f"Download 3-5 canonical blog posts or papers",
                    f"Fetch YouTube transcripts for key explainer videos",
                ],
            })
        elif source_count < 3 or kb_words < 800:
            suggestions.append({
                "lesson_title": title,
                "lesson_slug": slug,
                "severity": "medium",
                "concepts": concepts,
                "topics_found": topics_found,
                "source_count": source_count,
                "kb_words": kb_words,
                "suggestion": (
                    f"Wiki has thin coverage ({source_count} files). "
                    f"Consider adding more sources for richer tutor grounding."
                ),
                "recommended_actions": [
                    f"Add 2-3 more blog posts or tutorials to: {', '.join(topics_found)}",
                    f"Check for missing YouTube transcripts",
                ],
            })

    return suggestions


# ---------------------------------------------------------------------------
# Phase 2: Terminology cleanup
# ---------------------------------------------------------------------------

CLEANUP_PROMPT = """\
You are a technical editor. Review the following lesson content and fix:

1. **Terminology consistency** — ensure product names, tool names, and \
technical terms are spelled correctly and consistently throughout.
2. **Quality** — tighten prose, fix awkward phrasing, ensure bullet points \
are parallel in structure.
3. **Formatting** — ensure Markdown is well-formed, headings are consistent, \
bold/backtick usage follows conventions.

{domain_terms_section}

Preserve the overall structure and length (600-1000 words). Do not add \
information not present in the original.

Return a JSON object with:
- "content": the cleaned content
- "summary": the cleaned summary
- "concepts": the cleaned concepts array
- "changes": array of strings describing each change made

Return ONLY valid JSON.

LESSON TITLE: {title}
ORIGINAL CONTENT:
{content}

ORIGINAL SUMMARY: {summary}
ORIGINAL CONCEPTS: {concepts}
"""


async def run_cleanup(lessons: list, domain_terms: str = "") -> AsyncGenerator[str, None]:
    """Run terminology cleanup on each lesson. Yields SSE events."""
    total = len(lessons)
    domain_section = ""
    if domain_terms:
        domain_section = f"Pay special attention to these domain-specific terms:\n{domain_terms}\n"

    for i, lesson in enumerate(lessons):
        title = lesson.get("title", "Untitled")
        content = lesson.get("content", "")
        if not content.strip():
            yield _sse({
                "type": "progress",
                "lesson_title": title,
                "index": i + 1,
                "total": total,
                "status": "skipped",
            })
            continue

        yield _sse({
            "type": "progress",
            "lesson_title": title,
            "index": i + 1,
            "total": total,
            "status": "cleaning",
        })

        prompt = CLEANUP_PROMPT.format(
            title=title,
            content=content,
            summary=lesson.get("summary", ""),
            concepts=json.dumps(lesson.get("concepts", [])),
            domain_terms_section=domain_section,
        )

        try:
            result = await _call_llm_json(prompt, max_tokens=8192)
            lesson["content_before"] = content
            lesson["content"] = result.get("content", content)
            lesson["summary"] = result.get("summary", lesson.get("summary", ""))
            lesson["concepts"] = result.get("concepts", lesson.get("concepts", []))
            lesson["cleanup_changes"] = result.get("changes", [])
            yield _sse({
                "type": "progress",
                "lesson_title": title,
                "index": i + 1,
                "total": total,
                "status": "done",
                "changes": len(lesson["cleanup_changes"]),
            })
        except Exception as e:
            yield _sse({
                "type": "progress",
                "lesson_title": title,
                "index": i + 1,
                "total": total,
                "status": "error",
                "error": str(e),
            })

    yield _sse({"type": "cleanup", "data": lessons})
    yield _sse({"type": "done"})


# ---------------------------------------------------------------------------
# Quality gate
# ---------------------------------------------------------------------------

def evaluate_quality_gate(lessons: list) -> dict:
    """Evaluate lessons against the handoff contract."""
    results = []
    all_pass = True
    for lesson in lessons:
        content = lesson.get("content", "")
        concepts = lesson.get("concepts", [])
        summary = lesson.get("summary", "")
        word_count = len(content.split())
        checks = {
            "word_count": word_count,
            "content_ok": word_count >= 100,
            "content_target": 400 <= word_count <= 1200,
            "has_concepts": len(concepts) > 0,
            "concept_count": len(concepts),
            "concept_target": 4 <= len(concepts) <= 8,
            "has_summary": len(summary.strip()) > 0,
        }
        passes = checks["content_ok"] and checks["has_concepts"] and checks["has_summary"]
        if not passes:
            all_pass = False
        results.append({
            "title": lesson.get("title", ""),
            "slug": lesson.get("slug", ""),
            "passes": passes,
            **checks,
        })
    return {"lessons": results, "all_pass": all_pass, "total": len(results)}


# ---------------------------------------------------------------------------
# SSE helper
# ---------------------------------------------------------------------------

def _sse(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"
