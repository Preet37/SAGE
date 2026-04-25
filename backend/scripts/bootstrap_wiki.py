"""
Bootstrap & maintain the Pedagogy Wiki — Educator Registry + Resource Index.

Phases:
  A: Extract from existing courses (no LLM, no search)
  B: LLM-generated educator profiles + resource curation
  C: Web search verification of flagged URLs
  D: Pedagogical gap-filling via discovery search
  E: Download source content (blogs, transcripts)

Usage (from backend/):
  # Full bootstrap (Phases A + B + C):
  uv run python scripts/bootstrap_wiki.py

  # Phase A only:
  uv run python scripts/bootstrap_wiki.py --phase-a

  # Verify + discover on existing wiki:
  uv run python scripts/bootstrap_wiki.py --verify-only --discover

  # Download all source content:
  uv run python scripts/bootstrap_wiki.py --download

  # Scope to specific topics:
  uv run python scripts/bootstrap_wiki.py --download --topic attention-mechanism,tokenization

  # Re-verify stale pages (last verified > 30 days ago):
  uv run python scripts/bootstrap_wiki.py --stale-days 30 --verify-only --discover

  # Manually file a source:
  uv run python scripts/bootstrap_wiki.py --file-source attention-mechanism https://example.com "Blog Title"

  # Generate/update concept map:
  uv run python scripts/bootstrap_wiki.py --concept-map

  # Align resource pages with concept map:
  uv run python scripts/bootstrap_wiki.py --consolidate
"""

import asyncio
import json
import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import httpx

from app.config import get_settings
from app.services.wiki_authors import (
    resolve_author, get_name_index,
    is_venue, parse_arxiv_id, extract_arxiv_authors, format_paper_authors,
    extract_author_from_html,
)

_BACKEND_DIR = Path(__file__).resolve().parent.parent
_CONTENT_DIR = Path(os.environ.get("CONTENT_DIR", str(_BACKEND_DIR.parent / "content"))).resolve()
_WIKI_DIR = _CONTENT_DIR / "pedagogy-wiki"
_CACHE_PATH = Path(__file__).parent / ".wiki_bootstrap_cache.json"

_http_client: httpx.AsyncClient | None = None
_llm_semaphore = asyncio.Semaphore(5)


def _get_http_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(
            timeout=300.0,
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
        )
    return _http_client


# ---------------------------------------------------------------------------
# LLM + Search helpers (mirrors course_enricher.py patterns)
# ---------------------------------------------------------------------------

async def _call_llm(prompt: str, *, max_tokens: int = 4096, temperature: float = 0.3) -> str:
    settings = get_settings()
    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.llm_model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    async with _llm_semaphore:
        t0 = time.monotonic()
        client = _get_http_client()
        resp = await client.post(
            f"{settings.llm_base_url}/v1/chat/completions",
            headers=headers,
            json=payload,
        )
        if resp.status_code != 200:
            print(f"  LLM error {resp.status_code}: {resp.text[:300]}")
        resp.raise_for_status()
        elapsed = time.monotonic() - t0
    content = resp.json()["choices"][0]["message"]["content"].strip()
    print(f"  LLM call: {elapsed:.1f}s | ~{len(prompt)} prompt chars | ~{len(content)} response chars")
    return content


async def _search(query: str) -> dict:
    settings = get_settings()
    has_dedicated = bool(
        settings.search_api_key
        and settings.search_base_url
        and settings.search_api_key != settings.llm_api_key
    )
    headers = {
        "Content-Type": "application/json",
    }
    if has_dedicated:
        headers["Authorization"] = f"Bearer {settings.search_api_key}"
        payload = {
            "model": "sonar",
            "messages": [{"role": "user", "content": query}],
        }
        url = f"{settings.search_base_url}/chat/completions"
    else:
        headers["Authorization"] = f"Bearer {settings.llm_api_key}"
        payload = {"query": query, "max_results": 5}
        url = f"{settings.llm_base_url}/v1/search/perplexity-search"

    try:
        client = _get_http_client()
        resp = await client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()

        if has_dedicated:
            content = data["choices"][0]["message"]["content"]
            citations = data.get("citations", [])
        else:
            results = data.get("results", [])
            content = "\n\n".join(
                r.get("snippet", r.get("content", r.get("text", "")))
                for r in results if r.get("snippet") or r.get("content") or r.get("text")
            )
            citations = [
                {"title": r.get("title", ""), "url": r.get("url", r.get("link", ""))}
                for r in results if r.get("url") or r.get("link")
            ]

        return {"query": query, "content": content[:15000], "citations": citations}
    except Exception as e:
        return {"query": query, "content": "", "citations": [], "error": str(e)}


# ═══════════════════════════════════════════════════════════════════════════
# Phase A: Extract from existing courses
# ═══════════════════════════════════════════════════════════════════════════

_URL_PATTERN = re.compile(r'https?://[^\s\)>\]"\']+')

def _resolve_educator_from_domain(domain: str) -> str | None:
    """Resolve a bare domain to an educator name via the author registry."""
    if domain in ("youtube.com",):
        return None
    entry = resolve_author(f"https://{domain}/")
    return entry.get("name") if entry else None


def _slugify(text: str) -> str:
    slug = text.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")[:80]


def _domain(url: str) -> str:
    try:
        return urlparse(url).netloc.replace("www.", "")
    except Exception:
        return ""


def phase_a() -> dict:
    """Extract structured data from existing courses. No LLM, no search."""
    print("\n" + "=" * 60)
    print("PHASE A: Extracting from existing courses")
    print("=" * 60)

    concept_freq: dict[str, set[str]] = defaultdict(set)
    concept_to_lessons: dict[str, list[dict]] = defaultdict(list)
    video_resources: list[dict] = []
    enrichment_urls: dict[str, list[dict]] = defaultdict(list)
    educator_mentions: dict[str, set[str]] = defaultdict(set)

    course_files = sorted(_CONTENT_DIR.glob("*/course.json"))
    course_files = [f for f in course_files if not f.parent.name.startswith("private-")]

    for course_file in course_files:
        course_slug = course_file.parent.name
        with open(course_file) as f:
            course = json.load(f)

        print(f"\n  Scanning: {course['title']} ({course_slug})")

        for mod in course.get("modules", []):
            for lesson in mod.get("lessons", []):
                lesson_slug = lesson.get("slug", "")
                concepts = lesson.get("concepts", [])

                for concept in concepts:
                    c_lower = concept.lower().strip()
                    concept_freq[c_lower].add(course_slug)
                    concept_to_lessons[c_lower].append({
                        "course": course_slug,
                        "lesson_slug": lesson_slug,
                        "lesson_title": lesson.get("title", ""),
                    })

                if lesson.get("youtube_id"):
                    video_resources.append({
                        "youtube_id": lesson["youtube_id"],
                        "video_title": lesson.get("video_title", ""),
                        "lesson_slug": lesson_slug,
                        "course": course_slug,
                        "concepts": concepts,
                    })

                content = lesson.get("content", "")
                name_idx = get_name_index()
                for name_lower, canonical in name_idx.items():
                    if name_lower in content.lower():
                        educator_mentions[canonical].add(course_slug)

        enrichment_dir = course_file.parent / "enrichment"
        if enrichment_dir.exists():
            for kb_file in enrichment_dir.glob("*_reference_kb.md"):
                lesson_slug = kb_file.stem.replace("_reference_kb", "")
                kb_text = kb_file.read_text()

                urls = _URL_PATTERN.findall(kb_text)
                for url in urls:
                    url = url.rstrip(".,;:")
                    domain = _domain(url)
                    educator = _resolve_educator_from_domain(domain)

                    enrichment_urls[lesson_slug].append({
                        "url": url,
                        "domain": domain,
                        "educator": educator,
                        "course": course_slug,
                    })

                    if educator:
                        educator_mentions[educator].add(course_slug)

                for name_lower, canonical in name_idx.items():
                    if name_lower in kb_text.lower():
                        educator_mentions[canonical].add(course_slug)

    concept_topics = []
    for concept, courses in sorted(concept_freq.items(), key=lambda x: -len(x[1])):
        concept_topics.append({
            "concept": concept,
            "courses": sorted(courses),
            "cross_course_count": len(courses),
            "lessons": concept_to_lessons[concept],
        })

    url_freq: dict[str, int] = defaultdict(int)
    for lesson_urls in enrichment_urls.values():
        seen_in_lesson: set[str] = set()
        for u in lesson_urls:
            base = u["url"].split("?")[0].split("#")[0]
            if base not in seen_in_lesson:
                url_freq[base] += 1
                seen_in_lesson.add(base)

    top_urls = sorted(url_freq.items(), key=lambda x: -x[1])[:50]

    result = {
        "concept_topics": concept_topics,
        "video_resources": video_resources,
        "enrichment_urls": {k: v for k, v in enrichment_urls.items()},
        "educator_mentions": {k: sorted(v) for k, v in educator_mentions.items()},
        "top_urls": top_urls,
    }

    print(f"\n  Results:")
    print(f"    Concepts: {len(concept_topics)} unique")
    print(f"    Videos: {len(video_resources)} curated YouTube links")
    print(f"    Educators detected: {len(educator_mentions)}")
    for name, courses in sorted(educator_mentions.items()):
        print(f"      {name}: mentioned in {courses}")
    print(f"    Top URLs by frequency: {len(top_urls)}")

    return result


# ═══════════════════════════════════════════════════════════════════════════
# Phase B: LLM-generated educator profiles + resource curation
# ═══════════════════════════════════════════════════════════════════════════

EDUCATOR_PROFILE_PROMPT = """\
You are building a teaching resource registry for an AI/ML learning platform.
Write a detailed profile for the educator/content creator: {name}

CONTEXT — this educator was found referenced in these courses: {courses}

Cover the following in your profile:
1. Teaching style (visual, code-first, mathematical, narrative, etc.)
2. Best topics they cover (be specific — not just "ML")
3. Topics they do NOT cover well or at all
4. Their best resources — with exact YouTube video IDs (11-char alphanumeric) \
or exact URLs. Only include resources you are HIGHLY confident exist.
5. How they pair with other educators (e.g., "3B1B for intuition → Karpathy \
for code")
6. Appropriate student level (beginner / intermediate / advanced)

Format the profile as markdown with these EXACT section headers:
# {name}

## Style
## Best For
## Not Good For
## Canonical Resources
## Pairs Well With
## Level
## Last Verified

For Canonical Resources, use this format for each:
- Topic description: youtube_id=XXXXXXXXXXX  (for videos)
- Topic description: url=https://...         (for articles/blogs)

CRITICAL: Only include YouTube IDs and URLs you are highly confident exist. \
Flag any you are uncertain about with [VERIFY] at the end of the line.
Use today's date ({today}) for Last Verified.
"""

RESOURCE_CURATION_PROMPT = """\
You are curating the best teaching resources for an AI/ML learning platform.

Topic: {topic}
Related concepts: {related_concepts}
Courses that cover this topic: {courses}

{existing_data}

From your knowledge of the AI/ML education ecosystem, identify the SINGLE \
BEST resource of each type for teaching this topic:

1. **Video** — the best YouTube explainer. Provide the exact 11-character \
video ID. Prefer: 3Blue1Brown, Andrej Karpathy, Yannic Kilcher, StatQuest, \
Serrano.Academy, Stanford/MIT lectures.

2. **Blog / Written explainer** — the best article or blog post. Provide \
the exact URL. Prefer: Jay Alammar, Lilian Weng, Christopher Olah, \
Chip Huyen, Sebastian Raschka, distill.pub.

3. **Deep dive** — the most comprehensive technical reference. Exact URL.

4. **Original paper** — the most readable seminal paper (arxiv URL if \
applicable). Only if one clearly exists for this topic.

5. **Code walkthrough** — the best hands-on implementation. URL or YouTube ID.

For each resource, explain briefly WHY it's the best for this topic \
(pedagogical reason, not just popularity).

Note any coverage gaps: "No excellent video exists for this specific topic."

Format as markdown:
# {topic_title}

## Video (best)
- **Educator** — "Video title"
- youtube_id: XXXXXXXXXXX
- Why: ...
- Level: beginner/intermediate/advanced

## Blog / Written explainer (best)
- **Author** — "Article title"
- url: https://...
- Why: ...
- Level: ...

## Deep dive
...

## Original paper
...

## Code walkthrough
...

## Coverage notes
- Strong: ...
- Weak: ...
- Gap: ...

{cross_validation}

## Last Verified
{today}

CRITICAL RULES:
- Only include resources you are genuinely confident exist.
- Flag uncertain URLs/IDs with [VERIFY] at the end of the line.
- If no good resource exists for a category, write "None identified" \
instead of guessing.
- Do NOT invent or hallucinate URLs.
"""


def _build_topic_title(concept: str) -> str:
    """Convert a concept slug to a human-readable title."""
    words = concept.replace("-", " ").replace("_", " ").split()
    stop_words = {"and", "or", "the", "a", "an", "in", "of", "for", "to", "with"}
    return " ".join(
        w.upper() if len(w) <= 3 and w not in stop_words else w.capitalize()
        for w in words
    )


_CONCEPT_MAP_PATH = _WIKI_DIR / "concept-map.md"

def _load_concept_map_fallback() -> dict[str, str]:
    fallback_path = _BACKEND_DIR.parent / "concept_map_fallback.json"
    if fallback_path.exists():
        return json.loads(fallback_path.read_text())
    return {}

_CONCEPT_MAP_FALLBACK = _load_concept_map_fallback()


def _parse_concept_map(path: Path) -> dict[str, str]:
    """Parse concept-map.md into a {concept: topic-slug} dict.

    Supports both formats:
      Three-level: # topic  →  ## subtopic  →  - concept
      Two-level:   ## topic  →  - concept
    Concepts always map to the TOP-LEVEL topic (the resource page).
    """
    merge_map: dict[str, str] = {}
    current_topic = ""

    for line in path.read_text().splitlines():
        stripped = line.strip()

        if stripped.startswith("# ") and not stripped.startswith("# Concept"):
            # Top-level topic (resource page)
            current_topic = _slugify(stripped[2:].strip())
        elif stripped.startswith("## "):
            # Subtopic — concepts under this still map to current_topic
            # (Don't update current_topic; it stays at the # level)
            pass
        elif stripped.startswith("- ") and current_topic:
            concept = stripped[2:].strip().lower()
            if concept and not concept.startswith("[") and not concept.startswith("*"):
                merge_map[concept] = current_topic

    return merge_map


def _load_merge_map() -> dict[str, str]:
    """Load concept→topic mapping from concept-map.md, falling back to hardcoded."""
    if _CONCEPT_MAP_PATH.exists():
        parsed = _parse_concept_map(_CONCEPT_MAP_PATH)
        if parsed:
            return parsed
    return dict(_CONCEPT_MAP_FALLBACK)


CONCEPT_MAP_PROMPT = """\
You are organizing concepts for an AI/ML teaching platform into a \
three-level hierarchy: Topic → Subtopic → Concept.

- **Topic**: Gets ONE resource index page. Should contain 8-20 concepts. \
  Not so broad that one page covers an entire course, not so narrow that \
  it only covers one lesson.
- **Subtopic**: A coherent cluster within a topic (2-5 per topic).
- **Concept**: The atomic unit from course lessons.

Below are {count} unique concepts extracted from {n_courses} courses.

EXISTING TOPICS (these already have resource pages — prefer keeping them \
as topics or subtopics rather than discarding):
{existing_topics}

CONCEPTS (with course counts):
{concepts_list}

RULES:
1. Target 25-35 topics. Each topic should have 8-20 concepts.
2. If a topic would exceed ~20 concepts, split it into multiple topics.
3. If a topic would have fewer than ~5 concepts, merge it into a \
   related topic as a subtopic.
4. Reuse existing topic slugs where possible — these already have \
   resource pages with curated content.
5. Each topic has 2-5 subtopics. Subtopics are kebab-case slugs.
6. Group by PEDAGOGICAL similarity (taught together), not keyword overlap.
7. Every concept must appear exactly once.
8. Use kebab-case slugs for both topics and subtopics.

EXAMPLES of good topic scoping (8-20 concepts each):
- "attention" covering attention-mechanism + self-attention + multi-head \
  (~15 concepts) — good, single page
- "agents" split into "agent-fundamentals" (~10) + "agent-tools" (~10) + \
  "agent-memory" (~10) — NOT crammed into one 30-concept page
- "neural-network-fundamentals" covering architecture + training basics \
  (~16 concepts) — good

Return a JSON object:
{{
  "topic-slug": {{
    "title": "Human Readable Title",
    "subtopics": {{
      "subtopic-slug": ["concept1", "concept2", ...],
      "subtopic-slug-2": ["concept3", "concept4", ...]
    }}
  }},
  ...
}}

Return ONLY valid JSON.
"""


async def generate_concept_map(phase_a_data: dict) -> Path:
    """Use LLM to group concepts into Topic → Subtopic → Concept; write concept-map.md."""
    print("\n" + "=" * 60)
    print("Generating concept map via LLM")
    print("=" * 60)

    concepts = phase_a_data["concept_topics"]
    n_courses = len(set(
        course for c in concepts for course in c["courses"]
    ))

    concepts_text = "\n".join(
        f"- {c['concept']} (in {len(c['courses'])} course(s): {', '.join(c['courses'])})"
        for c in concepts
    )

    # Gather existing topic slugs from resource pages on disk
    existing_dir = _WIKI_DIR / "resources" / "by-topic"
    existing_topics = []
    if existing_dir.exists():
        existing_topics = sorted(
            f.stem for f in existing_dir.glob("*.md")
            if f.name != "_index.md"
        )

    existing_text = "\n".join(f"- {t}" for t in existing_topics) if existing_topics else "(none)"

    prompt = CONCEPT_MAP_PROMPT.format(
        count=len(concepts),
        n_courses=n_courses,
        concepts_list=concepts_text,
        existing_topics=existing_text,
    )

    raw = await _call_llm(prompt, max_tokens=8192, temperature=0.2)

    text = raw.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
    if text.endswith("```"):
        text = text[:-3]

    topic_groups = json.loads(text.strip())

    # Build the markdown
    total_concepts = 0
    total_subtopics = 0
    lines = [
        "# Concept → Topic Map",
        "",
        "Three-level hierarchy: **Topic** (resource page) → "
        "**Subtopic** (section) → **Concept** (atomic unit).",
        "",
        "Edit this file to reorganize topics — the bootstrap script reads it.",
        "",
    ]

    for topic_slug in sorted(topic_groups.keys()):
        topic = topic_groups[topic_slug]
        title = topic.get("title", _build_topic_title(topic_slug))
        subtopics = topic.get("subtopics", {})

        n_concepts = sum(len(cs) for cs in subtopics.values())
        lines.append(f"# {topic_slug}")
        lines.append(f"**{title}** — {len(subtopics)} subtopics, {n_concepts} concepts")
        lines.append("")

        for subtopic_slug in sorted(subtopics.keys()):
            concept_list = subtopics[subtopic_slug]
            lines.append(f"## {subtopic_slug}")
            for concept in sorted(concept_list):
                lines.append(f"- {concept}")
                total_concepts += 1
            lines.append("")
            total_subtopics += 1

    # Add stats at the top
    stats_line = (
        f"*Generated: {time.strftime('%Y-%m-%d %H:%M')} | "
        f"{total_concepts} concepts → {total_subtopics} subtopics → "
        f"{len(topic_groups)} topics*"
    )
    lines.insert(5, stats_line)

    _CONCEPT_MAP_PATH.parent.mkdir(parents=True, exist_ok=True)
    _CONCEPT_MAP_PATH.write_text("\n".join(lines))

    print(f"\n  Topics (resource pages): {len(topic_groups)}")
    print(f"  Subtopics: {total_subtopics}")
    print(f"  Concepts mapped: {total_concepts}/{len(concepts)}")
    print(f"  Written to: {_CONCEPT_MAP_PATH}")

    return _CONCEPT_MAP_PATH


def _group_concepts_into_topics(phase_a_data: dict) -> list[dict]:
    """Group related concepts into resource index topics.

    Reads concept-map.md if it exists; otherwise falls back to
    the hardcoded merge map.
    """
    concepts = phase_a_data["concept_topics"]

    merge_map = _load_merge_map()

    topic_data: dict[str, dict] = {}

    for c in concepts:
        concept_name = c["concept"]
        topic_slug = merge_map.get(concept_name, _slugify(concept_name))

        if topic_slug not in topic_data:
            topic_data[topic_slug] = {
                "slug": topic_slug,
                "title": _build_topic_title(topic_slug),
                "concepts": [],
                "courses": set(),
                "lessons": [],
            }

        entry = topic_data[topic_slug]
        entry["concepts"].append(concept_name)
        entry["courses"].update(c["courses"])
        entry["lessons"].extend(c["lessons"])

    for entry in topic_data.values():
        entry["courses"] = sorted(entry["courses"])
        entry["concepts"] = sorted(set(entry["concepts"]))

    all_topics = sorted(topic_data.values(), key=lambda t: (-len(t["courses"]), -len(t["concepts"])))

    # Filter: keep multi-course topics, merged topics, and foundational singles
    _config_path = _BACKEND_DIR.parent / "wiki_config.json"
    _FOUNDATIONAL_SLUGS = set()
    if _config_path.exists():
        _cfg = json.loads(_config_path.read_text())
        _FOUNDATIONAL_SLUGS = set(_cfg.get("foundational_slugs", []))

    filtered = [
        t for t in all_topics
        if len(t["courses"]) >= 2
        or len(t["concepts"]) > 1
        or t["slug"] in _FOUNDATIONAL_SLUGS
    ]

    return filtered


async def phase_b(phase_a_data: dict) -> dict:
    """Generate educator profiles and resource index entries via LLM."""
    print("\n" + "=" * 60)
    print("PHASE B: LLM-generated educator profiles + resource curation")
    print("=" * 60)

    today = time.strftime("%Y-%m-%d")
    educator_mentions = phase_a_data["educator_mentions"]
    topics = _group_concepts_into_topics(phase_a_data)

    print(f"\n  Generating {len(educator_mentions)} educator profiles...")
    print(f"  Generating {len(topics)} topic resource entries...")

    # -- Educator profiles --
    async def _gen_educator(name: str, courses: list[str]) -> tuple[str, str]:
        prompt = EDUCATOR_PROFILE_PROMPT.format(
            name=name,
            courses=", ".join(courses),
            today=today,
        )
        content = await _call_llm(prompt, max_tokens=2048)
        return name, content

    educator_tasks = [
        _gen_educator(name, courses)
        for name, courses in educator_mentions.items()
    ]

    # -- Topic resource entries --
    video_by_concept: dict[str, list[dict]] = defaultdict(list)
    for v in phase_a_data["video_resources"]:
        for c in v.get("concepts", []):
            video_by_concept[c.lower()].append(v)

    url_freq = dict(phase_a_data["top_urls"])

    async def _gen_topic(topic: dict) -> tuple[str, str]:
        existing_parts = []

        related_videos = []
        for c in topic["concepts"]:
            related_videos.extend(video_by_concept.get(c, []))
        if related_videos:
            vid_lines = []
            for v in related_videos:
                vid_lines.append(
                    f"  - youtube_id={v['youtube_id']} "
                    f"title=\"{v.get('video_title', '')}\" "
                    f"(from {v['course']}/{v['lesson_slug']})"
                )
            existing_parts.append(
                "EXISTING YOUTUBE VIDEOS already curated for this topic:\n"
                + "\n".join(vid_lines)
            )

        cross_courses = topic["courses"]
        cross_validation = ""
        if len(cross_courses) > 1:
            cross_validation = (
                f"## Cross-validation\n"
                f"This topic appears in {len(cross_courses)} courses: "
                f"{', '.join(cross_courses)}"
            )

        prompt = RESOURCE_CURATION_PROMPT.format(
            topic=topic["slug"],
            topic_title=topic["title"],
            related_concepts=", ".join(topic["concepts"]),
            courses=", ".join(cross_courses),
            existing_data="\n\n".join(existing_parts) if existing_parts else "",
            cross_validation=cross_validation,
            today=today,
        )
        content = await _call_llm(prompt, max_tokens=2048)
        return topic["slug"], content

    topic_tasks = [_gen_topic(t) for t in topics]

    all_tasks = educator_tasks + topic_tasks
    results = await asyncio.gather(*all_tasks, return_exceptions=True)

    educator_profiles = {}
    topic_entries = {}

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"  ERROR in task {i}: {result}")
            continue
        key, content = result
        if i < len(educator_tasks):
            educator_profiles[key] = content
        else:
            topic_entries[key] = content

    print(f"\n  Generated {len(educator_profiles)} educator profiles")
    print(f"  Generated {len(topic_entries)} topic resource entries")

    return {
        "educator_profiles": educator_profiles,
        "topic_entries": topic_entries,
        "topics_metadata": {t["slug"]: t for t in topics},
    }


# ═══════════════════════════════════════════════════════════════════════════
# Phase C: Search verification
# ═══════════════════════════════════════════════════════════════════════════

_VERIFY_PATTERN = re.compile(r'\[VERIFY[^\]]*\]|\[NOT VERIFIED\]', re.IGNORECASE)
_YOUTUBE_ID_PATTERN = re.compile(r'youtube_id[=:\s]+([A-Za-z0-9_-]{11})')
_URL_IN_WIKI = re.compile(r'url[=:\s]+(https?://[^\s\]]+)')


_VERIFY_BATCH_SIZE = 8

_EDUCATOR_PATTERN = re.compile(r'\*\*([^*]+)\*\*')
_TITLE_PATTERN = re.compile(r'["""]([^"""]+)["""]')


def _build_discovery_queries(line: str, topic_key: str) -> list[str]:
    """Build search queries that FIND the resource, not just verify a URL.

    Uses the pedagogical context (educator name, resource title, topic)
    to construct discovery-style searches.
    """
    queries = []

    educator_match = _EDUCATOR_PATTERN.search(line)
    title_match = _TITLE_PATTERN.search(line)
    educator = educator_match.group(1) if educator_match else ""
    title = title_match.group(1) if title_match else ""

    yt_match = _YOUTUBE_ID_PATTERN.search(line)
    url_match = _URL_IN_WIKI.search(line)

    # Discovery search: find the resource by its description
    if educator and title:
        queries.append(f'{educator} "{title}"')
    elif educator:
        queries.append(f"{educator} {topic_key.replace('-', ' ')} tutorial")
    elif title:
        queries.append(f'"{title}" {topic_key.replace("-", " ")}')
    else:
        queries.append(f"best {topic_key.replace('-', ' ')} tutorial resource")

    # If it's a video, also search YouTube specifically
    if yt_match or "youtube" in line.lower() or "video" in line.lower():
        if educator:
            queries.append(f"{educator} {topic_key.replace('-', ' ')} youtube")
        else:
            queries.append(f"{topic_key.replace('-', ' ')} explainer video youtube")

    # Exact-match as secondary signal (may confirm or may fail — that's OK)
    if yt_match:
        queries.append(f"youtube.com/watch?v={yt_match.group(1)}")
    elif url_match:
        url = url_match.group(1).rstrip(".,;:)")
        queries.append(url)

    return queries[:3]


_VERIFY_BATCH_PROMPT = """\
You are finding and verifying teaching resources for an AI/ML learning platform.

Below are {count} resources that need verification. For each, you have:
- The original line from our wiki (with a flagged URL/ID)
- Web search results from discovery searches

Your job: use the search results to find the CORRECT URL or YouTube ID for \
each resource. Don't just check if the original link works — find the RIGHT one.

For each item, return:
1. CONFIRMED — the original URL/ID is correct (search results confirm it)
2. CORRECTED — found the right resource with a DIFFERENT URL/ID \
   (provide the full corrected line with the new URL/ID)
3. NOT FOUND — genuinely cannot determine the correct URL/ID from search results

Return a JSON array with EXACTLY {count} objects (one per item, in order):
[
  {{
    "index": 0,
    "status": "confirmed|corrected|not_found",
    "corrected_line": "the full corrected line with correct URL/ID (no [VERIFY] tag) — or null if not_found",
    "note": "1-sentence explanation of what you found"
  }}
]

ITEMS:
{items}

Return ONLY the JSON array. No markdown fencing, no extra text.
"""


async def _verify_batch(batch: list[dict]) -> list[dict]:
    """Find and verify a batch of [VERIFY] items via discovery search + LLM."""
    search_sem = asyncio.Semaphore(4)

    async def _do_searches(item: dict) -> dict:
        queries = _build_discovery_queries(item["line"], item["key"])
        results = []
        for query in queries:
            async with search_sem:
                print(f"    Searching: {query[:80]}...")
                result = await _search(query)
                results.append(result)
        combined_content = "\n\n".join(
            f"[Query: {r.get('query', '')}]\n{r.get('content', '')[:1200]}"
            for r in results if r.get("content")
        )
        combined_citations = []
        for r in results:
            combined_citations.extend(r.get("citations", []))
        return {
            **item,
            "search_result": {
                "content": combined_content[:4000],
                "citations": combined_citations,
            },
        }

    searched = await asyncio.gather(*[_do_searches(item) for item in batch])

    items_text = ""
    for i, sr in enumerate(searched):
        items_text += f"\n--- Item {i} ({sr['type']}: {sr['key']}) ---\n"
        items_text += f"Line: {sr['line']}\n"
        items_text += f"Search results:\n{sr['search_result'].get('content', '')}\n"
        citations = sr["search_result"].get("citations", [])
        if citations:
            cite_lines = [
                f"  - {c.get('title', '')}: {c.get('url', '')}"
                for c in citations[:10] if isinstance(c, dict)
            ]
            if cite_lines:
                items_text += "Citations:\n" + "\n".join(cite_lines) + "\n"

    raw = await _call_llm(
        _VERIFY_BATCH_PROMPT.format(count=len(batch), items=items_text),
        max_tokens=2048,
    )

    try:
        text = raw.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[-1]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        verdicts = json.loads(text)
    except json.JSONDecodeError:
        print(f"    WARNING: JSON parse failed for batch of {len(batch)}. Keeping [VERIFY] flags.")
        return [{"status": "parse_error", "index": i} for i in range(len(batch))]

    for v, sr in zip(verdicts, searched):
        v["_item"] = sr
    return verdicts


async def phase_c(phase_b_data: dict) -> dict:
    """Verify [VERIFY]-flagged URLs and YouTube IDs via web search.

    Processes items in small batches to avoid oversized LLM prompts.
    """
    print("\n" + "=" * 60)
    print("PHASE C: Verifying flagged resources")
    print("=" * 60)

    verify_items: list[dict] = []

    for name, content in phase_b_data["educator_profiles"].items():
        for line_num, line in enumerate(content.split("\n")):
            if _VERIFY_PATTERN.search(line):
                verify_items.append({
                    "type": "educator",
                    "key": name,
                    "line": line.strip(),
                    "line_num": line_num,
                })

    for slug, content in phase_b_data["topic_entries"].items():
        for line_num, line in enumerate(content.split("\n")):
            if _VERIFY_PATTERN.search(line):
                verify_items.append({
                    "type": "topic",
                    "key": slug,
                    "line": line.strip(),
                    "line_num": line_num,
                })

    print(f"\n  Found {len(verify_items)} items flagged [VERIFY]")

    if not verify_items:
        print("  Nothing to verify — all resources were confident.")
        return phase_b_data

    batches = [
        verify_items[i:i + _VERIFY_BATCH_SIZE]
        for i in range(0, len(verify_items), _VERIFY_BATCH_SIZE)
    ]
    print(f"  Processing in {len(batches)} batches of up to {_VERIFY_BATCH_SIZE}...\n")

    stats = {"confirmed": 0, "corrected": 0, "not_found": 0, "parse_error": 0}

    updated_profiles = dict(phase_b_data["educator_profiles"])
    updated_topics = dict(phase_b_data["topic_entries"])

    for batch_num, batch in enumerate(batches, 1):
        print(f"  --- Batch {batch_num}/{len(batches)} ({len(batch)} items) ---")
        verdicts = await _verify_batch(batch)

        for verdict in verdicts:
            status = verdict.get("status", "parse_error")
            stats[status] = stats.get(status, 0) + 1

            item = verdict.get("_item")
            if not item:
                continue

            key = item["key"]
            corrected_line = verdict.get("corrected_line")
            target = updated_profiles if item["type"] == "educator" else updated_topics
            content = target.get(key, "")

            if status == "confirmed":
                clean = re.sub(r'\s*\[VERIFY[^\]]*\]', '', item["line"]).strip()
                content = content.replace(item["line"], clean)
            elif status == "corrected" and corrected_line:
                content = content.replace(item["line"], corrected_line)
            elif status == "not_found":
                content = content.replace(
                    item["line"],
                    re.sub(r'\[VERIFY[^\]]*\]', '[NOT VERIFIED]', item["line"]),
                )

            target[key] = content

        print(f"    Running totals: {stats}\n")

    print(f"\n  Final: {stats}")
    phase_b_data["educator_profiles"] = updated_profiles
    phase_b_data["topic_entries"] = updated_topics
    return phase_b_data


# ═══════════════════════════════════════════════════════════════════════════
# Phase D: Pedagogical gap-filling via LLM-directed search
# ═══════════════════════════════════════════════════════════════════════════

_GAP_PATTERNS = [
    re.compile(r'None identified', re.IGNORECASE),
    re.compile(r'\[NOT VERIFIED\]', re.IGNORECASE),
    re.compile(r'No .{3,60} video .{3,60} exists', re.IGNORECASE),
    re.compile(r'No .{3,60} resource .{3,60} exists', re.IGNORECASE),
    re.compile(r'youtube_id:\s*None', re.IGNORECASE),
    re.compile(r'Gap:', re.IGNORECASE),
]

_SECTION_HEADER = re.compile(r'^##\s+(.+)', re.MULTILINE)

_DISCOVERY_QUERY_PROMPT = """\
You are a pedagogical search strategist for an AI/ML learning platform.

TOPIC: {topic}
RELATED CONCEPTS: {concepts}

Below is the current wiki entry for this topic. Some resource slots have gaps \
(marked "None identified", "[NOT VERIFIED]", or noted as coverage gaps).

CURRENT ENTRY:
{entry}

Your task: generate 4-6 targeted web search queries designed to FIND the best \
teaching resources to fill these gaps. These are NOT factual searches — you \
are looking for content that helps students LEARN and build INTUITION.

For each query, specify what gap it targets.

SEARCH STRATEGY RULES:
1. Include educator names when you know who likely covers this topic well \
   (e.g., "StatQuest dropout regularization explained")
2. Include terms like "tutorial", "explained", "from scratch", "visual", \
   "intuition" — these surface teaching content, not papers
3. Include year filters (2023, 2024, 2025) to find recent content
4. For video gaps: include "youtube" in the query
5. For blog gaps: include the likely author's domain or name
6. For code gaps: include "from scratch", "implementation", "notebook"

Return a JSON object:
{{
  "queries": [
    {{
      "query": "the search query",
      "target_gap": "which gap this fills (e.g., 'Video (best)', 'Code walkthrough')",
      "rationale": "why this query will find good teaching content"
    }}
  ]
}}

Return ONLY valid JSON.
"""

_DISCOVERY_EVAL_PROMPT = """\
You are a pedagogical quality evaluator for an AI/ML learning platform.

TOPIC: {topic}
GAP BEING FILLED: {target_gap}

We searched for teaching resources and found the following results. \
Evaluate each for TEACHING QUALITY, not just existence.

SEARCH RESULTS:
{search_results}

CURRENT ENTRY (for context):
{current_section}

For the best resource found, provide:
1. Is it genuinely useful for teaching this topic? (not just tangentially related)
2. What level is it appropriate for? (beginner/intermediate/advanced)
3. Does it complement or duplicate what we already have?

Return a JSON object:
{{
  "found_resource": true/false,
  "resource_type": "video|blog|paper|code|other",
  "educator": "Name of creator/author",
  "title": "Resource title",
  "url_or_id": "Full URL or youtube_id=XXXXXXXXXXX",
  "level": "beginner|intermediate|advanced",
  "why_good": "1-2 sentences on why this is good for teaching",
  "replacement_line": "The complete markdown line to insert into the wiki entry",
  "confidence": "high|medium|low"
}}

If nothing suitable was found, return:
{{
  "found_resource": false,
  "note": "Why nothing suitable was found"
}}

Return ONLY valid JSON.
"""

_PHASE_D_BATCH_SIZE = 4


def _identify_gaps(topic_slug: str, content: str) -> list[dict]:
    """Identify specific gaps in a topic's wiki entry."""
    gaps = []

    sections = _SECTION_HEADER.split(content)
    current_section = ""
    current_header = ""

    for i, part in enumerate(sections):
        if i % 2 == 1:
            current_header = part.strip()
        else:
            current_section = part.strip()
            if not current_header:
                continue

            has_gap = False
            gap_details = []
            for pattern in _GAP_PATTERNS:
                matches = pattern.findall(current_section)
                if matches:
                    has_gap = True
                    gap_details.extend(matches)

            if has_gap:
                gaps.append({
                    "topic": topic_slug,
                    "section": current_header,
                    "content": current_section[:500],
                    "gap_indicators": gap_details[:5],
                })

    return gaps


async def phase_d(phase_b_data: dict) -> dict:
    """Pedagogical gap-filling: LLM-crafted discovery searches for teaching resources."""
    print("\n" + "=" * 60)
    print("PHASE D: Pedagogical gap-filling via discovery search")
    print("=" * 60)

    topics_with_gaps: list[dict] = []

    for slug, content in phase_b_data["topic_entries"].items():
        gaps = _identify_gaps(slug, content)
        if gaps:
            topics_with_gaps.append({
                "slug": slug,
                "content": content,
                "gaps": gaps,
            })

    total_gaps = sum(len(t["gaps"]) for t in topics_with_gaps)
    print(f"\n  Topics with gaps: {len(topics_with_gaps)}/{len(phase_b_data['topic_entries'])}")
    print(f"  Total gap sections: {total_gaps}")

    if not topics_with_gaps:
        print("  No gaps found — wiki is fully populated.")
        return phase_b_data

    updated_topics = dict(phase_b_data["topic_entries"])
    stats = {"filled": 0, "not_found": 0, "low_confidence": 0, "errors": 0}

    batches = [
        topics_with_gaps[i:i + _PHASE_D_BATCH_SIZE]
        for i in range(0, len(topics_with_gaps), _PHASE_D_BATCH_SIZE)
    ]

    for batch_num, batch in enumerate(batches, 1):
        print(f"\n  --- Batch {batch_num}/{len(batches)} ---")

        for topic in batch:
            slug = topic["slug"]
            content = topic["content"]
            gaps = topic["gaps"]
            concepts = []

            meta = phase_b_data.get("topics_metadata", {}).get(slug, {})
            if meta:
                concepts = meta.get("concepts", [])

            print(f"\n    Topic: {slug} ({len(gaps)} gap sections)")

            # Step 1: LLM crafts discovery queries
            query_prompt = _DISCOVERY_QUERY_PROMPT.format(
                topic=slug.replace("-", " "),
                concepts=", ".join(concepts) if concepts else slug.replace("-", " "),
                entry=content[:3000],
            )

            try:
                raw = await _call_llm(query_prompt, max_tokens=1500)
                text = raw.strip()
                if text.startswith("```"):
                    text = text.split("\n", 1)[-1]
                if text.endswith("```"):
                    text = text[:-3]
                query_plan = json.loads(text.strip())
                queries = query_plan.get("queries", [])
            except (json.JSONDecodeError, Exception) as e:
                print(f"    ERROR generating queries for {slug}: {e}")
                stats["errors"] += 1
                continue

            print(f"    Generated {len(queries)} discovery queries")

            # Step 2: Execute searches
            search_sem = asyncio.Semaphore(3)
            search_results_by_gap: dict[str, list] = {}

            async def _run_search(q: dict) -> tuple[str, dict]:
                async with search_sem:
                    print(f"      Searching: {q['query'][:75]}...")
                    result = await _search(q["query"])
                return q.get("target_gap", ""), result

            search_tasks = [_run_search(q) for q in queries]
            search_outputs = await asyncio.gather(*search_tasks, return_exceptions=True)

            for output in search_outputs:
                if isinstance(output, Exception):
                    continue
                gap_target, result = output
                if gap_target not in search_results_by_gap:
                    search_results_by_gap[gap_target] = []
                search_results_by_gap[gap_target].append(result)

            # Step 3: Evaluate findings per gap section
            for gap in gaps:
                section = gap["section"]
                relevant_results = []
                for gap_key, results in search_results_by_gap.items():
                    if (section.lower() in gap_key.lower()
                            or gap_key.lower() in section.lower()
                            or gap_key == ""):
                        relevant_results.extend(results)

                if not relevant_results:
                    # Use all results if no specific match
                    for results in search_results_by_gap.values():
                        relevant_results.extend(results)

                combined_search = "\n\n".join(
                    f"[Query: {r.get('query', '')}]\n{r.get('content', '')[:1200]}"
                    for r in relevant_results[:4] if r.get("content")
                )

                if not combined_search.strip():
                    stats["not_found"] += 1
                    continue

                eval_prompt = _DISCOVERY_EVAL_PROMPT.format(
                    topic=slug.replace("-", " "),
                    target_gap=section,
                    search_results=combined_search[:5000],
                    current_section=gap["content"],
                )

                try:
                    raw = await _call_llm(eval_prompt, max_tokens=1000)
                    text = raw.strip()
                    if text.startswith("```"):
                        text = text.split("\n", 1)[-1]
                    if text.endswith("```"):
                        text = text[:-3]
                    evaluation = json.loads(text.strip())
                except (json.JSONDecodeError, Exception) as e:
                    print(f"      ERROR evaluating {section}: {e}")
                    stats["errors"] += 1
                    continue

                if not evaluation.get("found_resource"):
                    print(f"      {section}: no suitable resource found")
                    stats["not_found"] += 1
                    continue

                confidence = evaluation.get("confidence", "low")
                if confidence == "low":
                    print(f"      {section}: found but low confidence — skipping")
                    stats["low_confidence"] += 1
                    continue

                educator = evaluation.get("educator", "Unknown")
                title = evaluation.get("title", "")
                url_or_id = evaluation.get("url_or_id", "")
                why = evaluation.get("why_good", "")
                replacement = evaluation.get("replacement_line", "")

                print(f"      {section}: FILLED — {educator} \"{title}\" ({confidence})")

                # Insert discovery note into the wiki entry
                discovery_note = (
                    f"\n\n> **[Discovery — Phase D]** "
                    f"{replacement}\n"
                    f"> *Why*: {why}\n"
                    f"> *Confidence*: {confidence} | *Found*: {time.strftime('%Y-%m-%d')}"
                )

                # Append after the gap section
                section_pattern = re.compile(
                    rf'(## {re.escape(section)}.*?)(?=\n## |\n---|\Z)',
                    re.DOTALL,
                )
                match = section_pattern.search(content)
                if match:
                    insert_pos = match.end()
                    content = content[:insert_pos] + discovery_note + content[insert_pos:]
                    stats["filled"] += 1
                else:
                    content += discovery_note
                    stats["filled"] += 1

            updated_topics[slug] = content

        print(f"\n    Running totals: {stats}")

    print(f"\n  Final: {stats}")
    phase_b_data["topic_entries"] = updated_topics
    return phase_b_data


# ═══════════════════════════════════════════════════════════════════════════
# Phase E: Download source content (blogs, transcripts) for wiki resources
# ═══════════════════════════════════════════════════════════════════════════

_WIKI_URL_RE = re.compile(
    r'(?:url|URL)[=:\s]+(https?://[^\s\]\)>]+)', re.IGNORECASE
)
_WIKI_YT_RE = re.compile(r'youtube_id[=:\s]+([A-Za-z0-9_-]{11})')
_DISCOVERY_URL_RE = re.compile(
    r'\[([^\]]+)\]\((https?://[^\s\)]+)\)'
)


def _parse_sources_from_page(content: str) -> list[dict]:
    """Extract all downloadable sources (URLs + youtube_ids) from a topic page."""
    sources: list[dict] = []
    seen_urls: set[str] = set()

    _SKIP_HOSTS = {"www.youtube.com", "youtube.com", "youtu.be"}

    def _is_downloadable_url(url: str) -> bool:
        parsed = urlparse(url)
        host = parsed.hostname or ""
        if host in _SKIP_HOSTS:
            return False
        if not parsed.path or parsed.path == "/":
            return False
        return True

    for match in _WIKI_URL_RE.finditer(content):
        url = match.group(1).rstrip(".,;:")
        if url in seen_urls or not _is_downloadable_url(url):
            continue
        ctx = content[max(0, match.start() - 20):match.end() + 20]
        if "[NOT VERIFIED]" in ctx or "[VERIFY]" in ctx:
            continue
        seen_urls.add(url)
        parsed = urlparse(url)
        if parsed.hostname and "arxiv.org" in parsed.hostname:
            source_type = "paper"
        elif parsed.hostname and "github.com" in parsed.hostname:
            source_type = "code"
        else:
            source_type = "blog"
        sources.append({"type": source_type, "url": url})

    for match in _DISCOVERY_URL_RE.finditer(content):
        url = match.group(2).rstrip(".,;:")
        if url in seen_urls or not _is_downloadable_url(url):
            continue
        seen_urls.add(url)
        parsed = urlparse(url)
        if parsed.hostname and "arxiv.org" in parsed.hostname:
            source_type = "paper"
        elif parsed.hostname and "github.com" in parsed.hostname:
            source_type = "code"
        else:
            source_type = "blog"
        sources.append({"type": source_type, "url": url})

    for match in _WIKI_YT_RE.finditer(content):
        yt_id = match.group(1)
        yt_url = f"https://www.youtube.com/watch?v={yt_id}"
        if yt_url in seen_urls:
            continue
        seen_urls.add(yt_url)
        sources.append({"type": "youtube", "youtube_id": yt_id})

    return sources


def _source_slug(source: dict) -> str:
    """Generate a filename slug for a downloaded source."""
    if source["type"] == "youtube":
        return f"yt-{source['youtube_id']}"
    url = source["url"]
    parsed = urlparse(url)
    path = parsed.path.strip("/").replace("/", "-")
    host = parsed.hostname or ""
    host = host.replace("www.", "").replace(".com", "").replace(".io", "")
    host = host.replace(".github", "").replace(".org", "")
    slug = f"{host}-{path}" if path else host
    slug = re.sub(r'[^a-zA-Z0-9_-]', '-', slug)
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug[:80]


_JUNK_PHRASES = [
    "redirecting...",
    "sign in",
    "we read every piece of feedback",
    "while you're here, feast your eyes",
    "enable javascript",
    "please enable cookies",
    "just a moment",
    "access denied",
    "403 forbidden",
]

_MIN_DOWNLOAD_WORDS = 80


def _clean_extracted_text(text: str) -> str:
    """Strip common template/boilerplate artifacts from extracted text."""
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if stripped == "{{ message }}":
            continue
        if stripped.startswith("| Name | Name |"):
            continue
        if stripped == "|---|---|---|---|---|":
            continue
        if stripped.startswith("Skip to content"):
            continue
        if stripped.startswith("Navigation Menu"):
            continue
        cleaned.append(line)
    return "\n".join(cleaned).strip()


def _is_junk_content(text: str) -> bool:
    """Detect boilerplate/redirect/sign-in pages."""
    lower = text.lower().strip()
    for phrase in _JUNK_PHRASES:
        if lower.startswith(phrase) or lower == phrase:
            return True
    words = text.split()
    if len(words) < _MIN_DOWNLOAD_WORDS:
        return True
    return False


async def _fetch_github_notebook(url: str) -> dict:
    """Fetch a GitHub-hosted .ipynb notebook and extract markdown + code cells."""
    try:
        raw_url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

        client = _get_http_client()
        resp = await client.get(raw_url, follow_redirects=True)
        if resp.status_code != 200:
            return {"url": url, "content": "", "error": f"HTTP {resp.status_code}"}

        nb = json.loads(resp.text)
        cells = nb.get("cells", [])
        parts: list[str] = []

        for cell in cells:
            cell_type = cell.get("cell_type", "")
            source = "".join(cell.get("source", []))
            if not source.strip():
                continue

            if cell_type == "markdown":
                parts.append(source)
            elif cell_type == "code":
                parts.append(f"```python\n{source}\n```")

        text = "\n\n".join(parts)
        if not text.strip():
            return {"url": url, "content": "", "error": "No cells extracted"}

        return {"url": url, "content": text, "word_count": len(text.split())}
    except json.JSONDecodeError:
        return {"url": url, "content": "", "error": "Not valid JSON (not a notebook)"}
    except Exception as e:
        return {"url": url, "content": "", "error": str(e)}


async def _fetch_github_readme(url: str) -> dict:
    """For GitHub repo root URLs, try fetching the README via raw URL."""
    try:
        parsed = urlparse(url)
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) < 2:
            return {"url": url, "content": "", "error": "Not a valid repo URL"}

        owner, repo = path_parts[0], path_parts[1]

        for branch in ("main", "master"):
            raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md"
            client = _get_http_client()
            resp = await client.get(raw_url, follow_redirects=True)
            if resp.status_code == 200:
                text = resp.text
                if len(text.split()) >= _MIN_DOWNLOAD_WORDS:
                    return {"url": url, "content": text, "word_count": len(text.split())}

        return {"url": url, "content": "", "error": "No README found"}
    except Exception as e:
        return {"url": url, "content": "", "error": str(e)}


async def _fetch_blog(url: str) -> dict:
    """Fetch blog/page content using trafilatura, with fallbacks for special URLs."""
    parsed = urlparse(url)
    host = parsed.hostname or ""

    if "github.com" in host and ".ipynb" in parsed.path:
        return await _fetch_github_notebook(url)

    if "github.com" in host and "/blob/" not in parsed.path and "/tree/" not in parsed.path:
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) == 2:
            return await _fetch_github_readme(url)

    if "colab.research.google.com" in host:
        return {"url": url, "content": "", "error": "Colab notebooks require auth"}

    async def _try_fallbacks() -> dict:
        """Chain: browser → search. Returns first success."""
        browser_result = await _fetch_with_browser(url)
        if browser_result.get("content"):
            return browser_result
        return await _fetch_via_search(url)

    try:
        import trafilatura
        downloaded = await asyncio.to_thread(trafilatura.fetch_url, url)
        if not downloaded:
            if "github.com" in host:
                result = await _fetch_github_readme(url)
                if result.get("content"):
                    return result
            return await _try_fallbacks()

        text = await asyncio.to_thread(
            trafilatura.extract,
            downloaded,
            include_links=True,
            include_tables=True,
            favor_recall=True,
            output_format="txt",
        )
        if not text:
            if "github.com" in host:
                result = await _fetch_github_readme(url)
                if result.get("content"):
                    return result
            return await _try_fallbacks()

        text = _clean_extracted_text(text)

        if _is_junk_content(text):
            if "github.com" in host:
                result = await _fetch_github_readme(url)
                if result.get("content"):
                    return result
            return await _try_fallbacks()

        return {"url": url, "content": text, "word_count": len(text.split()),
                "_raw_html": downloaded}
    except Exception as e:
        return {"url": url, "content": "", "error": str(e)}


async def _fetch_with_browser(url: str) -> dict:
    """Fallback: use headless Chromium via Playwright to render JS-heavy pages."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        return {"url": url, "content": "", "error": "playwright not installed"}

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            )
            page = await context.new_page()
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(2000)

            text = await page.evaluate("""() => {
                for (const sel of ['nav', 'footer', 'header', '.sidebar',
                    '[role="navigation"]', '.cookie-banner', '#cookie-consent']) {
                    for (const el of document.querySelectorAll(sel)) el.remove();
                }
                const main = document.querySelector(
                    'main, article, .content, .post-content, #content'
                );
                return (main || document.body).innerText;
            }""")

            await browser.close()

        if not text or not text.strip():
            return {"url": url, "content": "", "error": "Browser rendered empty page"}

        text = _clean_extracted_text(text)
        word_count = len(text.split())

        if word_count < _MIN_DOWNLOAD_WORDS:
            return {"url": url, "content": "", "error": f"Browser got only {word_count} words"}

        return {"url": url, "content": text, "word_count": word_count, "via": "browser"}
    except Exception as e:
        err = str(e).split("\n")[0][:120]
        return {"url": url, "content": "", "error": f"Browser failed: {err}"}


async def _fetch_via_search(url: str) -> dict:
    """Last resort: use Perplexity search to retrieve page content."""
    query = (
        f"Provide a detailed, comprehensive summary of the content at this URL. "
        f"Include all key concepts, code examples, and technical details. "
        f"URL: {url}"
    )
    try:
        result = await _search(query)
        content = result.get("content", "")
        if not content or len(content.split()) < _MIN_DOWNLOAD_WORDS:
            return {"url": url, "content": "", "error": "Search returned insufficient content"}

        header = f"# Source: {url}\n# Fetched via: search fallback\n"
        return {
            "url": url,
            "content": content,
            "word_count": len(content.split()),
            "via": "search",
        }
    except Exception as e:
        return {"url": url, "content": "", "error": f"Search fallback failed: {e}"}


async def _fetch_transcript(youtube_id: str) -> dict:
    """Fetch YouTube transcript using youtube-transcript-api v1.2+."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        def _do_fetch():
            api = YouTubeTranscriptApi()
            transcript = api.fetch(youtube_id)
            return transcript.to_raw_data()

        snippets = await asyncio.to_thread(_do_fetch)
        full_text = " ".join(s["text"] for s in snippets)
        return {
            "youtube_id": youtube_id,
            "content": full_text,
            "word_count": len(full_text.split()),
        }
    except Exception as e:
        err = str(e).split("\n")[0][:120]
        return {"youtube_id": youtube_id, "content": "", "error": err}


async def download_wiki_content(topic_filter: list[str] | None = None) -> None:
    """Download source content for all wiki resource pages.

    For each topic page, parse URLs and youtube_ids, fetch content,
    and save as markdown files in a subfolder next to the topic page.
    """
    print("\n" + "=" * 60)
    print("Phase E: Downloading wiki source content")
    print("=" * 60)

    topics_dir = _WIKI_DIR / "resources" / "by-topic"
    topic_pages = sorted(
        f for f in topics_dir.glob("*.md") if f.name != "_index.md"
    )

    if topic_filter:
        topic_pages = [f for f in topic_pages if f.stem in topic_filter]

    total_sources = 0
    total_downloaded = 0
    total_skipped = 0
    total_errors = 0

    fetch_sem = asyncio.Semaphore(3)

    for page_path in topic_pages:
        topic_slug = page_path.stem
        content = page_path.read_text()
        sources = _parse_sources_from_page(content)

        if not sources:
            continue

        dl_dir = topics_dir / topic_slug
        dl_dir.mkdir(exist_ok=True)

        print(f"\n  {topic_slug}: {len(sources)} sources")
        total_sources += len(sources)

        async def _download_one(src: dict) -> tuple[str, bool, str]:
            slug = _source_slug(src)
            ext = ".txt" if src["type"] == "youtube" else ".md"
            out_path = dl_dir / f"{slug}{ext}"

            if out_path.exists():
                existing_words = len(out_path.read_text().split())
                if existing_words >= _MIN_DOWNLOAD_WORDS:
                    return slug, False, "skipped (exists)"

            async with fetch_sem:
                if src["type"] == "youtube":
                    result = await _fetch_transcript(src["youtube_id"])
                else:
                    result = await _fetch_blog(src["url"])

            if result.get("error") or not result.get("content"):
                err = result.get("error", "empty content")
                return slug, False, f"error: {err}"

            header_lines = []
            if src["type"] == "youtube":
                header_lines.append(
                    f"# Transcript: youtube_id={src['youtube_id']}"
                )
                header_lines.append(
                    f"# URL: https://www.youtube.com/watch?v={src['youtube_id']}"
                )
            else:
                header_lines.append(f"# Source: {src['url']}")
                if result.get("via") == "browser":
                    header_lines.append("# Fetched via: headless browser (Playwright)")
                elif result.get("via") == "search":
                    header_lines.append("# Fetched via: search fallback (Perplexity)")
            header_lines.append(f"# Downloaded: {time.strftime('%Y-%m-%d')}")
            header_lines.append(
                f"# Words: {result.get('word_count', 0)}"
            )

            # --- Author resolution (same logic as download_source) ---
            source_url = src.get("url", "")
            author_name = ""
            author_slug = ""
            author_entry = resolve_author(source_url) if source_url else None

            if author_entry and is_venue(author_entry.get("slug", "")):
                arxiv_id = parse_arxiv_id(source_url)
                if arxiv_id:
                    try:
                        paper_authors = await extract_arxiv_authors(arxiv_id)
                        author_name = format_paper_authors(paper_authors)
                    except Exception:
                        author_name = ""
            elif author_entry:
                author_name = author_entry.get("name", "")
                author_slug = author_entry.get("slug", "")
            elif result.get("_raw_html"):
                extracted = extract_author_from_html(result["_raw_html"])
                if extracted:
                    author_name = extracted

            if author_name:
                header_lines.append(f"# Author: {author_name}")
            if author_slug:
                header_lines.append(f"# Author Slug: {author_slug}")

            header_lines.append("")

            final = "\n".join(header_lines) + result["content"]
            out_path.write_text(final)
            return slug, True, f"OK ({result.get('word_count', 0)} words)"

        tasks = [_download_one(src) for src in sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for r in results:
            if isinstance(r, Exception):
                print(f"    ERROR: {r}")
                total_errors += 1
                continue
            slug, downloaded, status = r
            if downloaded:
                total_downloaded += 1
                print(f"    + {slug}: {status}")
            elif "skipped" in status:
                total_skipped += 1
            else:
                total_errors += 1
                print(f"    x {slug}: {status}")

    print(f"\n  Summary:")
    print(f"    Total sources:  {total_sources}")
    print(f"    Downloaded:     {total_downloaded}")
    print(f"    Skipped (exist):{total_skipped}")
    print(f"    Errors:         {total_errors}")


# ═══════════════════════════════════════════════════════════════════════════
# Consolidation: merge/split resource pages to match concept map
# ═══════════════════════════════════════════════════════════════════════════

_MERGE_PROMPT = """\
You are reorganizing a teaching resource wiki. Merge the content from a \
SECONDARY topic page into a PRIMARY topic page.

PRIMARY PAGE (keep this as the base):
{primary_content}

SECONDARY PAGE (merge this content in):
{secondary_content}

RULES:
1. Add the secondary page's resources under a new subtopic section \
   (## {secondary_title}) within the primary page
2. Deduplicate — if both pages recommend the same resource, keep the \
   more detailed version
3. Merge coverage notes — combine gap analysis from both pages
4. Keep the primary page's header (# title) and overall structure
5. Update "Last Verified" to today: {today}
6. Remove any [Discovery — Phase D] blockquote formatting — integrate \
   those resources cleanly into the sections
7. Output ONLY the final merged markdown — no commentary

Return the complete merged markdown page.
"""

_NEW_TOPIC_PROMPT = """\
You are creating a resource index page for a teaching wiki.

TOPIC: {title}
SUBTOPICS AND CONCEPTS:
{subtopics_text}

This topic does not have an existing resource page. Create one following \
this format:

# {title}

## Video (best)
- **Educator** — "Title"
- youtube_id: XXXXXXXXXXX or "None identified"
- Why: ...
- Level: ...

## Blog / Written explainer (best)
...

## Deep dive
...

## Original paper
...

## Code walkthrough
...

## Coverage notes
- Strong: ...
- Weak: ...
- Gap: ...

## Last Verified
{today}

RULES:
- Only include resources you are HIGHLY confident exist
- Flag uncertain URLs/IDs with [VERIFY]
- Prefer: 3Blue1Brown, Karpathy, Alammar, Weng, Olah, Raschka, StatQuest
- If no good resource exists for a category, write "None identified"

Return ONLY the markdown page.
"""


async def consolidate_wiki() -> None:
    """Merge/split resource pages to match the concept map's topic structure."""
    print("\n" + "=" * 60)
    print("Consolidating wiki to match concept map")
    print("=" * 60)

    if not _CONCEPT_MAP_PATH.exists():
        print("  ERROR: No concept-map.md found. Run --concept-map first.")
        return

    merge_map = _parse_concept_map(_CONCEPT_MAP_PATH)
    new_topics = set(merge_map.values())

    topics_dir = _WIKI_DIR / "resources" / "by-topic"
    existing = {
        f.stem: f.read_text()
        for f in topics_dir.glob("*.md")
        if f.name != "_index.md"
    }

    kept = new_topics & set(existing.keys())
    dropped = set(existing.keys()) - new_topics
    added = new_topics - set(existing.keys())

    print(f"\n  Existing pages: {len(existing)}")
    print(f"  Target topics:  {len(new_topics)}")
    print(f"  Kept:    {len(kept)}")
    print(f"  Dropped: {len(dropped)} (will merge into parents)")
    print(f"  New:     {len(added)} (will generate)")

    # Build merge plan: which dropped file goes into which parent
    concept_map_lines = _CONCEPT_MAP_PATH.read_text().splitlines()
    current_h1 = ""
    subtopic_to_topic: dict[str, str] = {}

    for line in concept_map_lines:
        if line.startswith("# ") and not line.startswith("# Concept"):
            current_h1 = line[2:].strip()
        elif line.startswith("## "):
            st = line[3:].strip()
            subtopic_to_topic[st] = current_h1

    merge_plan: dict[str, list[str]] = {}
    for d in dropped:
        parent = None
        for st_slug, topic_slug in subtopic_to_topic.items():
            if d in st_slug or st_slug in d or d == st_slug:
                parent = topic_slug
                break
        if not parent:
            for concept, topic in merge_map.items():
                if d.replace("-", " ") == concept or concept == d.replace("-", " "):
                    parent = topic
                    break
        if parent:
            merge_plan.setdefault(parent, []).append(d)
        else:
            print(f"  WARNING: Cannot find parent for dropped topic '{d}' — skipping")

    today = time.strftime("%Y-%m-%d")

    # -- Merge dropped files into parents --
    print(f"\n  Merging {len(dropped)} dropped files...")
    for parent_slug, children in sorted(merge_plan.items()):
        parent_content = existing.get(parent_slug, "")
        if not parent_content:
            print(f"    WARNING: Parent '{parent_slug}' has no existing page — skipping merges")
            continue

        for child_slug in children:
            child_content = existing.get(child_slug, "")
            if not child_content:
                continue

            child_title = _build_topic_title(child_slug)
            print(f"    Merging {child_slug} → {parent_slug}...")

            merged = await _call_llm(
                _MERGE_PROMPT.format(
                    primary_content=parent_content[:6000],
                    secondary_content=child_content[:6000],
                    secondary_title=child_title,
                    today=today,
                ),
                max_tokens=4096,
            )
            parent_content = merged
            existing[parent_slug] = merged

            # Remove the old file
            old_path = topics_dir / f"{child_slug}.md"
            if old_path.exists():
                old_path.unlink()
                print(f"      Removed: {child_slug}.md")

    # -- Generate new topic pages --
    if added:
        print(f"\n  Generating {len(added)} new topic pages...")

        for topic_slug in sorted(added):
            title = _build_topic_title(topic_slug)

            # Gather subtopics for this topic from concept map
            subtopics_for_topic: dict[str, list[str]] = {}
            current_h1 = ""
            current_subtopic = ""
            for line in concept_map_lines:
                if line.startswith("# ") and not line.startswith("# Concept"):
                    current_h1 = line[2:].strip()
                elif line.startswith("## ") and current_h1 == topic_slug:
                    current_subtopic = line[3:].strip()
                    subtopics_for_topic[current_subtopic] = []
                elif line.startswith("- ") and current_h1 == topic_slug and current_subtopic:
                    subtopics_for_topic[current_subtopic].append(line[2:].strip())

            subtopics_text = "\n".join(
                f"### {st}\n" + "\n".join(f"- {c}" for c in concepts)
                for st, concepts in subtopics_for_topic.items()
            )

            print(f"    Generating: {topic_slug} ({len(subtopics_for_topic)} subtopics)...")
            content = await _call_llm(
                _NEW_TOPIC_PROMPT.format(
                    title=title,
                    subtopics_text=subtopics_text,
                    today=today,
                ),
                max_tokens=3000,
            )
            existing[topic_slug] = content

    # -- Write all updated files --
    print(f"\n  Writing {len(new_topics)} topic files...")
    for slug in sorted(new_topics):
        content = existing.get(slug, "")
        if content:
            (topics_dir / f"{slug}.md").write_text(content)
            print(f"    Wrote: {slug}.md")

    # -- Update index --
    resource_index_lines = ["# Resource Index — By Topic\n"]
    resource_index_lines.append(
        "Best teaching resources per topic. Used by the Course Creator "
        "to populate youtube_id, video_title, and Recommended Reading.\n"
    )
    for slug in sorted(new_topics):
        title = _build_topic_title(slug)
        resource_index_lines.append(
            f"- [{title}](by-topic/{slug}.md)"
        )
    ((_WIKI_DIR / "resources") / "_index.md").write_text(
        "\n".join(resource_index_lines) + "\n"
    )

    # -- Update master index --
    educators_dir = _WIKI_DIR / "educators"
    n_educators = len([f for f in educators_dir.glob("*.md") if f.name != "_index.md"])
    master_lines = [
        "# Pedagogy Wiki\n",
        "A curated knowledge base of teaching resources and educator profiles ",
        "for the SocraticTutor platform. Used by the Course Creator to populate ",
        "videos, recommended reading, and teaching context for every lesson.\n",
        "## Collections\n",
        f"- [Educator Registry](educators/_index.md) — {n_educators} educator profiles",
        f"- [Resource Index](resources/_index.md) — {len(new_topics)} topic resource entries",
        f"- [Concept Map](concept-map.md) — 3-level hierarchy\n",
        "## How This Wiki Is Used\n",
        "1. **Course Creator** reads relevant resource entries before generating lesson content",
        "2. Each lesson gets `youtube_id`, `video_title`, and a Recommended Reading section",
        "3. New sources discovered during enrichment are filed back into the resource index",
        "4. Educator profiles help pair the right video/blog with the right topic\n",
        f"## Stats\n",
        f"- Educators: {n_educators}",
        f"- Topics: {len(new_topics)}",
        f"- Consolidated: {time.strftime('%Y-%m-%d %H:%M')}\n",
    ]
    (_WIKI_DIR / "_index.md").write_text("\n".join(master_lines))

    print(f"\n  Consolidation complete: {len(new_topics)} topic pages")
    print(f"  Merged: {len(dropped)} | New: {len(added)} | Kept: {len(kept)}")


# ═══════════════════════════════════════════════════════════════════════════
# Write wiki files to disk
# ═══════════════════════════════════════════════════════════════════════════

def write_wiki(phase_a_data: dict, phase_b_data: dict) -> None:
    """Write all wiki files to content/pedagogy-wiki/."""
    print("\n" + "=" * 60)
    print("Writing wiki files to disk")
    print("=" * 60)

    educators_dir = _WIKI_DIR / "educators"
    resources_dir = _WIKI_DIR / "resources" / "by-topic"
    educators_dir.mkdir(parents=True, exist_ok=True)
    resources_dir.mkdir(parents=True, exist_ok=True)

    # -- Educator profiles --
    educator_index_lines = ["# Educator Registry — Index\n"]
    educator_index_lines.append("Quick lookup: who teaches what in the AI/ML education ecosystem.\n")

    for name, content in sorted(phase_b_data["educator_profiles"].items()):
        slug = _slugify(name)
        filepath = educators_dir / f"{slug}.md"
        filepath.write_text(content)
        courses = phase_a_data["educator_mentions"].get(name, [])
        educator_index_lines.append(
            f"- [{name}]({slug}.md) — mentioned in: {', '.join(courses)}"
        )
        print(f"  Wrote: educators/{slug}.md")

    (educators_dir / "_index.md").write_text("\n".join(educator_index_lines) + "\n")
    print(f"  Wrote: educators/_index.md")

    # -- Topic resource entries --
    resource_index_lines = ["# Resource Index — By Topic\n"]
    resource_index_lines.append(
        "Best teaching resources per topic. Used by the Course Creator "
        "to populate youtube_id, video_title, and Recommended Reading.\n"
    )

    topics_meta = phase_b_data.get("topics_metadata", {})

    for slug, content in sorted(phase_b_data["topic_entries"].items()):
        filepath = resources_dir / f"{slug}.md"
        filepath.write_text(content)
        meta = topics_meta.get(slug, {})
        n_courses = len(meta.get("courses", []))
        concepts_str = ", ".join(meta.get("concepts", [])[:5])
        resource_index_lines.append(
            f"- [{meta.get('title', slug)}](by-topic/{slug}.md) "
            f"— {n_courses} course(s) | concepts: {concepts_str}"
        )
        print(f"  Wrote: resources/by-topic/{slug}.md")

    ((_WIKI_DIR / "resources") / "_index.md").write_text(
        "\n".join(resource_index_lines) + "\n"
    )
    print(f"  Wrote: resources/_index.md")

    # -- Master index --
    master_lines = [
        "# Pedagogy Wiki\n",
        "A curated knowledge base of teaching resources and educator profiles ",
        "for the SocraticTutor platform. Used by the Course Creator to populate ",
        "videos, recommended reading, and teaching context for every lesson.\n",
        "## Collections\n",
        f"- [Educator Registry](educators/_index.md) — "
        f"{len(phase_b_data['educator_profiles'])} educator profiles",
        f"- [Resource Index](resources/_index.md) — "
        f"{len(phase_b_data['topic_entries'])} topic resource entries\n",
        "## How This Wiki Is Used\n",
        "1. **Course Creator** reads relevant resource entries before generating "
        "lesson content",
        "2. Each lesson gets `youtube_id`, `video_title`, and a Recommended Reading "
        "section from the resource index",
        "3. New sources discovered during enrichment are filed back into the "
        "resource index",
        "4. Educator profiles help the system pair the right video/blog with "
        "the right topic\n",
        f"## Stats\n",
        f"- Educators: {len(phase_b_data['educator_profiles'])}",
        f"- Topics: {len(phase_b_data['topic_entries'])}",
        f"- Concepts covered: {sum(len(t.get('concepts', [])) for t in topics_meta.values())}",
        f"- Generated: {time.strftime('%Y-%m-%d %H:%M')}\n",
    ]
    (_WIKI_DIR / "_index.md").write_text("\n".join(master_lines))
    print(f"  Wrote: _index.md")

    total = len(phase_b_data["educator_profiles"]) + len(phase_b_data["topic_entries"]) + 3
    print(f"\n  Total files written: {total}")


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def _load_wiki_from_disk() -> dict:
    """Load existing wiki .md files into the same dict format Phase B produces."""
    educator_profiles = {}
    topic_entries = {}

    educators_dir = _WIKI_DIR / "educators"
    for md in sorted(educators_dir.glob("*.md")):
        if md.name == "_index.md":
            continue
        content = md.read_text()
        first_line = content.split("\n", 1)[0]
        name = first_line.lstrip("# ").strip()
        educator_profiles[name] = content

    topics_dir = _WIKI_DIR / "resources" / "by-topic"
    for md in sorted(topics_dir.glob("*.md")):
        if md.name == "_index.md":
            continue
        topic_entries[md.stem] = md.read_text()

    return {
        "educator_profiles": educator_profiles,
        "topic_entries": topic_entries,
        "topics_metadata": {},
    }


async def main():
    import argparse

    parser = argparse.ArgumentParser(description="Bootstrap the Pedagogy Wiki")
    parser.add_argument("--phase-a", action="store_true", help="Run Phase A only (extraction)")
    parser.add_argument("--skip-verify", action="store_true", help="Skip Phase C (verification)")
    parser.add_argument("--cached", action="store_true", help="Reuse cached Phase A data")
    parser.add_argument("--verify-only", action="store_true",
                        help="Re-run Phase C on existing wiki files (no LLM generation)")
    parser.add_argument("--discover", action="store_true",
                        help="Run Phase D on existing wiki files (pedagogical gap-filling)")
    parser.add_argument("--concept-map", action="store_true",
                        help="Generate concept-map.md via LLM (uses cached Phase A data)")
    parser.add_argument("--consolidate", action="store_true",
                        help="Merge/split resource pages to match concept-map.md")
    parser.add_argument("--download", action="store_true",
                        help="Download source content (blogs, transcripts) for wiki resources")
    parser.add_argument("--topic", type=str, default="",
                        help="Comma-separated topic slugs to scope operations")
    parser.add_argument("--stale-days", type=int, default=0,
                        help="Only process pages where Last Verified > N days ago")
    parser.add_argument("--file-source", nargs=3, metavar=("TOPIC", "URL", "TITLE"),
                        help="Manually file a source into a wiki topic page")
    args = parser.parse_args()

    topic_filter = [t.strip() for t in args.topic.split(",") if t.strip()] or None

    # -- File a source manually --
    if args.file_source:
        topic_slug, url, title = args.file_source
        sys.path.insert(0, str(_BACKEND_DIR))
        from app.services.course_generator import file_source_to_wiki
        ok = file_source_to_wiki(topic_slug, {
            "type": "blog",
            "title": title,
            "url": url,
            "why": "Manually filed via CLI",
            "confidence": "high",
        })
        print(f"{'Filed' if ok else 'FAILED'}: {title} → {topic_slug}")
        return

    # -- Stale-days filtering --
    if args.stale_days and args.stale_days > 0 and not topic_filter:
        from datetime import datetime, timedelta
        cutoff = datetime.now() - timedelta(days=args.stale_days)
        topics_dir = _WIKI_DIR / "resources" / "by-topic"
        stale = []
        for md in sorted(topics_dir.glob("*.md")):
            if md.name == "_index.md":
                continue
            content = md.read_text()
            import re as _re
            date_match = _re.search(r'Last Verified\s*\n(\d{4}-\d{2}-\d{2})', content)
            if date_match:
                verified = datetime.strptime(date_match.group(1), "%Y-%m-%d")
                if verified < cutoff:
                    stale.append(md.stem)
            else:
                stale.append(md.stem)
        if stale:
            topic_filter = stale
            print(f"Stale pages (>{args.stale_days} days): {len(stale)}")
            for s in stale:
                print(f"  {s}")
        else:
            print(f"No stale pages (all verified within {args.stale_days} days)")
            return

    # -- Concept map generation --
    if args.concept_map:
        if _CACHE_PATH.exists():
            with open(_CACHE_PATH) as f:
                phase_a_data = json.load(f)
        else:
            phase_a_data = phase_a()
            with open(_CACHE_PATH, "w") as f:
                json.dump(phase_a_data, f, indent=2, default=list)
        await generate_concept_map(phase_a_data)
        return

    # -- Consolidation --
    if args.consolidate:
        await consolidate_wiki()
        return

    # -- Download source content --
    if args.download:
        await download_wiki_content(topic_filter=topic_filter)
        return

    # -- Standalone modes (operate on existing wiki files) --
    if args.verify_only or args.discover:
        print("Loading existing wiki files...")
        phase_b_data = _load_wiki_from_disk()
        if topic_filter:
            phase_b_data["topic_entries"] = {
                k: v for k, v in phase_b_data["topic_entries"].items()
                if k in topic_filter
            }
            print(f"  Filtered to {len(phase_b_data['topic_entries'])} topics: {', '.join(topic_filter)}")
        print(f"  Loaded {len(phase_b_data['educator_profiles'])} educators, "
              f"{len(phase_b_data['topic_entries'])} topics")

        if args.verify_only:
            total_verify = sum(
                content.count("[VERIFY")
                for content in list(phase_b_data["educator_profiles"].values())
                + list(phase_b_data["topic_entries"].values())
            )
            print(f"  {total_verify} [VERIFY] flags found")
            phase_b_data = await phase_c(phase_b_data)

        if args.discover or (args.verify_only and args.discover):
            phase_b_data = await phase_d(phase_b_data)

        # Write updated files back
        for name, content in phase_b_data["educator_profiles"].items():
            slug = _slugify(name)
            (_WIKI_DIR / "educators" / f"{slug}.md").write_text(content)
        for slug, content in phase_b_data["topic_entries"].items():
            (_WIKI_DIR / "resources" / "by-topic" / f"{slug}.md").write_text(content)

        print(f"\n  Done. Updated files written to {_WIKI_DIR}")
        return

    # -- Full bootstrap --

    # Phase A
    if args.cached and _CACHE_PATH.exists():
        print("Loading cached Phase A data...")
        with open(_CACHE_PATH) as f:
            phase_a_data = json.load(f)
    else:
        phase_a_data = phase_a()
        with open(_CACHE_PATH, "w") as f:
            json.dump(phase_a_data, f, indent=2, default=list)
        print(f"\n  Cached Phase A data to {_CACHE_PATH}")

    if args.phase_a:
        print("\nPhase A complete. Run without --phase-a for full bootstrap.")
        return

    # Phase B
    phase_b_data = await phase_b(phase_a_data)

    # Phase C
    if not args.skip_verify:
        phase_b_data = await phase_c(phase_b_data)
    else:
        print("\n  Skipping Phase C (verification) — use without --skip-verify to verify.")

    # Write files
    write_wiki(phase_a_data, phase_b_data)

    print("\n" + "=" * 60)
    print("BOOTSTRAP COMPLETE")
    print("=" * 60)
    print(f"Wiki written to: {_WIKI_DIR}")
    print("Run with --discover for Phase D (pedagogical gap-filling).")


if __name__ == "__main__":
    asyncio.run(main())
