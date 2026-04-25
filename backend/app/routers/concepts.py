import json
import logging
import re
from fastapi import APIRouter, Depends, HTTPException
from openai import AsyncOpenAI
from sqlmodel import Session, select, text

from ..db import get_session
from ..deps import get_current_user
from ..models.user import User
from ..models.learning import Lesson, Module, LearningPath
from ..models.concept import ConceptPage
from ..schemas.concepts import (
    ConceptSearchRequest,
    ConceptPageResponse,
    ConceptSuggestion,
    MisconceptionItem,
    KeyEquation,
    Paper,
    VideoSuggestion,
)
from ..agent.system_prompt_concepts import build_concept_prompt
from ..config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/concepts", tags=["concepts"])

_async_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _async_client
    if _async_client is None:
        settings = get_settings()
        _async_client = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
        )
    return _async_client


def _ensure_extra_data_column(session: Session) -> None:
    """Add extra_data column to conceptpage if it doesn't exist (SQLite safe)."""
    try:
        session.exec(text("SELECT extra_data FROM conceptpage LIMIT 1"))
    except Exception:
        try:
            session.exec(text("ALTER TABLE conceptpage ADD COLUMN extra_data TEXT DEFAULT '{}'"))
            session.commit()
            logger.info("Added extra_data column to conceptpage table")
        except Exception as e:
            logger.warning("Could not add extra_data column: %s", e)


def _extract_json(raw: str) -> dict:
    """Robustly extract a JSON object from LLM output.

    Tries multiple strategies in order:
    1. Direct parse
    2. Strip markdown code fences (```json ... ```)
    3. Regex extract first {...} block
    4. Truncate at last valid closing brace
    """
    text_to_parse = raw.strip()

    # Strategy 1: direct parse
    try:
        return json.loads(text_to_parse)
    except json.JSONDecodeError:
        pass

    # Strategy 2: strip any code fence flavour
    stripped = re.sub(r"^```[a-zA-Z]*\n?", "", text_to_parse)
    stripped = re.sub(r"\n?```$", "", stripped.rstrip()).strip()
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass

    # Strategy 3: regex — find the first { ... } block
    match = re.search(r"\{[\s\S]*\}", stripped)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            # Strategy 4: truncate at last complete closing brace
            candidate = match.group(0)
            for end in range(len(candidate), 0, -1):
                try:
                    return json.loads(candidate[:end])
                except json.JSONDecodeError:
                    continue

    raise ValueError(f"Could not extract valid JSON from response: {raw[:300]}")


def _concept_to_response(c: ConceptPage) -> ConceptPageResponse:
    def _parse_json(raw: str | None, default):
        if not raw:
            return default
        try:
            return json.loads(raw)
        except Exception:
            return default

    misconceptions_raw = _parse_json(c.misconceptions, [])
    misconceptions = [
        MisconceptionItem(text=m.get("text", ""), is_correct=m.get("is_correct", False))
        for m in misconceptions_raw
        if isinstance(m, dict)
    ]

    extra = _parse_json(c.extra_data, {})

    key_equations = [
        KeyEquation(
            label=e.get("label", ""),
            latex=e.get("latex", ""),
            description=e.get("description", ""),
        )
        for e in extra.get("key_equations", [])
        if isinstance(e, dict)
    ]

    papers = [
        Paper(
            title=p.get("title", ""),
            authors=p.get("authors", ""),
            year=p.get("year", ""),
            description=p.get("description", ""),
        )
        for p in extra.get("papers", [])
        if isinstance(p, dict)
    ]

    videos = [
        VideoSuggestion(
            title=v.get("title", ""),
            channel=v.get("channel", ""),
            search_query=v.get("search_query", ""),
        )
        for v in extra.get("videos", [])
        if isinstance(v, dict)
    ]

    prerequisites = [p for p in extra.get("prerequisites", []) if isinstance(p, str)]

    return ConceptPageResponse(
        id=c.id,
        topic=c.topic,
        level=c.level,
        simple_definition=c.simple_definition,
        why_it_matters=c.why_it_matters,
        detailed_explanation=c.detailed_explanation,
        analogy=c.analogy,
        real_world_example=c.real_world_example,
        misconceptions=misconceptions,
        key_takeaways=_parse_json(c.key_takeaways, []),
        related_concepts=_parse_json(c.related_concepts, []),
        further_reading=_parse_json(c.further_reading, []),
        prerequisites=prerequisites,
        key_equations=key_equations,
        papers=papers,
        videos=videos,
        lesson_id=c.lesson_id,
        created_at=c.created_at,
    )


def _find_matching_lesson(topic: str, session: Session) -> Lesson | None:
    topic_lower = topic.lower().strip()
    lessons = session.exec(select(Lesson)).all()
    for lesson in lessons:
        if topic_lower in lesson.title.lower() or lesson.title.lower() in topic_lower:
            return lesson
        try:
            concepts = json.loads(lesson.concepts) if lesson.concepts else []
        except (json.JSONDecodeError, TypeError):
            concepts = []
        for concept in concepts:
            if isinstance(concept, str) and (
                topic_lower in concept.lower() or concept.lower() in topic_lower
            ):
                return lesson
    return None


FEATURED_CONCEPTS = [
    "Backpropagation", "Gradient descent", "Activation functions", "Dropout",
    "Batch normalization", "Convolution", "Residual connections", "LSTM",
    "Vanishing gradients", "Attention mechanism", "Word2Vec",
    "Self-attention", "Multi-head attention", "Transformer block",
    "Positional encoding", "RoPE", "Tokenization", "Byte pair encoding",
    "Scaling laws", "Mixture of experts", "Flash Attention", "KV cache",
    "Pre-training", "RLHF", "DPO", "Chain-of-thought", "Few-shot prompting",
    "Retrieval-augmented generation", "Vector database", "Embeddings",
    "LoRA", "QLoRA", "Quantization", "Hallucination",
    "CLIP", "Contrastive learning", "Vision Transformer", "LLaVA",
    "Diffusion models", "Stable Diffusion", "Cross-attention", "ControlNet",
    "Whisper", "Text-to-video", "Sora", "Multi-modal RAG",
    "ReAct", "Function calling", "Agent loop", "Multi-agent systems",
    "LangGraph", "Prompt injection", "Guardrails", "Model Context Protocol",
    "Reinforcement learning", "Sim-to-real transfer", "Domain randomization",
    "Digital twin", "VLA models", "Autonomous driving",
]

_FEATURED_KEYS = {c.lower() for c in FEATURED_CONCEPTS}


@router.get("/suggestions", response_model=list[ConceptSuggestion])
async def get_suggestions(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    _ensure_extra_data_column(session)
    lessons = session.exec(select(Lesson).order_by(Lesson.order_index)).all()

    seen: set[str] = set()
    by_key: dict[str, ConceptSuggestion] = {}
    for lesson in lessons:
        try:
            concepts = json.loads(lesson.concepts) if lesson.concepts else []
        except (json.JSONDecodeError, TypeError):
            concepts = []
        for concept in concepts:
            if isinstance(concept, str):
                key = concept.lower().strip()
                if key and key not in seen:
                    seen.add(key)
                    by_key[key] = ConceptSuggestion(label=concept, lesson_id=lesson.id)

    featured: list[ConceptSuggestion] = []
    for fc in FEATURED_CONCEPTS:
        key = fc.lower()
        if key in by_key:
            featured.append(by_key[key])
        else:
            featured.append(ConceptSuggestion(label=fc, lesson_id=None))

    rest = [s for k, s in by_key.items() if k not in _FEATURED_KEYS]
    return featured + rest


@router.post("/search", response_model=ConceptPageResponse)
async def search_concept(
    req: ConceptSearchRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    _ensure_extra_data_column(session)
    topic = req.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Topic cannot be empty")

    cached = session.exec(
        select(ConceptPage).where(ConceptPage.topic.ilike(topic))
    ).first()
    if cached:
        # Re-generate if the cached record has no enrichment data
        extra = json.loads(cached.extra_data or "{}") if cached.extra_data else {}
        if extra.get("papers") or extra.get("key_equations"):
            return _concept_to_response(cached)
        # Otherwise fall through to regenerate with new prompt

    matching_lesson = _find_matching_lesson(topic, session)
    lesson_title = lesson_content = lesson_summary = reference_kb = None
    concepts = None
    lesson_id = None

    if matching_lesson:
        lesson_title = matching_lesson.title
        lesson_content = matching_lesson.content
        lesson_summary = matching_lesson.summary
        reference_kb = matching_lesson.reference_kb
        lesson_id = matching_lesson.id
        try:
            concepts = json.loads(matching_lesson.concepts) if matching_lesson.concepts else []
        except (json.JSONDecodeError, TypeError):
            concepts = []

    prompt = build_concept_prompt(
        topic=topic,
        lesson_title=lesson_title,
        lesson_content=lesson_content,
        lesson_summary=lesson_summary,
        reference_kb=reference_kb,
        concepts=concepts,
    )

    client = _get_client()
    settings = get_settings()

    try:
        response = await client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Generate the concept page JSON for: {topic}"},
            ],
            max_tokens=8192,
            temperature=0.4,
        )
    except Exception as e:
        logger.error("LLM concept generation failed: %s", e)
        raise HTTPException(status_code=502, detail="Concept generation failed. Please try again.")

    raw = (response.choices[0].message.content or "").strip()

    try:
        data = _extract_json(raw)
    except ValueError:
        logger.error("Failed to parse concept JSON. Raw: %s", raw[:800])
        raise HTTPException(
            status_code=502,
            detail="Concept generation returned an invalid format. Please try again.",
        )

    extra_data = json.dumps({
        "prerequisites": data.get("prerequisites", []),
        "key_equations": data.get("key_equations", []),
        "papers": data.get("papers", []),
        "videos": data.get("videos", []),
    })

    if cached:
        # Update existing stale record
        cached.simple_definition = data.get("simple_definition", cached.simple_definition)
        cached.why_it_matters = data.get("why_it_matters", cached.why_it_matters)
        cached.detailed_explanation = data.get("detailed_explanation", cached.detailed_explanation)
        cached.analogy = data.get("analogy", cached.analogy)
        cached.real_world_example = data.get("real_world_example", cached.real_world_example)
        cached.misconceptions = json.dumps(data.get("misconceptions", []))
        cached.key_takeaways = json.dumps(data.get("key_takeaways", []))
        cached.related_concepts = json.dumps(data.get("related_concepts", []))
        cached.further_reading = json.dumps(data.get("further_reading", []))
        cached.extra_data = extra_data
        session.add(cached)
        session.commit()
        session.refresh(cached)
        return _concept_to_response(cached)

    concept_page = ConceptPage(
        topic=data.get("topic", topic),
        level=data.get("level", "intermediate"),
        simple_definition=data.get("simple_definition", ""),
        why_it_matters=data.get("why_it_matters", ""),
        detailed_explanation=data.get("detailed_explanation", ""),
        analogy=data.get("analogy", ""),
        real_world_example=data.get("real_world_example", ""),
        misconceptions=json.dumps(data.get("misconceptions", [])),
        key_takeaways=json.dumps(data.get("key_takeaways", [])),
        related_concepts=json.dumps(data.get("related_concepts", [])),
        further_reading=json.dumps(data.get("further_reading", [])),
        extra_data=extra_data,
        lesson_id=lesson_id,
    )
    session.add(concept_page)
    session.commit()
    session.refresh(concept_page)

    return _concept_to_response(concept_page)
