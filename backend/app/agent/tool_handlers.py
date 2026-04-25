import asyncio
import json
import logging
import re
from sqlmodel import Session, select
from ..db import engine
from ..models.learning import Lesson
from .context import TutorContext

logger = logging.getLogger(__name__)


async def execute_tool(name: str, tool_input: dict, context: TutorContext) -> dict:
    if name == "search_web":
        return await _search_web(tool_input["query"])
    elif name == "get_lesson_context":
        return await asyncio.to_thread(
            _get_lesson_context,
            lesson_id=tool_input.get("lesson_id"),
            lesson_slug=tool_input.get("lesson_slug"),
        )
    elif name == "get_lesson_transcript":
        return await asyncio.to_thread(
            _get_lesson_transcript,
            lesson_id=tool_input.get("lesson_id"),
            lesson_slug=tool_input.get("lesson_slug"),
            context=context,
        )
    elif name == "get_lesson_reference_kb":
        return await asyncio.to_thread(
            _get_lesson_reference_kb,
            lesson_id=tool_input.get("lesson_id"),
            lesson_slug=tool_input.get("lesson_slug"),
        )
    elif name == "get_curated_resources":
        return _get_curated_resources(tool_input.get("concepts", []))
    elif name == "get_relevant_images":
        return _get_relevant_images(tool_input.get("concepts", []))
    elif name == "get_user_progress":
        return _get_user_progress(context)
    else:
        return {"error": f"Unknown tool: {name}"}


async def _search_web(query: str) -> dict:
    """Delegate to the enricher's _search which handles NVIDIA / Perplexity routing.

    Adapts the enricher's response format (content + citations) into the
    result-list format the tutor agent expects.
    """
    from ..config import get_settings
    if not get_settings().search_enabled:
        return {
            "query": query,
            "content": "Web search is not configured. Please answer from your knowledge and the lesson content.",
            "results": [],
        }
    try:
        from ..services.course_enricher import _search, _classify_source_url

        data = await _search(query)

        if data.get("error"):
            return {"error": data["error"], "results": []}

        results = []
        for c in data.get("citations", []):
            url = c.get("url", "") if isinstance(c, dict) else str(c)
            title = c.get("title", "") if isinstance(c, dict) else ""
            if url:
                results.append({
                    "title": title,
                    "url": url,
                    "source_type": _classify_source_url(url),
                })

        return {
            "query": query,
            "content": data.get("content", ""),
            "results": results,
        }
    except Exception as e:
        return {"error": str(e), "results": []}


def _get_lesson_context(lesson_id: str | None = None, lesson_slug: str | None = None) -> dict:
    if not lesson_id and not lesson_slug:
        return {"error": "Provide either lesson_slug or lesson_id"}

    with Session(engine) as session:
        lesson = None
        if lesson_slug:
            lesson = session.exec(
                select(Lesson).where(Lesson.slug == lesson_slug)
            ).first()
        elif lesson_id:
            lesson = session.get(Lesson, lesson_id)

        if not lesson:
            return {"error": f"Lesson not found for slug='{lesson_slug}' / id='{lesson_id}'"}

        try:
            concepts = json.loads(lesson.concepts)
        except (json.JSONDecodeError, TypeError):
            concepts = []
        return {
            "lesson_id": lesson.id,
            "slug": lesson.slug,
            "title": lesson.title,
            "summary": lesson.summary,
            "concepts": concepts,
            "content": lesson.content,
        }


def _get_lesson_transcript(
    lesson_id: str | None = None,
    lesson_slug: str | None = None,
    context: TutorContext | None = None,
) -> dict:
    # Default to current lesson if no identifier provided
    if not lesson_id and not lesson_slug and context:
        lesson_id = context.lesson_id

    if not lesson_id and not lesson_slug:
        return {"error": "Provide either lesson_slug or lesson_id"}

    with Session(engine) as session:
        lesson = None
        if lesson_slug:
            lesson = session.exec(
                select(Lesson).where(Lesson.slug == lesson_slug)
            ).first()
        elif lesson_id:
            lesson = session.get(Lesson, lesson_id)

        if not lesson:
            return {"error": f"Lesson not found for slug='{lesson_slug}' / id='{lesson_id}'"}

        if not lesson.transcript:
            return {
                "lesson_id": lesson.id,
                "title": lesson.title,
                "transcript": None,
                "message": "No video transcript available for this lesson.",
            }

        return {
            "lesson_id": lesson.id,
            "title": lesson.title,
            "vimeo_url": lesson.vimeo_url,
            "transcript": lesson.transcript,
        }


def _get_lesson_reference_kb(
    lesson_id: str | None = None, lesson_slug: str | None = None
) -> dict:
    if not lesson_id and not lesson_slug:
        return {"error": "Provide either lesson_slug or lesson_id"}

    with Session(engine) as session:
        lesson = None
        if lesson_slug:
            lesson = session.exec(
                select(Lesson).where(Lesson.slug == lesson_slug)
            ).first()
        elif lesson_id:
            lesson = session.get(Lesson, lesson_id)

        if not lesson:
            return {"error": f"Lesson not found for slug='{lesson_slug}' / id='{lesson_id}'"}

        if not lesson.reference_kb:
            return {
                "lesson_id": lesson.id,
                "title": lesson.title,
                "reference_kb": None,
                "message": "No reference knowledge base available for this lesson.",
            }

        return {
            "lesson_id": lesson.id,
            "title": lesson.title,
            "reference_kb": lesson.reference_kb,
        }


def _get_curated_resources(concepts: list[str]) -> dict:
    """Return curated teaching resources from the pedagogy wiki."""
    try:
        from ..services.course_generator import load_wiki_context
    except Exception:
        return {"error": "Wiki context not available", "resources": []}

    if not concepts:
        return {"error": "No concepts provided", "resources": []}

    wiki_ctx = load_wiki_context(concepts)
    resources: list[dict] = []
    seen_ids: set[str] = set()

    _BOLD_RE = re.compile(r'^- \*\*([^*]+)\*\*\s*[—–-]\s*["\']?(.+?)["\']?\s*$')

    for slug in wiki_ctx.get("topics", []):
        for yt_id, title_line in wiki_ctx.get("youtube_ids", {}).get(slug, []):
            if yt_id in seen_ids:
                continue
            seen_ids.add(yt_id)
            m = _BOLD_RE.match(title_line) if title_line else None
            resources.append({
                "type": "video",
                "youtube_id": yt_id,
                "educator": m.group(1).strip() if m else "",
                "title": m.group(2).strip() if m else f"Video {yt_id}",
                "url": f"https://www.youtube.com/watch?v={yt_id}",
                "topic": slug,
                "has_transcript": any(
                    f["file"] == f"yt-{yt_id}.txt"
                    for files in wiki_ctx.get("source_content", {}).values()
                    for f in files
                ),
            })

        for title_line, url in wiki_ctx.get("recommended_reading", {}).get(slug, []):
            if url in seen_ids:
                continue
            seen_ids.add(url)
            m = _BOLD_RE.match(title_line) if title_line else None
            resources.append({
                "type": "blog",
                "educator": m.group(1).strip() if m else "",
                "title": m.group(2).strip() if m else url,
                "url": url,
                "topic": slug,
            })

    return {
        "topics": wiki_ctx.get("topics", []),
        "resource_count": len(resources),
        "resources": resources[:8],
    }


_MAX_TUTOR_IMAGES = 6


def _get_relevant_images(concepts: list[str]) -> dict:
    """Return curated educational images matched to concepts from the wiki."""
    try:
        from ..services.course_generator import load_wiki_context
    except Exception:
        return {"error": "Wiki context not available", "images": []}

    if not concepts:
        return {"error": "No concepts provided", "images": []}

    wiki_ctx = load_wiki_context(concepts)
    all_images = wiki_ctx.get("images", {})
    if not all_images:
        return {"concepts": concepts, "image_count": 0, "images": []}

    concept_set = {c.lower() for c in concepts}
    scored: list[tuple[int, str, dict]] = []

    for slug in wiki_ctx.get("topics", []):
        for img in all_images.get(slug, []):
            if not img.get("file"):
                continue
            img_concepts = {c.lower() for c in img.get("concepts", [])}
            overlap = len(concept_set & img_concepts)
            if overlap > 0:
                scored.append((overlap, slug, img))

    if not scored:
        return {"concepts": concepts, "image_count": 0, "images": []}

    scored.sort(key=lambda t: t[0], reverse=True)
    selected = scored[:_MAX_TUTOR_IMAGES]

    results = []
    for _score, slug, img in selected:
        results.append({
            "path": f"/api/wiki-images/{slug}/images/{img['file']}",
            "caption": img.get("suggested_caption", ""),
            "description": img.get("description", ""),
            "when_to_show": img.get("when_to_show", ""),
            "concepts": img.get("concepts", [])[:6],
            "topic": slug,
        })

    return {
        "concepts": concepts,
        "image_count": len(results),
        "images": results,
    }


def _get_user_progress(context: TutorContext) -> dict:
    return {
        "current_lesson": context.lesson_title,
        "completed_lessons": context.completed_lesson_titles,
        "total_completed": len(context.completed_lesson_titles),
    }
