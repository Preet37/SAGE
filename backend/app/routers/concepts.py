import json
import logging
from fastapi import APIRouter, Depends, HTTPException
from openai import AsyncOpenAI
from sqlmodel import Session, select

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


def _concept_to_response(c: ConceptPage) -> ConceptPageResponse:
    def _parse_json(raw: str, default):
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
        lesson_id=c.lesson_id,
        created_at=c.created_at,
    )


def _find_matching_lesson(topic: str, session: Session) -> Lesson | None:
    """Try to match the topic to a lesson by title or concepts."""
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


# ── GET /concepts/suggestions ─────────────────────────────────────────────────

@router.get("/suggestions", response_model=list[ConceptSuggestion])
async def get_suggestions(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    lessons = session.exec(
        select(Lesson).order_by(Lesson.order_index)
    ).all()

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


# ── POST /concepts/search ─────────────────────────────────────────────────────

@router.post("/search", response_model=ConceptPageResponse)
async def search_concept(
    req: ConceptSearchRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    topic = req.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Topic cannot be empty")

    # Check cache (case-insensitive)
    cached = session.exec(
        select(ConceptPage).where(ConceptPage.topic.ilike(topic))
    ).first()
    if cached:
        return _concept_to_response(cached)

    # Try to match to a curriculum lesson for grounding
    matching_lesson = _find_matching_lesson(topic, session)

    lesson_title = None
    lesson_content = None
    lesson_summary = None
    reference_kb = None
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
                {"role": "user", "content": f"Generate a concept page for: {topic}"},
            ],
            max_tokens=4096,
            temperature=0.7,
        )
    except Exception as e:
        logger.error("LLM concept generation failed: %s", e)
        raise HTTPException(status_code=502, detail="Concept generation failed. Please try again.")

    raw = (response.choices[0].message.content or "").strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        logger.error("Failed to parse concept JSON: %s", raw[:500])
        raise HTTPException(status_code=502, detail="Concept generation returned invalid format. Please try again.")

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
        lesson_id=lesson_id,
    )
    session.add(concept_page)
    session.commit()
    session.refresh(concept_page)

    return _concept_to_response(concept_page)
