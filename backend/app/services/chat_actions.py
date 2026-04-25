"""Chat co-pilot action executors.

Each executor takes draft data (and action-specific params), performs its
work, and returns a result dict with {action, status, summary, ...}.
"""

from __future__ import annotations

import json
import logging
import re

from .course_enricher import _search

logger = logging.getLogger(__name__)

AUTO_APPLY_ACTIONS = {"research_topic", "modify_outline", "edit_lesson_content"}
CONFIRM_ACTIONS = {"regenerate_lesson"}  # heavy — requires explicit user confirmation
ALL_ACTIONS = AUTO_APPLY_ACTIONS | CONFIRM_ACTIONS


def classify_action(action_type: str) -> str:
    """Return 'auto' or 'confirm' for a given action type."""
    if action_type in AUTO_APPLY_ACTIONS:
        return "auto"
    return "confirm"


def parse_draft_actions(response_text: str) -> list[dict] | None:
    """Extract draft_actions from fenced JSON in an LLM response.

    Looks for ```json blocks containing a "draft_actions" key.
    Falls back to legacy "outline_actions" and wraps them as modify_outline.
    Returns None if no actions found.
    """
    pattern = r"```json\s*\n([\s\S]*?)\n```"
    matches = re.findall(pattern, response_text)

    for match in matches:
        try:
            data = json.loads(match)
        except json.JSONDecodeError:
            continue

        if isinstance(data, dict):
            if "draft_actions" in data and isinstance(data["draft_actions"], list):
                return data["draft_actions"]
            if "outline_actions" in data and isinstance(data["outline_actions"], list):
                return [{
                    "action": "modify_outline",
                    "outline_actions": data["outline_actions"],
                }]

    return None


# ---------------------------------------------------------------------------
# Auto-apply executors
# ---------------------------------------------------------------------------

async def execute_research_topic(query: str) -> dict:
    """Run a web search. Returns results but does NOT mutate draft data."""
    result = await _search(query)

    if result.get("error"):
        return {
            "action": "research_topic",
            "status": "error",
            "summary": f"Search failed: {result['error']}",
        }

    citations = result.get("citations", [])
    citation_summary = ", ".join(
        c if isinstance(c, str) else c.get("url", c.get("title", ""))
        for c in citations[:5]
    )

    return {
        "action": "research_topic",
        "status": "success",
        "summary": f"Found {len(citations)} sources for \"{query}\"",
        "query": query,
        "content": result.get("content", "")[:3000],
        "citations": citations[:10],
    }


# ---------------------------------------------------------------------------
# Shared LLM helper
# ---------------------------------------------------------------------------

async def _llm_edit(system: str, user: str, *, max_tokens: int = 4096) -> str:
    """Single LLM call for editing tasks. Returns raw text response."""
    from .course_generator import _call_llm
    import httpx
    from ..config import get_settings

    settings = get_settings()
    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.llm_model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.2,
    }
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            f"{settings.llm_base_url}/chat/completions",
            headers=headers,
            json=payload,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()


# ---------------------------------------------------------------------------
# Auto-apply executors
# ---------------------------------------------------------------------------

async def execute_modify_outline(action: dict, draft_data: dict) -> dict:
    """Apply outline changes via a targeted LLM call.

    The LLM receives the current outline JSON and a natural-language instruction,
    and returns the modified outline JSON. This replaces the fragile deterministic
    sub-action parser.
    """
    outline = draft_data.get("outline")
    if not outline:
        return {"action": "modify_outline", "status": "error", "summary": "No outline exists yet"}

    instruction = action.get("instruction", "")
    if not instruction:
        return {"action": "modify_outline", "status": "error", "summary": "No instruction provided"}

    system = (
        "You are a course outline editor. You will be given a course outline in JSON "
        "and an instruction describing a structural change to make. "
        "Apply the change and return ONLY the modified outline JSON — no explanation, no markdown fences. "
        "Preserve all existing fields. Each module must have: title, order_index, lessons (array of objects "
        "with title, slug, summary, concepts). Slugs must be lowercase-hyphenated."
    )
    user = f"Instruction: {instruction}\n\nCurrent outline:\n{json.dumps(outline, indent=2)}"

    try:
        raw = await _llm_edit(system, user)
        # Strip any accidental markdown fences
        raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
        raw = re.sub(r"\s*```$", "", raw.strip())
        new_outline = json.loads(raw)
    except Exception as e:
        logger.warning("LLM outline edit failed: %s", e)
        return {"action": "modify_outline", "status": "error", "summary": f"Outline edit failed: {e}"}

    # Sync lessons dict with the new outline: add new, update existing, remove stale
    lessons_dict = draft_data.setdefault("lessons", {})
    new_slugs: set[str] = set()
    for mod in new_outline.get("modules", []):
        for les in mod.get("lessons", []):
            slug = les.get("slug", "")
            if not slug:
                continue
            new_slugs.add(slug)
            if slug not in lessons_dict:
                lessons_dict[slug] = {
                    "title": les.get("title", ""),
                    "slug": slug,
                    "summary": les.get("summary", ""),
                    "concepts": les.get("concepts", []),
                    "status": "outline",
                }
            else:
                lessons_dict[slug]["title"] = les.get("title", lessons_dict[slug]["title"])
                lessons_dict[slug]["summary"] = les.get("summary", lessons_dict[slug]["summary"])
                lessons_dict[slug]["concepts"] = les.get("concepts", lessons_dict[slug]["concepts"])

    for stale in list(lessons_dict.keys()):
        if stale not in new_slugs:
            del lessons_dict[stale]

    # Reindex order_index
    for mi, mod in enumerate(new_outline.get("modules", [])):
        mod["order_index"] = mi

    draft_data["outline"] = new_outline

    old_mod_count = len(outline.get("modules", []))
    new_mod_count = len(new_outline.get("modules", []))
    old_lesson_count = sum(len(m.get("lessons", [])) for m in outline.get("modules", []))
    new_lesson_count = sum(len(m.get("lessons", [])) for m in new_outline.get("modules", []))

    summary = f"Outline updated ({old_mod_count}→{new_mod_count} modules, {old_lesson_count}→{new_lesson_count} lessons)"
    return {"action": "modify_outline", "status": "success", "summary": summary}


async def execute_edit_lesson_content(
    slug: str,
    target: str,
    instruction: str,
    draft_data: dict,
) -> dict:
    """Apply a targeted edit to lesson notes or reference KB via a single LLM call.

    This is much faster than full regeneration — the LLM receives the existing
    markdown and applies a specific change, without any wiki research.
    target: 'notes' | 'reference_kb'
    """
    lessons_dict = draft_data.get("lessons", {})
    if slug not in lessons_dict:
        return {"action": "edit_lesson_content", "status": "error", "summary": f"Lesson '{slug}' not found"}

    lesson = lessons_dict[slug]
    field = "content" if target == "notes" else "reference_kb"
    existing = lesson.get(field, "")

    if not existing:
        return {
            "action": "edit_lesson_content",
            "status": "error",
            "summary": f"Lesson '{slug}' has no {target} content to edit",
        }

    target_label = "student-facing lesson notes" if target == "notes" else "tutor reference knowledge base"
    system = (
        f"You are a markdown editor for educational content. "
        f"You will be given {target_label} in markdown and an instruction for a specific edit. "
        f"Apply the edit precisely and return ONLY the complete modified markdown — "
        f"no explanation, no commentary, no fences. Preserve all sections, headings, "
        f"and formatting that were not part of the edit."
    )
    user = f"Instruction: {instruction}\n\n---\n\n{existing}"

    try:
        modified = await _llm_edit(system, user, max_tokens=8192)
        # Strip accidental fences
        modified = re.sub(r"^```(?:markdown|md)?\s*\n?", "", modified)
        modified = re.sub(r"\n?```$", "", modified)
        modified = modified.strip()
    except Exception as e:
        logger.warning("LLM lesson edit failed for %r: %s", slug, e)
        return {"action": "edit_lesson_content", "status": "error", "summary": f"Edit failed: {e}"}

    lesson[field] = modified
    old_words = len(existing.split())
    new_words = len(modified.split())
    title = lesson.get("title", slug)

    return {
        "action": "edit_lesson_content",
        "status": "success",
        "summary": f"Edited {target} for \"{title}\" ({old_words}→{new_words} words)",
        "slug": slug,
        "target": target,
    }


async def execute_regenerate_lesson(slug: str, draft_data: dict) -> dict:
    """Re-generate content for a single lesson. Overwrites existing content."""
    from .course_generator import generate_content

    outline = draft_data.get("outline")
    if not outline:
        return {"action": "regenerate_lesson", "status": "error", "summary": "No outline"}

    lessons_dict = draft_data.get("lessons", {})
    if slug not in lessons_dict:
        return {"action": "regenerate_lesson", "status": "error", "summary": f"Lesson '{slug}' not found"}

    ref_kb: dict[str, str] = {}
    for s, l in lessons_dict.items():
        kb = l.get("reference_kb", "")
        if kb:
            ref_kb[s] = kb

    outline_with_lessons = {**outline, "_lessons_dict": lessons_dict}

    generated_lesson = None
    gen = generate_content(
        outline_with_lessons,
        draft_data.get("source_text", ""),
        draft_data.get("source_type", "prompt"),
        existing_lessons=None,
        reference_kb=ref_kb or None,
    )

    async for event_str in gen:
        if not event_str.startswith("data: "):
            continue
        try:
            evt = json.loads(event_str[6:].strip())
        except json.JSONDecodeError:
            continue

        if evt.get("type") == "progress" and evt.get("status") == "done" and evt.get("lesson"):
            lesson = evt["lesson"]
            if lesson.get("slug") == slug:
                generated_lesson = lesson
                break

    if not generated_lesson:
        return {"action": "regenerate_lesson", "status": "error", "summary": f"Generation didn't produce lesson '{slug}'"}

    lesson_entry = lessons_dict[slug]
    lesson_entry["content"] = generated_lesson.get("content", "")
    lesson_entry["summary"] = generated_lesson.get("summary", lesson_entry.get("summary", ""))
    lesson_entry["concepts"] = generated_lesson.get("concepts", lesson_entry.get("concepts", []))
    lesson_entry["sources_used"] = generated_lesson.get("sources_used", [])
    if generated_lesson.get("reference_kb"):
        lesson_entry["reference_kb"] = generated_lesson["reference_kb"]
    lesson_entry["status"] = "content_done"

    word_count = len((generated_lesson.get("content", "")).split())
    return {
        "action": "regenerate_lesson",
        "status": "success",
        "summary": f"Regenerated lesson \"{lesson_entry.get('title', slug)}\" — {word_count:,} words",
        "slug": slug,
        "word_count": word_count,
    }


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

async def execute_action(action: dict, draft_data: dict) -> dict:
    """Route an action dict to the appropriate executor."""
    action_type = action.get("action", "")

    if action_type == "research_topic":
        query = action.get("query", "")
        if not query:
            return {"action": action_type, "status": "error", "summary": "No query provided"}
        return await execute_research_topic(query)

    elif action_type == "modify_outline":
        return await execute_modify_outline(action, draft_data)

    elif action_type == "edit_lesson_content":
        slug = action.get("slug", "")
        target = action.get("target", "notes")
        instruction = action.get("instruction", "")
        if not slug:
            return {"action": action_type, "status": "error", "summary": "No slug provided"}
        if not instruction:
            return {"action": action_type, "status": "error", "summary": "No instruction provided"}
        if target not in ("notes", "reference_kb"):
            return {"action": action_type, "status": "error", "summary": f"Invalid target '{target}' — must be 'notes' or 'reference_kb'"}
        return await execute_edit_lesson_content(slug, target, instruction, draft_data)

    elif action_type == "regenerate_lesson":
        slug = action.get("slug", "")
        if not slug:
            return {"action": action_type, "status": "error", "summary": "No slug provided"}
        return await execute_regenerate_lesson(slug, draft_data)

    return {"action": action_type, "status": "error", "summary": f"Unknown action type: {action_type}"}
