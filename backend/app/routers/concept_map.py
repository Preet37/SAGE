"""Concept map API — live knowledge graph of student mastery."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.models.user import User
from app.models.concept import ConceptNode, ConceptEdge, StudentMastery
from app.routers.auth import get_current_user

router = APIRouter(prefix="/concept-map", tags=["concept-map"])


class NodeOut(BaseModel):
    id: int
    label: str
    description: str
    node_type: str
    mastery_score: float = 0.0
    is_mastered: bool = False
    lesson_id: Optional[int]

    class Config:
        from_attributes = True


class EdgeOut(BaseModel):
    id: int
    source_id: int
    target_id: int
    edge_type: str
    weight: float

    class Config:
        from_attributes = True


class MasteryUpdate(BaseModel):
    concept_id: int
    score: float  # 0.0 - 1.0


@router.get("/{course_id}")
async def get_concept_map(
    course_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Return the full concept graph with student mastery overlaid."""
    nodes_result = await db.execute(
        select(ConceptNode).where(ConceptNode.course_id == course_id)
    )
    nodes = nodes_result.scalars().all()

    mastery_result = await db.execute(
        select(StudentMastery).where(StudentMastery.user_id == user.id)
    )
    mastery_map = {m.concept_id: m for m in mastery_result.scalars().all()}

    node_ids = [n.id for n in nodes]
    edges_result = await db.execute(
        select(ConceptEdge).where(
            ConceptEdge.source_id.in_(node_ids),
            ConceptEdge.target_id.in_(node_ids),
        )
    )
    edges = edges_result.scalars().all()

    nodes_out = []
    for node in nodes:
        m = mastery_map.get(node.id)
        nodes_out.append({
            "id": node.id,
            "label": node.label,
            "description": node.description,
            "node_type": node.node_type,
            "lesson_id": node.lesson_id,
            "mastery_score": m.score if m else 0.0,
            "is_mastered": m.is_mastered if m else False,
        })

    edges_out = [
        {"id": e.id, "source_id": e.source_id, "target_id": e.target_id,
         "edge_type": e.edge_type, "weight": e.weight}
        for e in edges
    ]

    return {"nodes": nodes_out, "edges": edges_out}


@router.post("/mastery")
async def update_mastery(
    update: MasteryUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    update.score = max(0.0, min(1.0, update.score))
    result = await db.execute(
        select(StudentMastery).where(
            and_(
                StudentMastery.user_id == user.id,
                StudentMastery.concept_id == update.concept_id,
            )
        )
    )
    mastery = result.scalar_one_or_none()

    if mastery:
        mastery.score = max(mastery.score, update.score)
        mastery.attempts += 1
        mastery.is_mastered = mastery.score >= 0.8
    else:
        mastery = StudentMastery(
            user_id=user.id,
            concept_id=update.concept_id,
            score=update.score,
            attempts=1,
            is_mastered=update.score >= 0.8,
        )
        db.add(mastery)

    await db.commit()
    return {"concept_id": update.concept_id, "score": mastery.score, "is_mastered": mastery.is_mastered}


@router.get("/next/{course_id}")
async def get_next_concepts(
    course_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Return the 3 concepts the Progress Agent recommends studying next."""
    nodes_result = await db.execute(
        select(ConceptNode).where(ConceptNode.course_id == course_id)
    )
    nodes = {n.id: n for n in nodes_result.scalars().all()}

    mastery_result = await db.execute(
        select(StudentMastery).where(StudentMastery.user_id == user.id)
    )
    mastery = {m.concept_id: m for m in mastery_result.scalars().all()}
    unvisited = [
        n for n in nodes.values()
        if n.id not in mastery or not mastery[n.id].is_mastered
    ]
    unvisited.sort(key=lambda n: (mastery.get(n.id).score if n.id in mastery else 0.0, n.id))

    return [{"id": n.id, "label": n.label, "description": n.description} for n in unvisited[:3]]
