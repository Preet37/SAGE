"""
Seed script for SocraticTutor curriculum.

Scans content/*/course.json for course packages and loads them into the
database.  Each course.json follows a standard schema — see content/README.md.

Run with:  python seed.py   (from the backend/ directory)
"""
import json
import re
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from sqlmodel import Session, select
from app.db import engine, run_migrations
from app.models.learning import LearningPath, Module, Lesson, Project
from app.models.concept import ConceptPage  # noqa: F401 — imported so table is created
from app.models.user import User  # noqa: F401 — imported so table is created
from app.models.progress import UserLessonProgress, ChatMessage  # noqa: F401

_BACKEND_DIR = Path(__file__).resolve().parent
from app.config import CONTENT_DIR as _CONTENT_DIR  # noqa: E402


def _strip_html(html: str) -> str:
    """Remove HTML tags and normalize whitespace."""
    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", text).strip()


def _load_enrichment(course_slug: str, lesson_slug: str) -> str | None:
    """Load a reference KB markdown file from the course enrichment dir."""
    kb_path = _CONTENT_DIR / course_slug / "enrichment" / f"{lesson_slug}_reference_kb.md"
    if kb_path.exists():
        return kb_path.read_text()
    return None


def _seed_course(session: Session, course: dict, order_index: int = 99) -> None:
    """Seed or update a single course from a course.json dict.

    - If the LearningPath doesn't exist, creates everything fresh.
    - If it already exists, updates lesson content/summary/concepts
      while **preserving** existing ``reference_kb`` unless a new enrichment
      file is present.
    """
    slug = course["slug"]
    existing_path = session.exec(
        select(LearningPath).where(LearningPath.slug == slug)
    ).first()

    order = course.get("order", order_index)

    if existing_path:
        existing_path.order_index = order
        existing_path.visibility = "public"
        session.add(existing_path)
        print(f"\n  {course['title']} already exists — updating content (preserving reference_kb)...")
        updated = 0
        created = 0
        for mod_data in course["modules"]:
            mod = session.exec(
                select(Module).where(
                    Module.learning_path_id == existing_path.id,
                    Module.order_index == mod_data["order_index"],
                )
            ).first()
            if not mod:
                mod = Module(
                    learning_path_id=existing_path.id,
                    title=mod_data["title"],
                    order_index=mod_data["order_index"],
                )
                session.add(mod)
                session.flush()

            for lesson_data in mod_data["lessons"]:
                lesson = session.exec(
                    select(Lesson).where(Lesson.slug == lesson_data["slug"])
                ).first()

                content = lesson_data.get("content", "")
                summary = lesson_data.get("summary", "")
                concepts = lesson_data.get("concepts", [])
                enrichment = _load_enrichment(slug, lesson_data["slug"])

                if lesson:
                    if content:
                        lesson.content = content
                    if summary:
                        lesson.summary = summary
                    lesson.concepts = json.dumps(concepts)
                    if enrichment:
                        lesson.reference_kb = enrichment
                    if lesson_data.get("youtube_id"):
                        lesson.youtube_id = lesson_data["youtube_id"]
                    if lesson_data.get("video_title"):
                        lesson.video_title = lesson_data["video_title"]
                    sources = lesson_data.get("sources_used")
                    if sources:
                        lesson.sources_used = json.dumps(sources) if isinstance(sources, list) else sources
                    images = lesson_data.get("image_metadata")
                    if images:
                        lesson.image_metadata = json.dumps(images) if isinstance(images, list) else images
                    session.add(lesson)
                    updated += 1
                else:
                    sources = lesson_data.get("sources_used")
                    images = lesson_data.get("image_metadata")
                    lesson = Lesson(
                        module_id=mod.id,
                        title=lesson_data["title"],
                        slug=lesson_data["slug"],
                        order_index=lesson_data.get("order_index", 0),
                        content=content or "*Content pending.*",
                        summary=summary or f"This lesson covers {lesson_data['title']}.",
                        concepts=json.dumps(concepts),
                        youtube_id=lesson_data.get("youtube_id"),
                        video_title=lesson_data.get("video_title"),
                        vimeo_url=lesson_data.get("vimeo_url"),
                        transcript=lesson_data.get("transcript"),
                        reference_kb=enrichment,
                        sources_used=json.dumps(sources) if isinstance(sources, list) else sources,
                        image_metadata=json.dumps(images) if isinstance(images, list) else images,
                    )
                    session.add(lesson)
                    created += 1

        session.commit()
        msg = f"  Updated {updated} lessons."
        if created:
            msg += f" Created {created} new lesson(s)."
        print(msg)
        return

    print(f"\n  Creating LearningPath: {course['title']}...")
    path = LearningPath(
        slug=slug,
        title=course["title"],
        description=course["description"],
        level=course.get("level", "beginner"),
        order_index=order,
        visibility="public",
    )
    session.add(path)
    session.flush()

    module_count = 0
    lesson_count = 0

    for mod_data in course["modules"]:
        mod = Module(
            learning_path_id=path.id,
            title=mod_data["title"],
            order_index=mod_data["order_index"],
        )
        session.add(mod)
        session.flush()
        module_count += 1

        for lesson_data in mod_data["lessons"]:
            content = lesson_data.get("content", "")
            summary = lesson_data.get("summary", "")

            if not content and not lesson_data.get("transcript"):
                summary = summary or f"Video lesson: {lesson_data['title']}"
                content = "*Content pending — no transcript or description available.*"

            enrichment = _load_enrichment(slug, lesson_data["slug"])

            lesson = Lesson(
                module_id=mod.id,
                title=lesson_data["title"],
                slug=lesson_data["slug"],
                order_index=lesson_data.get("order_index", 0),
                content=content,
                summary=summary or f"This lesson covers {lesson_data['title']}.",
                concepts=json.dumps(lesson_data.get("concepts", [])),
                youtube_id=lesson_data.get("youtube_id"),
                video_title=lesson_data.get("video_title"),
                vimeo_url=lesson_data.get("vimeo_url"),
                transcript=lesson_data.get("transcript"),
                reference_kb=enrichment,
            )
            session.add(lesson)
            lesson_count += 1

    session.commit()
    print(f"  Created: {module_count} modules, {lesson_count} lessons")


def seed():
    """Scan content/*/course.json and seed all discovered courses."""
    print("Creating database tables...")
    run_migrations()

    if not _CONTENT_DIR.exists():
        print(f"No content directory found at {_CONTENT_DIR}")
        print("Add course packages under content/<slug>/course.json")
        return

    _PRIVATE_PREFIXES = ("private-",)
    course_files = sorted(
        p for p in _CONTENT_DIR.glob("*/course.json")
        if not p.parent.name.startswith(_PRIVATE_PREFIXES)
    )
    if not course_files:
        print(f"No course.json files found in {_CONTENT_DIR}/*/")
        print("Add course packages under content/<slug>/course.json")
        return

    print(f"Found {len(course_files)} course(s) in {_CONTENT_DIR}")

    courses = []
    for course_file in course_files:
        with open(course_file) as f:
            course = json.load(f)
        courses.append(course)
    courses.sort(key=lambda c: (c.get("order", 999), c.get("title", "")))

    with Session(engine) as session:
        for idx, course in enumerate(courses):
            _seed_course(session, course, order_index=idx)

    _seed_preloaded_concepts()
    _seed_projects()
    print("\nSeed complete!")


def _seed_preloaded_concepts():
    """Load pre-generated concept pages from content/preloaded_concepts.json."""
    concepts_file = _CONTENT_DIR / "preloaded_concepts.json"
    if not concepts_file.exists():
        return

    with open(concepts_file) as f:
        concepts = json.load(f)

    with Session(engine) as session:
        existing = {
            row.topic.lower()
            for row in session.exec(select(ConceptPage)).all()
        }
        created = 0
        for c in concepts:
            if c["topic"].lower() in existing:
                continue
            page = ConceptPage(
                topic=c["topic"],
                level=c.get("level", "intermediate"),
                simple_definition=c.get("simple_definition", ""),
                why_it_matters=c.get("why_it_matters", ""),
                detailed_explanation=c.get("detailed_explanation", ""),
                analogy=c.get("analogy", ""),
                real_world_example=c.get("real_world_example", ""),
                misconceptions=json.dumps(c.get("misconceptions", [])),
                key_takeaways=json.dumps(c.get("key_takeaways", [])),
                related_concepts=json.dumps(c.get("related_concepts", [])),
                further_reading=json.dumps(c.get("further_reading", [])),
                lesson_id=c.get("lesson_id"),
            )
            session.add(page)
            created += 1

        if created:
            session.commit()
        print(f"\n  Concept pages: {len(existing)} already cached, {created} loaded from preloaded_concepts.json")


def _seed_projects():
    """Load project definitions from content/projects/*.json."""
    projects_dir = _CONTENT_DIR / "projects"
    if not projects_dir.exists():
        return

    project_files = sorted(projects_dir.glob("*.json"))
    if not project_files:
        return

    with Session(engine) as session:
        created = 0
        updated = 0
        for pf in project_files:
            with open(pf) as f:
                data = json.load(f)

            slug = data["slug"]
            existing = session.exec(
                select(Project).where(Project.slug == slug)
            ).first()

            if existing:
                existing.title = data.get("title", existing.title)
                existing.subtitle = data.get("subtitle", "")
                existing.course_slug = data.get("course_slug", "")
                existing.status = data.get("status", "coming_soon")
                existing.difficulty = data.get("difficulty", "intermediate")
                existing.hero_emoji = data.get("hero_emoji", "")
                existing.vision = data.get("vision", "")
                existing.learning_outcomes = json.dumps(data.get("learning_outcomes", []))
                existing.concepts = json.dumps(data.get("concepts", []))
                existing.architecture_mermaid = data.get("architecture_mermaid", "")
                existing.demo_url = data.get("demo_url", "")
                existing.demo_embed = data.get("demo_embed", False)
                existing.repo_url = data.get("repo_url", "")
                existing.setup_instructions = data.get("setup_instructions", "")
                existing.challenges = json.dumps(data.get("challenges", []))
                existing.related_lesson_slugs = json.dumps(data.get("related_lesson_slugs", []))
                existing.order_index = data.get("order_index", 0)
                session.add(existing)
                updated += 1
            else:
                project = Project(
                    slug=slug,
                    title=data.get("title", slug),
                    subtitle=data.get("subtitle", ""),
                    course_slug=data.get("course_slug", ""),
                    status=data.get("status", "coming_soon"),
                    difficulty=data.get("difficulty", "intermediate"),
                    hero_emoji=data.get("hero_emoji", ""),
                    vision=data.get("vision", ""),
                    learning_outcomes=json.dumps(data.get("learning_outcomes", [])),
                    concepts=json.dumps(data.get("concepts", [])),
                    architecture_mermaid=data.get("architecture_mermaid", ""),
                    demo_url=data.get("demo_url", ""),
                    demo_embed=data.get("demo_embed", False),
                    repo_url=data.get("repo_url", ""),
                    setup_instructions=data.get("setup_instructions", ""),
                    challenges=json.dumps(data.get("challenges", [])),
                    related_lesson_slugs=json.dumps(data.get("related_lesson_slugs", [])),
                    order_index=data.get("order_index", 0),
                )
                session.add(project)
                created += 1

        session.commit()
        print(f"\n  Projects: {updated} updated, {created} created")


if __name__ == "__main__":
    seed()
