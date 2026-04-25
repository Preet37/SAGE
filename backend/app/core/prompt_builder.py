"""System prompt builder.

Pulls from the user's accessibility profile, concept mastery, and chosen
teaching mode to shape tone, reading level, and emphasis.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class A11yProfile:
    dyslexia_font: bool = False
    high_contrast: bool = False
    reduce_motion: bool = False
    tts_voice: str = "default"
    reading_level: str = "standard"  # "simple" | "standard" | "advanced"


@dataclass
class ConceptMastery:
    label: str
    mastery: float  # 0.0–1.0


_MODE_DIRECTIVES: dict[str, str] = {
    "default": "Use a clear, balanced Socratic style.",
    "eli5": "Explain like the learner is five. Use everyday objects and simple words.",
    "analogy": "Lead with a vivid analogy from everyday life before any technical detail.",
    "code": "Prefer short code examples; show the smallest snippet that captures the idea.",
    "deep_dive": "Go several levels deep; assume curiosity and tolerance for complexity.",
}


def _a11y_directives(p: A11yProfile) -> list[str]:
    out: list[str] = []
    if p.dyslexia_font or p.reading_level == "simple":
        out += [
            "Use short sentences (≤ 18 words).",
            "Prefer common words; avoid clauses-within-clauses.",
        ]
    if p.reduce_motion:
        out.append("Do not suggest animations or motion-based explanations.")
    if p.tts_voice != "default":
        out.append("Write text that reads naturally aloud; avoid ASCII art and tables.")
    if p.reading_level == "advanced":
        out.append("Assume familiarity with formal vocabulary; be concise.")
    return out


def _mastery_directives(concepts: list[ConceptMastery]) -> list[str]:
    if not concepts:
        return []
    weak = sorted([c for c in concepts if c.mastery < 0.5], key=lambda c: c.mastery)[:3]
    strong = [c for c in concepts if c.mastery >= 0.8]
    out: list[str] = []
    if weak:
        labels = ", ".join(c.label for c in weak)
        out.append(f"The learner is still developing: {labels}. Scaffold these explicitly.")
    if strong:
        labels = ", ".join(c.label for c in strong)
        out.append(
            f"The learner has mastered: {labels}. You may build on these without re-teaching."
        )
    return out


SOCRATIC_CORE = (
    "You are SAGE, a Socratic tutor. Your job is to ask one focused guiding question at a time, "
    "ground every claim in the provided sources, and never invent facts. "
    "If a source does not support an answer, say so plainly."
)
    
EXPERT_TEACHER_CORE = (
    "Act as an expert teacher. Please teach the learner by following these rules:\n"
    "Structure: Break the topic into 5-7 logical modules, from foundational to advanced.\n"
    "Method: For each module, start with a concise lecture (theory + concrete example), followed by 2 check-for-understanding questions.\n"
    "Interaction: Do not proceed to the next module until the check-for-understanding questions are correctly answered.\n"
    "Tone: Clear, patient, and engaging.\n"
    "Relevance: Ensure the questions are directly related to the content just taught.\n"
    "Start with Module 1 unless context shows a module is in progress."
)


def build_system_prompt(
    a11y: A11yProfile,
    mastery: list[ConceptMastery],
    sources: list[str] | None = None,
    objective: str | None = None,
    expert_teacher_mode: bool = True,
) -> str:
    parts: list[str] = [EXPERT_TEACHER_CORE if expert_teacher_mode else SOCRATIC_CORE]

    if objective:
        parts.append(f"Lesson objective: {objective}")

    directives = _a11y_directives(a11y) + _mastery_directives(mastery)
    if directives:
        parts.append("Constraints:\n- " + "\n- ".join(directives))

    if sources:
        joined = "\n\n".join(f"[{i}] {s}" for i, s in enumerate(sources))
        parts.append(f"Sources (cite by [index]):\n{joined}")

    return "\n\n".join(parts)
