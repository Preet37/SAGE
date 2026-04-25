import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..db import get_session
from ..deps import get_current_user
from ..models.user import User
from ..models.learning import Project
from ..schemas.projects import ProjectSummary, ProjectDetail

router = APIRouter(prefix="/projects", tags=["projects"])


def _parse_json_list(raw: str) -> list:
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return []


@router.get("", response_model=List[ProjectSummary])
def list_projects(
    session: Session = Depends(get_session),
    _user: User = Depends(get_current_user),
):
    projects = session.exec(
        select(Project).order_by(Project.order_index)
    ).all()
    return [
        ProjectSummary(
            id=p.id,
            slug=p.slug,
            title=p.title,
            subtitle=p.subtitle,
            course_slug=p.course_slug,
            status=p.status,
            difficulty=p.difficulty,
            hero_emoji=p.hero_emoji,
            concepts=_parse_json_list(p.concepts),
            order_index=p.order_index,
        )
        for p in projects
    ]


@router.get("/{slug}", response_model=ProjectDetail)
def get_project(
    slug: str,
    session: Session = Depends(get_session),
    _user: User = Depends(get_current_user),
):
    project = session.exec(
        select(Project).where(Project.slug == slug)
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return ProjectDetail(
        id=project.id,
        slug=project.slug,
        title=project.title,
        subtitle=project.subtitle,
        course_slug=project.course_slug,
        status=project.status,
        difficulty=project.difficulty,
        hero_emoji=project.hero_emoji,
        vision=project.vision,
        learning_outcomes=_parse_json_list(project.learning_outcomes),
        concepts=_parse_json_list(project.concepts),
        architecture_mermaid=project.architecture_mermaid,
        demo_url=project.demo_url,
        demo_embed=project.demo_embed,
        repo_url=project.repo_url,
        setup_instructions=project.setup_instructions,
        challenges=_parse_json_list(project.challenges),
        related_lesson_slugs=_parse_json_list(project.related_lesson_slugs),
        order_index=project.order_index,
    )
