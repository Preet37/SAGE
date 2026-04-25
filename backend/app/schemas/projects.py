from typing import List, Optional
from pydantic import BaseModel


class ProjectSummary(BaseModel):
    id: str
    slug: str
    title: str
    subtitle: str
    course_slug: str
    status: str
    difficulty: str
    hero_emoji: str
    concepts: List[str]
    order_index: int


class ProjectDetail(BaseModel):
    id: str
    slug: str
    title: str
    subtitle: str
    course_slug: str
    status: str
    difficulty: str
    hero_emoji: str
    vision: str
    learning_outcomes: List[str]
    concepts: List[str]
    architecture_mermaid: str
    demo_url: str
    demo_embed: bool
    repo_url: str
    setup_instructions: str
    challenges: List[str]
    related_lesson_slugs: List[str]
    order_index: int
