import json
import logging
import re
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlmodel import Session, select

from ..db import get_session, engine
from ..deps import get_current_user
from ..models.user import User
from ..models.course_draft import CourseDraft
from ..schemas.course_creator import (
    CreateDraftRequest,
    UpdateOutlineRequest,
    UpdateContentRequest,
    UpdateCleanupRequest,
    UpdateReferenceKbDraftsRequest,
    UpdateQARequest,
    DraftChatRequest,
    DraftSummaryResponse,
    DraftDetailResponse,
)
from ..services.course_generator import (
    generate_outline,
    generate_content,
    generate_reference_kb_from_wiki,
    suggest_wiki_enrichment,
    assess_wiki_coverage,
    assess_wiki_coverage_stream,
    ensure_wiki_coverage_stream,
    file_structural_note,
    run_cleanup,
    check_outline_coverage,
    load_wiki_context,
)
from ..services.wiki_downloader import download_source
from ..services.course_validator import generate_qa, evaluate_qa, publish_course

router = APIRouter(prefix="/course-creator", tags=["course-creator"])


def _slugify(title: str) -> str:
    slug = title.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")[:80]


_PHASE_ALIASES = {"enrichment": "research", "validation": "reviewing", "content": "reviewing"}


def _normalize_phase(phase: str) -> str:
    """Map legacy phase names to current ones."""
    return _PHASE_ALIASES.get(phase, phase)


# ---------------------------------------------------------------------------
# Per-lesson data model helpers
# ---------------------------------------------------------------------------

def _migrate_draft_data(data: dict) -> dict:
    """Migrate legacy draft data to the per-lesson model if needed.

    Legacy format:
      data.outline = {title, modules: [{title, lessons: [{slug, ...}]}]}
      data.research = {queries, search_results, evaluations, curated_sources}
      data.content  = {reference_kb: {slug: md}, lessons: [{slug, ...}]}

    New format:
      data.outline = {title, modules: [{title, lesson_slugs: [slug]}]}
      data.lessons  = {slug: {title, slug, summary, concepts, status, research, reference_kb, content}}
    """
    if data.get("lessons") and isinstance(data["lessons"], dict):
        return data

    outline = data.get("outline", {})
    if not outline.get("modules"):
        return data

    first_module = outline["modules"][0]
    if "lesson_slugs" in first_module:
        return data

    lessons_dict: dict[str, dict] = {}
    new_modules = []

    research = data.get("research", {}) or data.get("enrichment", {}) or {}
    queries = research.get("queries", {}).get("by_lesson", {}) or research.get("generated_queries", {})
    search_results = research.get("search_results", {})
    evaluations = research.get("evaluations", {})
    curated_sources = research.get("curated_sources", {})

    ref_kb = (
        data.get("content", {}).get("reference_kb", {})
        or data.get("enrichment", {}).get("reference_kb_drafts", {})
    )
    content_lessons = data.get("content", {}).get("lessons", [])
    content_by_slug = {l.get("slug", ""): l for l in content_lessons if l.get("slug")}

    for module in outline["modules"]:
        slugs = []
        for lesson in module.get("lessons", []):
            slug = lesson.get("slug", "")
            if not slug:
                continue
            slugs.append(slug)

            status = "outline"
            lesson_research = {}
            if slug in queries:
                lesson_research["queries"] = queries[slug]
            if slug in search_results:
                lesson_research["search_results"] = search_results[slug]
            if slug in evaluations:
                lesson_research["evaluations"] = evaluations[slug]
            if slug in curated_sources:
                lesson_research["curated_sources"] = curated_sources[slug]
                status = "researched"

            kb_md = ref_kb.get(slug, "")
            if kb_md:
                status = "kb_done"

            content_data = content_by_slug.get(slug, {})
            content_md = content_data.get("content", "")
            if content_md:
                status = "content_done"

            lessons_dict[slug] = {
                "title": lesson.get("title", ""),
                "slug": slug,
                "summary": lesson.get("summary", content_data.get("summary", "")),
                "concepts": lesson.get("concepts", content_data.get("concepts", [])),
                "status": status,
                "research": lesson_research if lesson_research else {},
                "reference_kb": kb_md,
                "content": content_md,
            }

        new_modules.append({
            "title": module.get("title", ""),
            "order_index": module.get("order_index", 0),
            "lesson_slugs": slugs,
        })

    data["outline"] = {
        "title": outline.get("title", data.get("title", "")),
        "description": outline.get("description", ""),
        "level": outline.get("level", ""),
        "modules": new_modules,
    }
    data["lessons"] = lessons_dict

    for key in ("research", "enrichment", "content"):
        data.pop(key, None)

    return data


def _get_all_lessons_list(data: dict) -> list[dict]:
    """Get all lessons as a flat list (for pipeline functions)."""
    return list(data.get("lessons", {}).values())


def _get_outline_slugs(data: dict) -> set[str]:
    """Return the set of lesson slugs referenced by the current outline."""
    outline = data.get("outline", {})
    slugs: set[str] = set()
    for module in outline.get("modules", []):
        for slug in module.get("lesson_slugs", []):
            slugs.add(slug)
        for lesson in module.get("lessons", []):
            s = lesson.get("slug", "")
            if s:
                slugs.add(s)
    return slugs


def _compute_draft_phase(data: dict) -> str:
    """Compute the draft-level phase from per-lesson statuses."""
    lessons = data.get("lessons", {})
    if not lessons:
        return "research"
    statuses = {l.get("status", "outline") for l in lessons.values()}
    if all(s == "content_done" for s in statuses):
        return "validation"
    if all(s in ("kb_done", "content_done") for s in statuses):
        return "content"
    if all(s in ("researched", "kb_done", "content_done") for s in statuses):
        return "content"
    if all(s == "outline" for s in statuses):
        return "structure"
    return "content"


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

@router.post("/drafts", response_model=DraftSummaryResponse)
def create_draft(
    req: CreateDraftRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    draft_data: dict = {"source_text": req.source_text}
    if req.source_url:
        draft_data["source_url"] = req.source_url
    draft = CourseDraft(
        user_id=user.id,
        title=req.title,
        slug=_slugify(req.title),
        source_type=req.source_type,
        data=json.dumps(draft_data),
    )
    session.add(draft)
    session.commit()
    session.refresh(draft)
    return draft


@router.get("/drafts", response_model=List[DraftSummaryResponse])
def list_drafts(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    drafts = session.exec(
        select(CourseDraft)
        .where(CourseDraft.user_id == user.id)
        .order_by(CourseDraft.updated_at.desc())
    ).all()
    return drafts


@router.get("/drafts/{draft_id}", response_model=DraftDetailResponse)
def get_draft(
    draft_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = _migrate_draft_data(json.loads(draft.data))
    phase = _normalize_phase(draft.phase)
    return DraftDetailResponse(
        id=draft.id,
        title=draft.title,
        slug=draft.slug,
        source_type=draft.source_type,
        phase=phase,
        stage=draft.stage,
        data=data,
        created_at=draft.created_at,
        updated_at=draft.updated_at,
    )


@router.delete("/drafts/{draft_id}")
def delete_draft(
    draft_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    session.delete(draft)
    session.commit()
    return {"ok": True}


@router.patch("/drafts/{draft_id}/patch")
def patch_draft(
    draft_id: str,
    body: dict,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Incrementally merge keys into draft.data without overwriting the rest."""
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = json.loads(draft.data)
    for key, value in body.items():
        if key in ("phase", "stage"):
            setattr(draft, key, value)
        else:
            data[key] = value
    draft.data = json.dumps(data)
    draft.updated_at = datetime.utcnow()
    session.commit()
    return {"ok": True}


@router.get("/drafts/{draft_id}/export")
def export_draft(
    draft_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = _migrate_draft_data(json.loads(draft.data))
    return {
        "schema_version": "2.0",
        "title": draft.title,
        "slug": draft.slug,
        "source_type": draft.source_type,
        "phase": _normalize_phase(draft.phase),
        "stage": draft.stage,
        "created_at": draft.created_at.isoformat(),
        "updated_at": draft.updated_at.isoformat(),
        **data,
    }


# ---------------------------------------------------------------------------
# Outline
# ---------------------------------------------------------------------------

@router.put("/drafts/{draft_id}/outline")
def save_outline(
    draft_id: str,
    req: UpdateOutlineRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = json.loads(draft.data)
    raw_outline = req.outline

    new_modules = []
    lessons_dict = data.get("lessons", {})

    for module in raw_outline.get("modules", []):
        slugs = []
        for lesson in module.get("lessons", []):
            slug = lesson.get("slug", "")
            if not slug:
                continue
            slugs.append(slug)
            if slug not in lessons_dict:
                lessons_dict[slug] = {
                    "title": lesson.get("title", ""),
                    "slug": slug,
                    "summary": lesson.get("summary", ""),
                    "concepts": lesson.get("concepts", []),
                    "status": "outline",
                    "research": {},
                    "reference_kb": "",
                    "content": "",
                }
            else:
                lessons_dict[slug]["title"] = lesson.get("title", lessons_dict[slug]["title"])
                lessons_dict[slug]["summary"] = lesson.get("summary", lessons_dict[slug]["summary"])
                lessons_dict[slug]["concepts"] = lesson.get("concepts", lessons_dict[slug]["concepts"])
        new_modules.append({
            "title": module.get("title", ""),
            "order_index": module.get("order_index", 0),
            "lesson_slugs": slugs,
        })

    all_slugs = {s for m in new_modules for s in m.get("lesson_slugs", [])}
    for slug in list(lessons_dict.keys()):
        if slug not in all_slugs:
            del lessons_dict[slug]

    data["outline"] = {
        "title": raw_outline.get("title", ""),
        "description": raw_outline.get("description", ""),
        "level": raw_outline.get("level", ""),
        "modules": new_modules,
    }
    data["lessons"] = lessons_dict

    draft.data = json.dumps(data)
    draft.phase = "content"
    draft.stage = "generate_lessons"
    draft.updated_at = datetime.utcnow()
    session.commit()
    return {"ok": True, "phase": draft.phase, "stage": draft.stage}


# ---------------------------------------------------------------------------
# Content & Knowledge
# ---------------------------------------------------------------------------

@router.put("/drafts/{draft_id}/content")
def save_content(
    draft_id: str,
    req: UpdateContentRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = _migrate_draft_data(json.loads(draft.data))
    for lesson_data in req.lessons:
        slug = lesson_data.get("slug", "")
        lesson = data.get("lessons", {}).get(slug)
        if lesson:
            lesson["content"] = lesson_data.get("content", "")
            if lesson_data.get("summary"):
                lesson["summary"] = lesson_data["summary"]
            if lesson_data.get("concepts"):
                lesson["concepts"] = lesson_data["concepts"]
            lesson["status"] = "content_done"
    draft.data = json.dumps(data)
    draft.phase = "validation"
    draft.stage = "generate_qa"
    draft.updated_at = datetime.utcnow()
    session.commit()
    return {"ok": True, "phase": draft.phase, "stage": draft.stage}


@router.put("/drafts/{draft_id}/cleanup")
def save_cleanup(
    draft_id: str,
    req: UpdateCleanupRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = _migrate_draft_data(json.loads(draft.data))
    for lesson_data in req.lessons:
        slug = lesson_data.get("slug", "")
        lesson = data.get("lessons", {}).get(slug)
        if lesson:
            if lesson_data.get("content"):
                lesson["content"] = lesson_data["content"]
            if lesson_data.get("summary"):
                lesson["summary"] = lesson_data["summary"]
            if lesson_data.get("concepts"):
                lesson["concepts"] = lesson_data["concepts"]
    draft.data = json.dumps(data)
    draft.stage = "quality_gate"
    draft.updated_at = datetime.utcnow()
    session.commit()
    return {"ok": True, "phase": draft.phase, "stage": draft.stage}


@router.get("/drafts/{draft_id}/wiki-coverage")
def wiki_coverage(
    draft_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Check outline concepts against the pedagogy wiki concept map."""
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = _migrate_draft_data(json.loads(draft.data))
    outline = data.get("outline", {})
    outline_with_lessons = {**outline, "_lessons_dict": data.get("lessons", {})}
    return check_outline_coverage(outline_with_lessons)


@router.post("/drafts/{draft_id}/assess-coverage")
async def stream_assess_coverage(
    draft_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Stream per-lesson KB coverage assessment via SSE."""
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = _migrate_draft_data(json.loads(draft.data))
    lessons_dict = data.get("lessons", {})
    draft_id_copy = draft.id

    # Only assess lessons that are in the current outline (ignore stale entries)
    outline = data.get("outline", {})
    outline_slugs = {
        les.get("slug", "")
        for mod in outline.get("modules", [])
        for les in mod.get("lessons", [])
    }
    lessons_list = [
        {"title": l.get("title", slug), "slug": slug,
         "summary": l.get("summary", ""), "concepts": l.get("concepts", [])}
        for slug, l in lessons_dict.items()
        if not outline_slugs or slug in outline_slugs
    ]

    async def _stream_and_save():
        assessment_data = {
            "fully_covered": [],
            "needs_research": [],
            "no_match": [],
        }
        async for event_str in assess_wiki_coverage_stream(lessons_list):
            yield event_str
            try:
                raw = event_str.strip()
                if raw.startswith("data: "):
                    evt = json.loads(raw[6:])
                    if evt.get("type") == "lesson_assessed":
                        verdict = evt.get("verdict", "")
                        entry = {
                            "slug": evt.get("slug", ""),
                            "title": evt.get("title", ""),
                            "topics": evt.get("topics", []),
                            "concept_verdicts": evt.get("concept_verdicts", {}),
                            "source_count": evt.get("source_count", 0),
                            "sources": evt.get("sources", []),
                            "research_topics": evt.get("research_topics", []),
                            "unmapped": evt.get("unmapped", []),
                        }
                        if verdict == "fully_covered":
                            assessment_data["fully_covered"].append(entry)
                        elif verdict == "needs_research":
                            assessment_data["needs_research"].append(entry)
                        elif verdict == "no_match":
                            assessment_data["no_match"].append(entry)
                    elif evt.get("type") == "done":
                        assessment_data["assessed_at"] = datetime.utcnow().isoformat()
                        from sqlmodel import Session as DBSession
                        with DBSession(engine) as save_session:
                            d = save_session.get(CourseDraft, draft_id_copy)
                            if d:
                                d_data = _migrate_draft_data(json.loads(d.data))
                                d_data["coverage_assessment"] = assessment_data
                                d.data = json.dumps(d_data)
                                d.stage = "coverage_assessed"
                                d.updated_at = datetime.utcnow()
                                save_session.commit()
            except Exception:
                pass

    return StreamingResponse(_stream_and_save(), media_type="text/event-stream")


class EnrichCoverageRequest(BaseModel):
    lesson_slugs: List[str] | None = None


@router.post("/drafts/{draft_id}/enrich-coverage")
async def stream_enrich_coverage(
    draft_id: str,
    req: EnrichCoverageRequest | None = None,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Stream KB enrichment pipeline via SSE."""
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = _migrate_draft_data(json.loads(draft.data))
    lessons_dict = data.get("lessons", {})
    outline = data.get("outline", {})
    course_desc = outline.get("description", outline.get("title", ""))
    course_profile = outline.get("course_profile")

    slug_filter = set(req.lesson_slugs) if req and req.lesson_slugs else None

    lessons_list = [
        {"title": l.get("title", slug), "slug": slug,
         "summary": l.get("summary", ""), "concepts": l.get("concepts", [])}
        for slug, l in lessons_dict.items()
        if slug_filter is None or slug in slug_filter
    ]

    draft_id_copy = draft.id

    async def _stream_and_save():
        collected_events: list[dict] = []
        async for event_str in ensure_wiki_coverage_stream(
            lessons_list, course_desc, course_profile=course_profile,
        ):
            yield event_str
            try:
                raw = event_str.strip()
                if raw.startswith("data: "):
                    evt = json.loads(raw[6:])
                    collected_events.append(evt)
            except (json.JSONDecodeError, KeyError):
                pass

        # Persist enrichment events to draft.data so they survive reload
        try:
            with Session(engine) as save_session:
                d = save_session.get(CourseDraft, draft_id_copy)
                if d:
                    d_data = _migrate_draft_data(json.loads(d.data))
                    existing = d_data.get("enrichment_log", [])
                    existing.extend(collected_events)
                    d_data["enrichment_log"] = existing
                    d.data = json.dumps(d_data)
                    d.updated_at = datetime.utcnow()
                    save_session.commit()
        except Exception as e:
            logger.warning("Failed to persist enrichment log: %s", e)

    return StreamingResponse(
        _stream_and_save(),
        media_type="text/event-stream",
    )


class PromoteSourceRequest(BaseModel):
    topic_slug: str
    url: str
    title: str = ""


@router.post("/drafts/{draft_id}/promote-source")
async def promote_source(
    draft_id: str,
    req: PromoteSourceRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Download a near-miss source and add it to the wiki topic."""
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")

    try:
        result = await download_source(
            req.url,
            req.topic_slug,
            title=req.title,
            extract_images=True,
        )
        return {
            "success": True,
            "topic_slug": req.topic_slug,
            "url": req.url,
            "saved_path": result.get("saved_path", ""),
            "word_count": result.get("word_count", 0),
        }
    except Exception as e:
        logger.error("Failed to promote source %s: %s", req.url, e)
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


@router.post("/drafts/{draft_id}/wiki-reference-kb")
async def stream_wiki_reference_kb(
    draft_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Generate reference KB from wiki downloads for each lesson."""
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = _migrate_draft_data(json.loads(draft.data))
    lessons_dict = data.get("lessons", {})
    outline = data.get("outline", {})
    draft_id_copy = draft.id

    lessons_list = [
        {"title": l.get("title", slug), "slug": slug,
         "summary": l.get("summary", ""), "concepts": l.get("concepts", [])}
        for slug, l in lessons_dict.items()
    ]

    existing_kb = data.get("reference_kb_drafts", {})
    kb_course_profile = outline.get("course_profile")

    async def _stream_and_save():
        async for event_str in generate_reference_kb_from_wiki(
            lessons_list, existing_kb=existing_kb,
            course_profile=kb_course_profile,
        ):
            yield event_str
            try:
                raw = event_str.strip()
                if raw.startswith("data: "):
                    evt = json.loads(raw[6:])
                    if evt.get("type") == "reference_kb" and evt.get("data"):
                        kb_data = evt["data"]
                        with Session(engine) as save_session:
                            d = save_session.get(CourseDraft, draft_id_copy)
                            if d:
                                d_data = _migrate_draft_data(json.loads(d.data))
                                for slug, kb_md in kb_data.items():
                                    lesson = d_data.get("lessons", {}).get(slug)
                                    if lesson and kb_md:
                                        lesson["reference_kb"] = kb_md
                                d.data = json.dumps(d_data)
                                d.updated_at = datetime.utcnow()
                                save_session.commit()
            except Exception:
                pass

    return StreamingResponse(_stream_and_save(), media_type="text/event-stream")


@router.get("/drafts/{draft_id}/wiki-enrichment-suggestions")
def wiki_enrichment_suggestions(
    draft_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Identify lessons that need more wiki content for better tutor grounding."""
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = _migrate_draft_data(json.loads(draft.data))
    lessons_dict = data.get("lessons", {})
    existing_kb = data.get("reference_kb_drafts", {})

    lessons_list = [
        {"title": l.get("title", slug), "slug": slug,
         "summary": l.get("summary", ""), "concepts": l.get("concepts", [])}
        for slug, l in lessons_dict.items()
    ]

    return suggest_wiki_enrichment(lessons_list, existing_kb)


@router.get("/drafts/{draft_id}/quality-gate")
def quality_gate(
    draft_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = _migrate_draft_data(json.loads(draft.data))
    outline_slugs = _get_outline_slugs(data)

    results = []
    all_pass = True
    for slug, lesson in data.get("lessons", {}).items():
        if outline_slugs and slug not in outline_slugs:
            continue
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
            "slug": slug,
            "passes": passes,
            **checks,
        })

    return {"lessons": results, "all_pass": all_pass, "total": len(results)}


# ---------------------------------------------------------------------------
# Reference KB
# ---------------------------------------------------------------------------

@router.put("/drafts/{draft_id}/reference-kb-drafts")
def save_reference_kb_drafts(
    draft_id: str,
    req: UpdateReferenceKbDraftsRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = _migrate_draft_data(json.loads(draft.data))
    for slug, kb_md in (req.reference_kb_drafts or {}).items():
        lesson = data.get("lessons", {}).get(slug)
        if lesson:
            lesson["reference_kb"] = kb_md
            if lesson.get("status") in ("outline", "researched"):
                lesson["status"] = "kb_done"
    draft.data = json.dumps(data)
    computed_phase = _compute_draft_phase(data)
    draft.phase = computed_phase
    draft.stage = "generate_qa" if computed_phase == "validation" else "generate_lessons"
    draft.updated_at = datetime.utcnow()
    session.commit()
    return {"ok": True, "phase": draft.phase, "stage": draft.stage}


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

@router.put("/drafts/{draft_id}/qa")
def save_qa(
    draft_id: str,
    req: UpdateQARequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = json.loads(draft.data)
    data["validation"] = data.get("validation", {})
    data["validation"]["qa_pairs"] = {
        "approved": req.approved,
        "rejected": req.rejected,
    }
    draft.data = json.dumps(data)
    draft.stage = "final_dashboard"
    draft.updated_at = datetime.utcnow()
    session.commit()
    return {"ok": True, "phase": draft.phase, "stage": draft.stage}


# ---------------------------------------------------------------------------
# SSE Streaming — Outline generation
# ---------------------------------------------------------------------------

@router.post("/drafts/{draft_id}/generate-outline")
async def stream_generate_outline(
    draft_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = json.loads(draft.data)
    source_text = data.get("source_text", "")
    draft_id_copy = draft.id

    async def _stream_and_save():
        gen = generate_outline(source_text, draft.source_type)
        async for event_str in gen:
            yield event_str
            try:
                raw = event_str.strip()
                if raw.startswith("data: "):
                    evt = json.loads(raw[6:])
                    if evt.get("type") == "outline":
                        outline = evt["data"]
                        with Session(engine) as save_session:
                            d = save_session.get(CourseDraft, draft_id_copy)
                            if d:
                                d_data = json.loads(d.data)
                                d_data["outline"] = outline
                                lessons_dict = d_data.setdefault("lessons", {})
                                for mod in outline.get("modules", []):
                                    for les in mod.get("lessons", []):
                                        slug = les.get("slug", "")
                                        if slug and slug not in lessons_dict:
                                            lessons_dict[slug] = {
                                                "title": les.get("title", ""),
                                                "slug": slug,
                                                "summary": les.get("summary", ""),
                                                "concepts": les.get("concepts", []),
                                                "source_hints": les.get("source_hints", []),
                                                "status": "outline",
                                            }
                                d.data = json.dumps(d_data)
                                d.phase = "content"
                                d.stage = "generate_content"
                                d.updated_at = datetime.utcnow()
                                save_session.commit()
            except Exception:
                pass

    return StreamingResponse(_stream_and_save(), media_type="text/event-stream")


# ---------------------------------------------------------------------------
# SSE Streaming endpoints — Content generation
# ---------------------------------------------------------------------------

class GenerateContentRequest(BaseModel):
    force_slugs: list[str] | None = None


@router.post("/drafts/{draft_id}/generate-content")
async def stream_generate_content(
    draft_id: str,
    resume: bool = False,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
    body: GenerateContentRequest | None = None,
):
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = _migrate_draft_data(json.loads(draft.data))
    outline = data.get("outline", {})
    source_text = data.get("source_text", "")
    draft_id_copy = draft.id
    force_slugs = set((body.force_slugs or []) if body else [])

    existing_lessons = None
    if resume or force_slugs:
        existing_lessons = [
            l for l in _get_all_lessons_list(data)
            if l.get("content") and l.get("slug") not in force_slugs
        ]
        logger.warning(
            "Content generation RESUME: %d existing, %d force-regenerate: %s",
            len(existing_lessons), len(force_slugs), list(force_slugs),
        )
    else:
        logger.warning("Content generation FRESH: resume=%s", resume)

    ref_kb: dict[str, str] = {}
    for slug, lesson in data.get("lessons", {}).items():
        kb = lesson.get("reference_kb", "")
        if kb:
            ref_kb[slug] = kb

    course_profile = outline.get("course_profile")

    async def _stream_and_save():
        outline_with_lessons = {**outline, "_lessons_dict": data.get("lessons", {})}
        gen = generate_content(
            outline_with_lessons, source_text, draft.source_type,
            existing_lessons=existing_lessons,
            reference_kb=ref_kb or None,
            wiki_context=None,
            course_profile=course_profile,
        )
        async for event_str in gen:
            yield event_str
            try:
                raw = event_str.strip()
                if raw.startswith("data: "):
                    evt = json.loads(raw[6:])
                    if evt.get("type") == "progress" and evt.get("status") == "done" and evt.get("lesson"):
                        if evt.get("skipped"):
                            continue
                        lesson_data = evt["lesson"]
                        slug = lesson_data.get("slug", "")
                        if slug:
                            from sqlmodel import Session as DBSession
                            with DBSession(engine) as save_session:
                                d = save_session.get(CourseDraft, draft_id_copy)
                                if d:
                                    d_data = _migrate_draft_data(json.loads(d.data))
                                    lesson = d_data.get("lessons", {}).get(slug)
                                    if lesson:
                                        lesson["content"] = lesson_data.get("content", "")
                                        if lesson_data.get("summary"):
                                            lesson["summary"] = lesson_data["summary"]
                                        if lesson_data.get("concepts"):
                                            lesson["concepts"] = lesson_data["concepts"]
                                        if lesson_data.get("sources_used"):
                                            lesson["sources_used"] = lesson_data["sources_used"]
                                        if lesson_data.get("reference_kb"):
                                            lesson["reference_kb"] = lesson_data["reference_kb"]
                                        if lesson_data.get("youtube_id"):
                                            lesson["youtube_id"] = lesson_data["youtube_id"]
                                        if lesson_data.get("video_title"):
                                            lesson["video_title"] = lesson_data["video_title"]
                                        lesson["status"] = "content_done"
                                    d.data = json.dumps(d_data)
                                    d.updated_at = datetime.utcnow()
                                    save_session.commit()
            except Exception:
                pass

    return StreamingResponse(_stream_and_save(), media_type="text/event-stream")


@router.post("/drafts/{draft_id}/run-cleanup")
async def stream_run_cleanup(
    draft_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = _migrate_draft_data(json.loads(draft.data))
    lessons = [
        {
            "slug": slug,
            "title": l.get("title", ""),
            "content": l.get("content", ""),
            "summary": l.get("summary", ""),
            "concepts": l.get("concepts", []),
        }
        for slug, l in data.get("lessons", {}).items()
        if l.get("content")
    ]
    domain_terms = data.get("domain_terms", "")
    return StreamingResponse(
        run_cleanup(lessons, domain_terms),
        media_type="text/event-stream",
    )


# ---------------------------------------------------------------------------
# SSE Streaming endpoints — Validation (QA generation, evaluation)
# ---------------------------------------------------------------------------

@router.post("/drafts/{draft_id}/generate-qa")
async def stream_generate_qa(
    draft_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = _migrate_draft_data(json.loads(draft.data))
    lessons = [
        {
            "slug": slug,
            "title": l.get("title", ""),
            "content": l.get("content", ""),
            "summary": l.get("summary", ""),
            "concepts": l.get("concepts", []),
        }
        for slug, l in data.get("lessons", {}).items()
        if l.get("content")
    ]
    kb_drafts = {
        slug: l.get("reference_kb", "")
        for slug, l in data.get("lessons", {}).items()
        if l.get("reference_kb")
    }
    return StreamingResponse(
        generate_qa(lessons, reference_kb_drafts=kb_drafts or None),
        media_type="text/event-stream",
    )


@router.post("/drafts/{draft_id}/evaluate-qa")
async def stream_evaluate_qa(
    draft_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = _migrate_draft_data(json.loads(draft.data))
    lessons = [
        {
            "slug": slug,
            "title": l.get("title", ""),
            "content": l.get("content", ""),
            "summary": l.get("summary", ""),
            "concepts": l.get("concepts", []),
        }
        for slug, l in data.get("lessons", {}).items()
        if l.get("content")
    ]
    qa_pairs = data.get("validation", {}).get("qa_pairs", {}).get("approved", [])
    return StreamingResponse(
        evaluate_qa(lessons, qa_pairs),
        media_type="text/event-stream",
    )


@router.post("/drafts/{draft_id}/publish")
def publish(
    draft_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = _migrate_draft_data(json.loads(draft.data))
    data["title"] = draft.title

    existing_path_id = data.get("published_path_id")
    result = publish_course(
        data, session, user_id=user.id, existing_path_id=existing_path_id,
    )

    data["published_path_id"] = result["learning_path_id"]
    data["published_slug"] = result["slug"]
    draft.data = json.dumps(data)
    draft.phase = "published"
    draft.stage = "done"
    draft.updated_at = datetime.utcnow()
    session.commit()
    return result


# ---------------------------------------------------------------------------
# Draft Chat — contextual conversation about the draft
# ---------------------------------------------------------------------------

DRAFT_CHAT_SYSTEM = """\
You are a course design co-pilot. The user is building a course with a \
wizard. They are currently in the "{phase}" phase (stage: "{stage}").

TITLE: {title}
SOURCE TYPE: {source_type}

{context}

## App workflow

The user builds courses through an automated pipeline. The phases are:
**Shaping → Researching → Building → Reviewing → Published**

Steps within the pipeline:
1. **Outline** (Shaping) — AI generates a structured outline (modules → lessons \
→ concepts) from the user's goal or uploaded transcript. The user can edit the \
outline via chat or directly in the Outline tab.
2. **Prepare Content** (Researching) — The system assesses each lesson's concepts \
against the wiki knowledge base. Results appear in the Research tab as a coverage \
report (covered / thin / missing concepts per lesson).
3. **Enrich** (Researching, optional) — An automated pipeline that searches the \
web for sources on thin/missing concepts, curates results, and downloads them \
into the wiki. Typically takes 2-5 minutes for a 6-lesson course. The user \
clicks one button ("Enrich N Concepts") and it runs automatically — no manual \
research needed.
4. **Build Course** (Building) — AI generates full lesson content grounded in \
wiki sources. Each lesson streams as it completes (~1-3 min per lesson). Users \
can selectively regenerate individual lessons without rebuilding everything.
5. **Quality Gate** (Reviewing) — Automated checks on each lesson: minimum word \
count, concept coverage, summary present. Shows pass/fail per lesson.
6. **Publish** (Published) — Pushes the draft to a live learning path accessible \
at /learn/{{slug}}. After publishing, the creator can share the course via email \
invites or a share link.

## Features & terminology

**Tabs the user sees (right panel):**
- **Outline** — modules and lessons with drag-to-reorder. "Build All" / \
"Build Select" buttons trigger content generation.
- **Research** — coverage results: which concepts are covered, thin, or missing \
in the wiki. "Enrich All" / "Enrich Select" buttons fill gaps automatically. \
"Build All" / "Build Select" buttons also available here.
- **Enrich** — live enrichment activity: per-lesson source picks, near misses, \
download stats. "Build All" / "Build Select" buttons available after enrichment.
- **Build** — build progress per lesson during content generation with \
collapsible source details.
- **Lessons** — two sub-views per lesson: **Notes** (the lesson content learners \
read) and **Reference KB** (curated wiki excerpts the Socratic tutor uses for \
grounding and citations — learners don't see this directly).
- **Publish** — course stats, readiness checks, per-lesson quality breakdown, \
and publish button.

**Key terms:**
- **Wiki / Knowledge Base (KB)** — a curated library of topic articles, papers, \
and educator resources organized by topic. All lesson content is grounded in \
the wiki so the tutor can cite sources. Enrichment expands the wiki.
- **Reference KB** — per-lesson excerpt from the wiki that the Socratic tutor \
uses to answer learner questions with citations. Different from lesson notes.
- **Notes** — the main lesson content the learner reads.
- **Concepts** — specific learning objectives per lesson (e.g., "scaled \
dot-product attention", "teacher forcing"). Coverage is assessed at concept \
level.
- **Coverage verdicts** — covered (strong wiki match), thin (partial match, \
could benefit from enrichment), missing (no wiki match, enrichment recommended).

**After publishing — the learner experience:**
- Learners see the course at /learn/{{slug}} with modules, lessons, and progress \
tracking.
- Each lesson has: markdown content (notes), optional video, reference sources, \
a **Socratic AI tutor** (conversational, cites wiki sources, uses pedagogy \
principles), and a quiz.
- The tutor is grounded in the reference KB — it doesn't hallucinate; it pulls \
from the curated wiki and cites its sources.

**Sharing & access:**
- Courses can be **public** (anyone can access) or **private** (invite only).
- Creators can share via email or a copyable link. Recipients join with one click.

**Other capabilities:**
- **Transcript upload** — paste or upload a lecture transcript as source material \
instead of typing a learning goal.
- **Export** — download the full draft as JSON for backup or migration.
- **Selective regeneration** — after building, regenerate only specific lessons \
(no need to rebuild the whole course).

Help the user by answering questions, suggesting improvements, and \
executing actions when they ask. Be concise and practical. When coverage \
data is available in the context, reference specific numbers and lessons. \
When the user asks about timing, sharing, publishing, or how learners will \
experience the course, refer to the information above.

## What you CAN and CANNOT do

**You CAN (via actions):**
- Edit lesson notes or reference KB text (edit_lesson_content)
- Modify the outline structure (modify_outline)
- Search the web for information (research_topic)
- Trigger a full lesson regeneration (regenerate_lesson, requires confirmation)

**You CANNOT (tell the user to use the UI instead):**
- Run the enrichment pipeline — this is a separate automated process \
triggered by the "Enrich All" or "Enrich Select" button on the Research \
or Enrich tab. You cannot enrich KB from chat.
- Generate course content — triggered by "Build All" / "Build Select" \
buttons on the Outline, Research, or Enrich tabs.
- Assess coverage — triggered by "Prepare Content" on the Outline tab.
- Publish the course — done from the Publish tab.

When a lesson is missing reference KB, do NOT suggest running enrichment \
from chat. Instead, tell the user to go to the Research or Enrich tab \
and run "Enrich Select" for that specific lesson, or use edit_lesson_content \
to manually add content to the reference_kb if they have specific text.

## Actions

When the user asks you to DO something (not just discuss), output a JSON \
block inside a ```json fence with a "draft_actions" array. Each action \
object has an "action" field. Available actions:

### 1. research_topic (auto-applied)
Search the web for information on a topic. Results shown in chat.
{{"action": "research_topic", "query": "..."}}

### 2. modify_outline (auto-applied)
Add, remove, reorder, or rename modules/lessons/course metadata. \
Describe the change in plain English — the system applies it for you.
{{"action": "modify_outline", "instruction": "Add a new module on efficiency techniques at the end"}}

### 3. edit_lesson_content (auto-applied)
Make a targeted edit to the notes or reference KB of a specific lesson \
without full regeneration. Use for small changes: fix formatting, remove \
duplicate links, add an example, simplify a section, etc.
{{"action": "edit_lesson_content", "slug": "lesson-slug", "target": "notes", "instruction": "Remove duplicate external links, keeping only the first occurrence of each URL"}}
{{"action": "edit_lesson_content", "slug": "lesson-slug", "target": "reference_kb", "instruction": "Add a section on practical implementation tips"}}

### 4. regenerate_lesson (requires user confirmation)
Completely re-generate a lesson from scratch using the wiki knowledge base. \
Only use this when the lesson needs a fundamental structural overhaul — NOT \
for small edits (use edit_lesson_content instead).
{{"action": "regenerate_lesson", "slug": "lesson-slug"}}

## Action selection guide
- Fixing formatting, removing links, adding/tweaking content → edit_lesson_content
- Adding/removing/reordering modules or lessons → modify_outline
- Completely rewriting a lesson from scratch → regenerate_lesson (user must confirm)
- Looking something up → research_topic

## Rules
- You can combine multiple actions in one response.
- Always use existing slugs from the context — do NOT invent slugs for edit_lesson_content.
- For edit_lesson_content, write a clear, specific instruction so the edit is precise.
- Actions that say "auto-applied" execute immediately without user confirmation.
- regenerate_lesson requires confirmation — the user will see a card to approve or skip.
- Only output actions when the user asks you to DO something, not for general discussion.

## Example

User: "Remove the duplicate links in the intro lesson notes, and add a module on evaluation"
```json
{{"draft_actions": [
  {{"action": "edit_lesson_content", "slug": "intro-to-attention", "target": "notes",
    "instruction": "Remove duplicate external links, keeping only the first occurrence of each URL"}},
  {{"action": "modify_outline",
    "instruction": "Add a new module called 'Evaluation & Benchmarks' at the end with one lesson on BLEU score and evaluation metrics"}}
]}}
```
"""


def _build_chat_context(data: dict) -> list[str]:
    """Assemble context sections for the chat system prompt."""
    parts = []

    if data.get("outline"):
        parts.append(f"OUTLINE:\n{json.dumps(data['outline'], indent=1)}")

    lessons_dict = data.get("lessons", {})
    if lessons_dict:
        details = []
        for idx, (slug, l) in enumerate(lessons_dict.items(), 1):
            entry = f"### Lesson {idx}: {l.get('title', 'Untitled')} [{l.get('status', 'outline')}]\n"
            entry += f"Slug: {slug}\n"
            entry += f"Concepts: {', '.join(l.get('concepts', []))}\n"
            content = l.get("content", "")
            if content:
                entry += f"Content ({len(content)} chars):\n{content}\n"
            elif l.get("reference_kb"):
                entry += f"Reference KB ({len(l['reference_kb'])} chars) generated\n"
            else:
                entry += "(No content generated yet)\n"
            details.append(entry)
        parts.append(f"LESSONS ({len(lessons_dict)} total):\n\n" + "\n---\n".join(details))

    cov = data.get("coverage_assessment")
    if cov:
        covered = thin = missing = 0
        total_sources = 0
        all_topics: set[str] = set()
        per_lesson: list[str] = []

        for bucket in ("fully_covered", "needs_research", "no_match"):
            for entry in cov.get(bucket, []):
                lesson = entry.get("lesson", {})
                slug = lesson.get("slug", entry.get("slug", "?"))
                topics = entry.get("topics", [])
                for t in topics:
                    all_topics.add(t)
                total_sources += entry.get("source_count", 0)

                verdicts = entry.get("concept_verdicts", {})
                thin_concepts = []
                missing_concepts = []
                for concept, v in verdicts.items():
                    vstr = v if isinstance(v, str) else (v or {}).get("verdict", "missing")
                    if vstr == "covered":
                        covered += 1
                    elif vstr == "thin":
                        thin += 1
                        thin_concepts.append(concept)
                    else:
                        missing += 1
                        missing_concepts.append(concept)

                unmapped = entry.get("unmapped", [])
                missing += len(unmapped)
                missing_concepts.extend(unmapped)

                if bucket == "fully_covered":
                    per_lesson.append(f"- {slug}: fully_covered ({len(topics)} topics, {entry.get('source_count', 0)} sources)")
                elif bucket == "no_match":
                    per_lesson.append(f"- {slug}: no_match — unmapped: {missing_concepts}")
                else:
                    gaps = []
                    if thin_concepts:
                        gaps.append(f"thin: {thin_concepts}")
                    if missing_concepts:
                        gaps.append(f"missing: {missing_concepts}")
                    per_lesson.append(f"- {slug}: needs_research — {', '.join(gaps)}")

        total = covered + thin + missing
        lines = [
            f"COVERAGE ASSESSMENT (assessed {cov.get('assessed_at', 'unknown')}):",
            f"Concept-level: {covered} covered, {thin} thin, {missing} missing ({total} total across {len(per_lesson)} lessons)",
            f"Wiki topics matched: {', '.join(sorted(all_topics)) or 'none'}",
            f"Sources checked: {total_sources}",
            "",
            "Per-lesson verdicts:",
        ] + per_lesson
        parts.append("\n".join(lines))

    # Quality / readiness stats
    outline_slugs = _get_outline_slugs(data)
    active_lessons = {
        slug: l for slug, l in lessons_dict.items()
        if not outline_slugs or slug in outline_slugs
    }
    if active_lessons:
        total = len(active_lessons)
        with_content = []
        without_content = []
        with_concepts = []
        without_concepts = []
        with_summary = []
        without_summary = []
        with_kb = []
        without_kb = []
        word_counts = []

        for slug, l in active_lessons.items():
            title = l.get("title", slug)
            content = l.get("content", "")
            wc = len(content.split()) if content else 0
            word_counts.append(wc)

            if wc >= 100:
                with_content.append(title)
            else:
                without_content.append(title)
            if l.get("concepts"):
                with_concepts.append(title)
            else:
                without_concepts.append(title)
            if l.get("summary", "").strip():
                with_summary.append(title)
            else:
                without_summary.append(title)
            if l.get("reference_kb"):
                with_kb.append(title)
            else:
                without_kb.append(title)

        lines = [
            f"COURSE READINESS ({total} lessons in current outline):",
            f"Content: {len(with_content)}/{total} lessons have content (total {sum(word_counts):,} words, avg {round(sum(word_counts)/max(total,1))}/lesson)",
            f"Concepts: {len(with_concepts)}/{total}",
            f"Summaries: {len(with_summary)}/{total}",
            f"Reference KB: {len(with_kb)}/{total}",
        ]
        if without_content:
            lines.append(f"Lessons WITHOUT sufficient content: {', '.join(without_content)}")
        if without_concepts:
            lines.append(f"Lessons WITHOUT concepts: {', '.join(without_concepts)}")
        if without_summary:
            lines.append(f"Lessons WITHOUT summaries: {', '.join(without_summary)}")
        if without_kb:
            lines.append(f"Lessons WITHOUT reference KB: {', '.join(without_kb)}")
        if word_counts:
            lines.append(f"Word count range: {min(word_counts)}–{max(word_counts)}")
        parts.append("\n".join(lines))

    if data.get("source_text"):
        parts.append(f"SOURCE TEXT (first 2000 chars):\n{data['source_text'][:2000]}")

    return parts


@router.post("/drafts/{draft_id}/chat")
async def draft_chat(
    draft_id: str,
    req: DraftChatRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")

    data = _migrate_draft_data(json.loads(draft.data))
    draft_id_copy = draft.id

    context_parts = _build_chat_context(data)
    system_prompt = DRAFT_CHAT_SYSTEM.format(
        phase=draft.phase,
        stage=draft.stage,
        title=draft.title,
        source_type=draft.source_type,
        context="\n\n".join(context_parts) if context_parts else "(No content generated yet)",
    )

    messages = [{"role": "system", "content": system_prompt}]
    for msg in req.history:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": req.message})

    from ..config import get_settings
    from ..services.chat_actions import (
        parse_draft_actions,
        classify_action,
        execute_action,
    )
    import httpx

    settings = get_settings()

    async def _stream():
        headers = {
            "Authorization": f"Bearer {settings.llm_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": settings.llm_model,
            "messages": messages,
            "max_tokens": 4096,
            "temperature": 0.4,
            "stream": True,
        }

        full_response = []

        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream(
                "POST",
                f"{settings.llm_base_url}/chat/completions",
                headers=headers,
                json=payload,
            ) as resp:
                async for line in resp.aiter_lines():
                    if line.startswith("data: "):
                        chunk = line[6:]
                        if chunk.strip() == "[DONE]":
                            break
                        try:
                            parsed = json.loads(chunk)
                            delta = parsed["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                full_response.append(content)
                                yield f"data: {json.dumps({'type': 'token', 'content': content})}\n\n"
                        except (json.JSONDecodeError, KeyError, IndexError):
                            pass

        response_text = "".join(full_response)
        actions = parse_draft_actions(response_text)

        if actions:
            auto_acts = [a for a in actions if classify_action(a.get("action", "")) == "auto"]
            pending = [a for a in actions if classify_action(a.get("action", "")) != "auto"]
            auto_applied = []

            if auto_acts:
                with Session(engine) as action_session:
                    draft_row = action_session.get(CourseDraft, draft_id_copy)
                    if draft_row:
                        action_data = _migrate_draft_data(json.loads(draft_row.data))

                        # Run auto-applied actions in parallel
                        async def _run(act: dict) -> dict:
                            try:
                                return await execute_action(act, action_data)
                            except Exception as e:
                                logger.warning("Chat action failed: %s", e)
                                return {
                                    "action": act.get("action", ""),
                                    "status": "error",
                                    "summary": str(e),
                                }

                        import asyncio as _asyncio
                        auto_applied = list(await _asyncio.gather(*[_run(a) for a in auto_acts]))

                        if any(r.get("status") == "success" for r in auto_applied):
                            draft_row.data = json.dumps(action_data)
                            draft_row.updated_at = datetime.utcnow()
                            action_session.commit()

            yield f"data: {json.dumps({'type': 'draft_actions', 'auto_applied': auto_applied, 'pending': pending})}\n\n"

        # Persist chat history into draft.data so it survives refresh/logout
        try:
            updated_history = [{"role": m.role, "content": m.content} for m in req.history]
            updated_history.append({"role": "user", "content": req.message})
            updated_history.append({"role": "assistant", "content": response_text})
            with Session(engine) as save_session:
                d = save_session.get(CourseDraft, draft_id_copy)
                if d:
                    d_data = _migrate_draft_data(json.loads(d.data))
                    d_data["chat_history"] = updated_history
                    d.data = json.dumps(d_data)
                    d.updated_at = datetime.utcnow()
                    save_session.commit()
        except Exception as e:
            logger.warning("Failed to persist chat history: %s", e)

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(_stream(), media_type="text/event-stream")


@router.post("/drafts/{draft_id}/apply-chat-action")
async def apply_chat_action(
    draft_id: str,
    body: dict,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    """Execute a confirm-required chat action that the user approved."""
    from ..services.chat_actions import execute_action

    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")

    data = _migrate_draft_data(json.loads(draft.data))
    result = await execute_action(body, data)

    if result.get("status") == "success":
        draft.data = json.dumps(data)
        draft.updated_at = datetime.utcnow()
        session.commit()

    return result


# ---------------------------------------------------------------------------
# Transcript upload
# ---------------------------------------------------------------------------

@router.post("/drafts/{draft_id}/upload-transcript")
async def upload_transcript(
    draft_id: str,
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")

    content = await file.read()
    text = content.decode("utf-8", errors="replace")

    data = json.loads(draft.data)
    data["source_text"] = text
    data["upload_filename"] = file.filename
    draft.data = json.dumps(data)
    draft.source_type = "transcript"
    draft.updated_at = datetime.utcnow()
    session.commit()

    return {
        "ok": True,
        "filename": file.filename,
        "char_count": len(text),
        "source_type": "transcript",
    }


@router.get("/drafts/{draft_id}/final-dashboard")
def final_dashboard(
    draft_id: str,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    draft = session.get(CourseDraft, draft_id)
    if not draft or draft.user_id != user.id:
        raise HTTPException(status_code=404, detail="Draft not found")
    data = _migrate_draft_data(json.loads(draft.data))
    lessons_dict = data.get("lessons", {})
    outline_slugs = _get_outline_slugs(data)
    active_lessons = {
        slug: l for slug, l in lessons_dict.items()
        if not outline_slugs or slug in outline_slugs
    }

    content_word_counts = [len(l.get("content", "").split()) for l in active_lessons.values() if l.get("content")]
    kb_texts = [l.get("reference_kb", "") for l in active_lessons.values() if l.get("reference_kb")]

    qa = data.get("validation", {}).get("qa_pairs", {})
    approved = qa.get("approved", [])
    rejected = qa.get("rejected", [])

    qa_scores = [p.get("quality_score", 0) for p in approved if p.get("quality_score")]
    reasoning_types = list({p.get("reasoning_type", "") for p in approved if p.get("reasoning_type")})

    if kb_texts:
        kb_word_counts = [len(md.split()) for md in kb_texts]
        kb_section_counts = [md.count("\n## ") for md in kb_texts]
        knowledge_stats = {
            "format": "markdown",
            "lesson_count": len(kb_texts),
            "total_words": sum(kb_word_counts),
            "avg_word_count": round(sum(kb_word_counts) / max(len(kb_word_counts), 1)),
            "total_sections": sum(kb_section_counts),
        }
    else:
        knowledge_stats = {"format": "none", "count": 0}

    return {
        "content": {
            "lesson_count": len(content_word_counts),
            "avg_word_count": round(sum(content_word_counts) / max(len(content_word_counts), 1)),
            "min_word_count": min(content_word_counts) if content_word_counts else 0,
            "max_word_count": max(content_word_counts) if content_word_counts else 0,
        },
        "knowledge": knowledge_stats,
        "qa": {
            "approved_count": len(approved),
            "rejected_count": len(rejected),
            "reasoning_types": reasoning_types,
            "avg_score": round(sum(qa_scores) / max(len(qa_scores), 1), 1) if qa_scores else 0,
            "synthesis_count": sum(1 for p in approved if p.get("tier") == "synthesis"),
        },
    }


