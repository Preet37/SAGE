"""Pre-generate concept pages for featured concepts.

Iterates through the curated FEATURED_CONCEPTS list, skips any already
cached in the database, and generates the rest via the LLM. This ensures
instant responses when users first search these concepts.

Run with:  python -m scripts.preload_concepts [--dry-run]
"""

import asyncio
import json
import logging
import sys
import time

from openai import AsyncOpenAI
from sqlmodel import Session, select

from app.db import engine, create_db_and_tables
from app.config import get_settings
from app.models.learning import Lesson
from app.models.concept import ConceptPage
from app.routers.concepts import FEATURED_CONCEPTS
from app.agent.system_prompt_concepts import build_concept_prompt

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

CONCURRENCY = 3


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


async def generate_concept(client: AsyncOpenAI, model: str, topic: str, session: Session) -> bool:
    """Generate and cache a single concept page. Returns True if generated."""
    cached = session.exec(
        select(ConceptPage).where(ConceptPage.topic.ilike(topic))
    ).first()
    if cached:
        return False

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

    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Generate a concept page for: {topic}"},
        ],
        max_tokens=4096,
        temperature=0.7,
    )

    raw = (response.choices[0].message.content or "").strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines)

    data = json.loads(raw)

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
    return True


async def main(dry_run: bool = False):
    create_db_and_tables()
    settings = get_settings()
    client = AsyncOpenAI(api_key=settings.llm_api_key, base_url=settings.llm_base_url)

    with Session(engine) as session:
        to_generate = []
        already_cached = 0
        for topic in FEATURED_CONCEPTS:
            cached = session.exec(
                select(ConceptPage).where(ConceptPage.topic.ilike(topic))
            ).first()
            if cached:
                already_cached += 1
            else:
                to_generate.append(topic)

        logger.info(
            "%d featured concepts: %d cached, %d to generate",
            len(FEATURED_CONCEPTS), already_cached, len(to_generate),
        )

        if dry_run:
            for t in to_generate:
                print(f"  Would generate: {t}")
            return

        if not to_generate:
            logger.info("All concepts already cached!")
            return

        sem = asyncio.Semaphore(CONCURRENCY)
        generated = 0
        failed = 0
        start = time.time()

        async def _do(topic: str):
            nonlocal generated, failed
            async with sem:
                try:
                    created = await generate_concept(client, settings.llm_model, topic, session)
                    if created:
                        generated += 1
                        logger.info("  [%d/%d] Generated: %s", generated + failed, len(to_generate), topic)
                    else:
                        logger.info("  [%d/%d] Already cached: %s", generated + failed, len(to_generate), topic)
                except Exception as e:
                    failed += 1
                    logger.error("  [%d/%d] Failed: %s — %s", generated + failed, len(to_generate), topic, e)

        await asyncio.gather(*[_do(t) for t in to_generate])

        elapsed = time.time() - start
        logger.info(
            "Done in %.1fs — %d generated, %d failed, %d were already cached",
            elapsed, generated, failed, already_cached,
        )


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    asyncio.run(main(dry_run=dry_run))
