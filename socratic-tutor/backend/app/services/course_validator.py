"""
Course Creator — Phase 4 service.

Handles QA pair generation, QA evaluation, and publishing
(seeding to the production database).
"""

import json
import re
from datetime import datetime
from typing import AsyncGenerator, Optional

import httpx
from sqlmodel import Session, select

from ..config import get_settings
from ..models.learning import LearningPath, Module, Lesson

# ---------------------------------------------------------------------------
# LLM helper
# ---------------------------------------------------------------------------

async def _call_llm(prompt: str, *, max_tokens: int = 4096, temperature: float = 0.2) -> str:
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
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            f"{settings.llm_base_url}/v1/chat/completions",
            headers=headers,
            json=payload,
        )
        resp.raise_for_status()
    raw = resp.json()["choices"][0]["message"]["content"].strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()
    return raw


async def _call_llm_json(prompt: str, **kwargs) -> dict:
    raw = await _call_llm(prompt, **kwargs)
    return json.loads(raw)


# ---------------------------------------------------------------------------
# Phase 4: QA generation
# ---------------------------------------------------------------------------

QA_GENERATION_PROMPT = """\
You are generating diverse question-answer pairs for a technical tutoring \
system's evaluation suite.

LESSON TITLE: {title}
LESSON CONTENT:
{content}

REFERENCE KNOWLEDGE:
{chunks_text}

Generate 8-12 Q&A pairs that test different reasoning levels:
- factual: direct recall (2-3 pairs)
- conceptual: understanding relationships (2-3 pairs)
- procedural: how to do something (2-3 pairs)
- synthesis: combining information across topics and lessons (2-3 pairs)

For each pair produce:
- "question": a realistic student question
- "reference_answer": a complete, accurate answer (150-300 words)
- "reasoning_type": one of "factual", "conceptual", "procedural", "synthesis"
- "concepts_tested": array of concepts this question touches
- "tier": "basic" (covered in content alone) or "synthesis" (requires reference knowledge)

Return JSON: {{"qa_pairs": [...]}}
Return ONLY valid JSON.
"""


async def generate_qa(
    lessons: list,
    reference_kb_drafts: dict[str, str] | None = None,
) -> AsyncGenerator[str, None]:
    """Generate QA pairs for each lesson. Yields SSE events."""
    total = len(lessons)
    all_qa = []

    for i, lesson in enumerate(lessons):
        title = lesson.get("title", "Untitled")
        slug = lesson.get("slug", f"lesson-{i}")
        yield _sse({
            "type": "progress",
            "lesson_title": title,
            "index": i + 1,
            "total": total,
            "status": "generating_qa",
        })

        chunks_text = ""
        if reference_kb_drafts and slug in reference_kb_drafts:
            chunks_text = reference_kb_drafts[slug]

        prompt = QA_GENERATION_PROMPT.format(
            title=title,
            content=lesson.get("content", "")[:4000],
            chunks_text=chunks_text[:30000],
        )

        try:
            result = await _call_llm_json(prompt, max_tokens=8192)
            pairs = result.get("qa_pairs", [])
            for qi, pair in enumerate(pairs):
                pair["lesson_slug"] = slug
                pair["pair_index"] = qi
            all_qa.extend(pairs)
            yield _sse({
                "type": "progress",
                "lesson_title": title,
                "index": i + 1,
                "total": total,
                "status": "done",
                "qa_count": len(pairs),
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

    yield _sse({"type": "qa", "data": all_qa})
    yield _sse({"type": "done"})


# ---------------------------------------------------------------------------
# Phase 4: QA evaluation
# ---------------------------------------------------------------------------

QA_EVAL_PROMPT = """\
You are evaluating the quality of a Q&A pair for a technical tutoring system.

LESSON TITLE: {title}
LESSON CONTENT:
{content}

QUESTION: {question}
REFERENCE ANSWER: {answer}
REASONING TYPE: {reasoning_type}

Evaluate on these criteria (1-5 scale):
1. **Accuracy** — is the answer factually correct given the content?
2. **Completeness** — does it fully address the question?
3. **Relevance** — is the question relevant to the lesson?
4. **Clarity** — is both the question and answer clearly written?
5. **Difficulty** — is the difficulty appropriate for the reasoning type?

Return JSON:
{{
  "accuracy": int,
  "completeness": int,
  "relevance": int,
  "clarity": int,
  "difficulty_appropriate": int,
  "quality_score": float (weighted average 0-5),
  "issues": ["list of specific issues if any"],
  "recommendation": "keep" | "revise" | "reject"
}}

Return ONLY valid JSON.
"""


async def evaluate_qa(lessons: list, qa_pairs: list) -> AsyncGenerator[str, None]:
    """Evaluate QA pairs for quality. Yields SSE events."""
    total = len(qa_pairs)

    lessons_by_slug = {l.get("slug", f"lesson-{i}"): l for i, l in enumerate(lessons)}

    for i, pair in enumerate(qa_pairs):
        slug = pair.get("lesson_slug", "")
        lesson = lessons_by_slug.get(slug, {})
        yield _sse({
            "type": "progress",
            "index": i + 1,
            "total": total,
            "question": pair.get("question", "")[:80],
            "status": "evaluating",
        })

        prompt = QA_EVAL_PROMPT.format(
            title=lesson.get("title", ""),
            content=lesson.get("content", "")[:3000],
            question=pair.get("question", ""),
            answer=pair.get("reference_answer", ""),
            reasoning_type=pair.get("reasoning_type", ""),
        )

        try:
            result = await _call_llm_json(prompt, max_tokens=1024)
            pair["evaluation"] = result
            pair["quality_score"] = result.get("quality_score", 0)
            yield _sse({
                "type": "progress",
                "index": i + 1,
                "total": total,
                "status": "done",
                "quality_score": pair["quality_score"],
                "recommendation": result.get("recommendation", ""),
            })
        except Exception as e:
            pair["evaluation"] = {"error": str(e)}
            pair["quality_score"] = 0
            yield _sse({
                "type": "progress",
                "index": i + 1,
                "total": total,
                "status": "error",
                "error": str(e),
            })

    yield _sse({"type": "evaluation", "data": qa_pairs})
    yield _sse({"type": "done"})


# ---------------------------------------------------------------------------
# Publish — seed to production database
# ---------------------------------------------------------------------------

def _slugify(text: str) -> str:
    slug = text.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")[:80]


def _build_modules_and_lessons(
    path_id: str,
    modules_data: list[dict],
    lessons_dict: dict,
    db_session: Session,
) -> int:
    """Create Module + Lesson rows for a LearningPath. Returns lesson count."""
    lesson_count = 0
    for mod_idx, mod_data in enumerate(modules_data):
        module = Module(
            title=mod_data["title"],
            slug=_slugify(mod_data["title"]),
            order_index=mod_data.get("order_index", mod_idx),
            learning_path_id=path_id,
        )
        db_session.add(module)
        db_session.flush()

        lesson_slugs = mod_data.get("lesson_slugs", [])
        if not lesson_slugs:
            for les_obj in mod_data.get("lessons", []):
                if isinstance(les_obj, dict) and les_obj.get("slug"):
                    lesson_slugs.append(les_obj["slug"])
                elif isinstance(les_obj, str):
                    lesson_slugs.append(les_obj)
        for order_idx, lesson_slug in enumerate(lesson_slugs):
            les = lessons_dict.get(lesson_slug, {})
            img_meta = les.get("image_metadata")
            src_used = les.get("sources_used")
            lesson = Lesson(
                title=les.get("title", lesson_slug),
                slug=lesson_slug,
                order_index=order_idx,
                module_id=module.id,
                summary=les.get("summary", ""),
                concepts=json.dumps(les.get("concepts", [])),
                content=les.get("content", ""),
                reference_kb=les.get("reference_kb", ""),
                youtube_id=les.get("youtube_id"),
                video_title=les.get("video_title"),
                sources_used=json.dumps(src_used) if src_used else None,
                image_metadata=json.dumps(img_meta) if img_meta else None,
            )
            db_session.add(lesson)
            lesson_count += 1
    return lesson_count


def publish_course(
    draft_data: dict,
    db_session: Session,
    *,
    user_id: str | None = None,
    existing_path_id: str | None = None,
) -> dict:
    """Seed (or update) a draft into the production tables.

    If *existing_path_id* is supplied the existing LearningPath is updated
    in-place: its metadata is patched and old modules/lessons are replaced.
    """
    outline = draft_data.get("outline", {})
    lessons_dict = draft_data.get("lessons", {})
    qa_data = draft_data.get("validation", {}).get("qa_pairs", {})

    title = outline.get("title", draft_data.get("title", "Untitled Course"))
    modules_data = outline.get("modules", [])

    # ── Republish: update existing path ────────────────────────────
    if existing_path_id:
        path = db_session.get(LearningPath, existing_path_id)
        if path:
            path.title = title
            path.slug = _slugify(title)
            path.description = outline.get("description", "")
            path.level = outline.get("level", path.level)

            # Delete old modules (cascades to lessons via DB or manual)
            old_modules = db_session.exec(
                select(Module).where(Module.learning_path_id == path.id)
            ).all()
            for old_mod in old_modules:
                old_lessons = db_session.exec(
                    select(Lesson).where(Lesson.module_id == old_mod.id)
                ).all()
                for old_les in old_lessons:
                    db_session.delete(old_les)
                db_session.delete(old_mod)
            db_session.flush()

            lesson_count = _build_modules_and_lessons(
                path.id, modules_data, lessons_dict, db_session,
            )
            db_session.commit()

            kb_count = sum(1 for l in lessons_dict.values() if l.get("reference_kb"))
            return {
                "learning_path_id": path.id,
                "slug": path.slug,
                "module_count": len(modules_data),
                "lesson_count": lesson_count,
                "kb_lessons": kb_count,
                "qa_approved": len(qa_data.get("approved", [])),
                "republished": True,
            }

    # ── First publish: create new path ─────────────────────────────
    slug = _slugify(title)
    path = LearningPath(
        title=title,
        slug=slug,
        description=outline.get("description", ""),
        level=outline.get("level", "beginner"),
        created_by=user_id,
        visibility="private" if user_id else "public",
    )
    db_session.add(path)
    db_session.flush()

    lesson_count = _build_modules_and_lessons(
        path.id, modules_data, lessons_dict, db_session,
    )
    db_session.commit()

    kb_count = sum(1 for l in lessons_dict.values() if l.get("reference_kb"))
    return {
        "learning_path_id": path.id,
        "slug": slug,
        "module_count": len(modules_data),
        "lesson_count": lesson_count,
        "kb_lessons": kb_count,
        "qa_approved": len(qa_data.get("approved", [])),
    }


def _sse(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"
