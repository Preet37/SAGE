"""
Notes router — human-AI collaboration through note revision.
Students write notes; AI reviews, enriches, identifies gaps, and
suggests connections to the concept graph.
"""
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.models.user import User
from app.models.lesson import Lesson
from app.models.concept import ConceptNode
from app.routers.auth import get_current_user
from app.config import get_settings, load_yaml_config

router = APIRouter(prefix="/notes", tags=["notes"])
settings = get_settings()
yaml_cfg = load_yaml_config()


class NoteSubmit(BaseModel):
    lesson_id: int
    content: str  # raw student notes (markdown OK)
    note_type: str = "lesson"  # lesson | concept | question | summary


class NoteRevisionOut(BaseModel):
    original: str
    revised: str
    gaps_identified: list[str]
    concept_connections: list[dict]
    misconceptions: list[str]
    strength_score: float
    suggestions: list[str]


@router.post("/revise", response_model=NoteRevisionOut)
async def revise_notes(
    req: NoteSubmit,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    AI reviews student notes and returns:
    - Corrected/enriched version
    - Knowledge gaps
    - Misconceptions detected
    - Concept graph connections
    - Suggestions for improvement
    """
    lesson_result = await db.execute(select(Lesson).where(Lesson.id == req.lesson_id))
    lesson = lesson_result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(404, "Lesson not found")

    nodes_result = await db.execute(
        select(ConceptNode).where(ConceptNode.course_id == lesson.course_id)
    )
    concept_labels = [n.label for n in nodes_result.scalars().all()]

    prompt = f"""You are SAGE's Note Revision Agent reviewing student notes on "{lesson.title}".
Key concepts: {", ".join(lesson.key_concepts)}
Student notes: {req.content[:800]}

Return ONLY this JSON object, nothing else before or after:
{{"revised":"improved markdown version of notes","gaps_identified":["missing concept 1"],"concept_connections":[{{"from":"their term","to":"graph term","relationship":"how they relate"}}],"misconceptions":["wrong statement if any"],"strength_score":0.6,"suggestions":["actionable tip 1","actionable tip 2"]}}"""

    from app.agents.base import asi1_complete
    result_str = await asi1_complete(prompt, max_tokens=1024)

    # Strip markdown code fences and extract JSON
    result_str = result_str.strip()
    import re
    # Try to find JSON object in the response
    json_match = re.search(r'\{[\s\S]*\}', result_str)
    if json_match:
        result_str = json_match.group(0)

    try:
        data = json.loads(result_str)
    except json.JSONDecodeError:
        data = {
            "revised": req.content + "\n\n*[AI revision unavailable — raw notes preserved]*",
            "gaps_identified": [],
            "concept_connections": [],
            "misconceptions": [],
            "strength_score": 0.5,
            "suggestions": ["Try adding more specific examples.", "Connect concepts to the key terms."],
        }

    return NoteRevisionOut(
        original=req.content,
        revised=data.get("revised", req.content),
        gaps_identified=data.get("gaps_identified", []),
        concept_connections=data.get("concept_connections", []),
        misconceptions=data.get("misconceptions", []),
        strength_score=float(data.get("strength_score", 0.5)),
        suggestions=data.get("suggestions", []),
    )


@router.post("/generate-plan")
async def generate_lesson_plan(
    lesson_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Generate a downloadable lesson plan / study guide for offline use.
    Returns structured markdown the frontend can download or cache.
    """
    lesson_result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = lesson_result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(404, "Lesson not found")

    nodes_result = await db.execute(
        select(ConceptNode).where(ConceptNode.course_id == lesson.course_id)
    )
    concepts = nodes_result.scalars().all()

    prompt = f"""Create a comprehensive study guide / lesson plan for: "{lesson.title}"

Key concepts to cover: {", ".join(lesson.key_concepts)}
Related concept graph nodes: {", ".join(c.label for c in concepts[:10])}

Generate a structured markdown study guide with:
1. Learning objectives (3-5 bullet points)
2. Core concepts explained (with examples)
3. Key formulas/code snippets
4. Practice problems (3 varied difficulty)
5. Connection map (how concepts relate to each other)
6. Further reading suggestions
7. Self-assessment checklist

Make it thorough and self-contained — usable offline."""

    from app.agents.base import asi1_complete
    plan_content = await asi1_complete(prompt, max_tokens=2000)

    return {
        "lesson_id": lesson_id,
        "lesson_title": lesson.title,
        "plan_markdown": plan_content,
        "download_filename": f"sage-{lesson.slug}-study-guide.md",
        "key_concepts": lesson.key_concepts,
        "offline_ready": True,
    }
