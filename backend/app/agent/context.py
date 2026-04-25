from dataclasses import dataclass, field


@dataclass
class TutorContext:
    lesson_id: str
    lesson_title: str
    lesson_summary: str
    concepts: list[str]
    completed_lesson_titles: list[str]
    mode: str = "default"
    lesson_content: str = ""
    reference_kb: str = ""
    curriculum_index: list[dict] = field(default_factory=list)
    domain: str = "technical"
    available_images: list[dict] = field(default_factory=list)
    # Exploration mode fields (all optional, backward compatible)
    exploration_mode: bool = False
    available_courses: list[dict] = field(default_factory=list)
    # Cognition track: identifiers used by verifier + semantic memory
    user_id: str = ""
    session_id: str = ""
    memory_block: str = ""
