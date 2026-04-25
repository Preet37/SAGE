from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from cuid2 import cuid_wrapper

cuid = cuid_wrapper()


class LearningPath(SQLModel, table=True):
    __tablename__ = "learningpath"

    id: str = Field(default_factory=cuid, primary_key=True)
    slug: str = Field(unique=True, index=True)
    title: str
    description: str
    level: str = "beginner"
    order_index: int = 0
    created_by: Optional[str] = Field(default=None, foreign_key="user.id", index=True)
    visibility: str = Field(default="public")  # "public" | "private"
    share_token: Optional[str] = Field(default=None, index=True)

    modules: List["Module"] = Relationship(back_populates="learning_path")


class CourseShare(SQLModel, table=True):
    __tablename__ = "courseshare"

    id: str = Field(default_factory=cuid, primary_key=True)
    learning_path_id: str = Field(foreign_key="learningpath.id", index=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    shared_at: datetime = Field(default_factory=datetime.utcnow)


class Module(SQLModel, table=True):
    __tablename__ = "module"

    id: str = Field(default_factory=cuid, primary_key=True)
    learning_path_id: str = Field(foreign_key="learningpath.id")
    title: str
    order_index: int

    learning_path: Optional[LearningPath] = Relationship(back_populates="modules")
    lessons: List["Lesson"] = Relationship(back_populates="module")


class Lesson(SQLModel, table=True):
    __tablename__ = "lesson"

    id: str = Field(default_factory=cuid, primary_key=True)
    module_id: str = Field(foreign_key="module.id")
    title: str
    slug: str
    content: str           # Markdown body
    summary: str           # 1-2 sentences for system prompt
    concepts: str          # JSON array: ["backpropagation", "relu"]
    order_index: int
    youtube_id: Optional[str] = None
    video_title: Optional[str] = None
    vimeo_url: Optional[str] = None
    transcript: Optional[str] = None
    reference_kb: Optional[str] = None  # Pre-searched detailed knowledge for LLM grounding
    sources_used: Optional[str] = None  # JSON array of source URLs used to generate this lesson
    image_metadata: Optional[str] = None  # JSON array of image entries from those sources

    module: Optional[Module] = Relationship(back_populates="lessons")


class Project(SQLModel, table=True):
    __tablename__ = "project"

    id: str = Field(default_factory=cuid, primary_key=True)
    slug: str = Field(index=True, unique=True)
    title: str
    subtitle: str = ""
    course_slug: str = ""
    status: str = "coming_soon"
    difficulty: str = "intermediate"
    hero_emoji: str = ""
    vision: str = ""
    learning_outcomes: str = "[]"
    concepts: str = "[]"
    architecture_mermaid: str = ""
    demo_url: str = ""
    demo_embed: bool = False
    repo_url: str = ""
    setup_instructions: str = ""
    challenges: str = "[]"
    related_lesson_slugs: str = "[]"
    order_index: int = 0
