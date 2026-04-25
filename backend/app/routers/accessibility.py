"""
Accessibility router — SAGE adapts to every learner's needs.
Students declare disabilities/preferences and the system adjusts
pedagogy, formatting, pacing, and peer matching accordingly.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/accessibility", tags=["accessibility"])

DISABILITY_PROFILES = {
    "dyslexia": {
        "label": "Dyslexia",
        "description": "Difficulty with reading, letter recognition, text processing",
        "prompt_modifier": (
            "ACCESSIBILITY - DYSLEXIA: Use short sentences (max 15 words). "
            "Use bullet points instead of paragraphs. "
            "Avoid walls of text. Bold key terms. "
            "Use concrete examples and avoid abstract descriptions. "
            "Never use italics for emphasis — use **bold** instead. "
            "Prefer numbered steps over prose explanations."
        ),
        "ui_hints": ["large_font", "high_contrast", "short_paragraphs"],
    },
    "adhd": {
        "label": "ADHD / Attention Difficulties",
        "description": "Difficulty sustaining attention, easily distracted",
        "prompt_modifier": (
            "ACCESSIBILITY - ADHD: Keep each response to ONE core idea. "
            "Start with a 1-sentence TL;DR. "
            "Use frequent check-in questions to re-engage. "
            "Break problems into tiny 2-3 step chunks. "
            "Celebrate small wins explicitly. "
            "Suggest short 5-minute focus sprints. "
            "Use emojis sparingly to mark key points."
        ),
        "ui_hints": ["focus_mode", "progress_bars", "short_sessions"],
    },
    "visual_impairment": {
        "label": "Visual Impairment",
        "description": "Low vision or blindness, relies on screen readers",
        "prompt_modifier": (
            "ACCESSIBILITY - VISUAL IMPAIRMENT: Never rely on visual formatting alone. "
            "Describe all diagrams and graphs in text. "
            "Avoid ASCII art or visual tables. "
            "Structure responses with clear heading levels. "
            "All code examples should include text explanations of what each line does. "
            "Use semantic HTML-friendly markdown structure."
        ),
        "ui_hints": ["screen_reader", "high_contrast", "large_font", "voice_output"],
    },
    "hearing_impairment": {
        "label": "Hearing Impairment",
        "description": "Deaf or hard of hearing",
        "prompt_modifier": (
            "ACCESSIBILITY - HEARING IMPAIRMENT: Rely entirely on visual/text-based explanations. "
            "Do not reference audio examples. "
            "Provide captions or transcripts for any referenced media. "
            "Use visual analogies and diagrams described in text."
        ),
        "ui_hints": ["no_voice_ui", "visual_alerts", "text_primary"],
    },
    "dyscalculia": {
        "label": "Dyscalculia",
        "description": "Difficulty with numbers and mathematical concepts",
        "prompt_modifier": (
            "ACCESSIBILITY - DYSCALCULIA: Always provide real-world meaning before math symbols. "
            "Step through every calculation slowly, one operation at a time. "
            "Use diagrams and visual representations when possible (described in text). "
            "Never assume numerical intuition — explain the 'why' behind every number. "
            "Use tables to organize numbers clearly. "
            "Provide worked examples first, then ask the student to try."
        ),
        "ui_hints": ["slow_math", "step_by_step", "no_symbol_overload"],
    },
    "autism": {
        "label": "Autism Spectrum",
        "description": "Prefers direct communication, literal language, clear structure",
        "prompt_modifier": (
            "ACCESSIBILITY - AUTISM SPECTRUM: Use literal, direct language. "
            "Avoid metaphors, sarcasm, or idioms without explanation. "
            "Provide extremely clear structure with explicit transitions. "
            "State expectations directly at the start. "
            "Avoid vague phrases like 'think about it' — be specific. "
            "Warn before topic changes. "
            "Respect deep focus on one topic without rushing."
        ),
        "ui_hints": ["predictable_layout", "no_sudden_changes", "explicit_structure"],
    },
    "esl": {
        "label": "English as Second Language",
        "description": "Non-native English speaker",
        "prompt_modifier": (
            "ACCESSIBILITY - ESL LEARNER: Use simple vocabulary. "
            "Avoid idioms and colloquialisms. "
            "Define technical terms the first time they appear. "
            "Use short, clear sentences. "
            "Provide translations of key concepts when helpful (bracket the original term). "
            "Be patient and ask for confirmation of understanding frequently."
        ),
        "ui_hints": ["simple_language", "term_glossary"],
    },
    "cognitive_load": {
        "label": "Cognitive Load / Processing Speed",
        "description": "Needs slower pacing, more repetition, simpler chunks",
        "prompt_modifier": (
            "ACCESSIBILITY - COGNITIVE LOAD: Introduce one concept at a time. "
            "Recap the previous point before moving forward. "
            "Use scaffolding — always build on what was just covered. "
            "Ask comprehension checks after every explanation. "
            "Avoid introducing more than 3 new terms per response. "
            "Prefer repetition and practice over breadth."
        ),
        "ui_hints": ["slow_pacing", "frequent_recaps", "comprehension_checks"],
    },
}

STRENGTH_PROFILES = {
    "visual_learner": "Use diagrams, graphs, and spatial descriptions. Describe visual relationships.",
    "auditory_learner": "Explain as if talking through the concept aloud. Use rhythm and patterns.",
    "kinesthetic_learner": "Relate concepts to physical actions and hands-on experiments.",
    "reading_learner": "Provide detailed written explanations, suggest readings, use structured notes.",
}


class AccessibilityProfile(BaseModel):
    disabilities: list[str] = []
    strengths: list[str] = []
    preferred_language: str = "en"
    font_size: str = "medium"  # small | medium | large | xl
    reduce_motion: bool = False
    voice_speed: float = 1.0
    custom_note: str = ""


class ProfileOut(BaseModel):
    disabilities: list[str]
    strengths: list[str]
    preferred_language: str
    font_size: str
    reduce_motion: bool
    voice_speed: float
    custom_note: str
    prompt_modifier: str
    ui_hints: list[str]


@router.get("/profiles")
async def list_profiles():
    """Return all available accessibility profiles."""
    return {
        "disabilities": [
            {"id": k, "label": v["label"], "description": v["description"]}
            for k, v in DISABILITY_PROFILES.items()
        ],
        "strengths": [
            {"id": k, "label": k.replace("_", " ").title(), "description": v}
            for k, v in STRENGTH_PROFILES.items()
        ],
    }


@router.get("/me")
async def get_my_profile(user: User = Depends(get_current_user)):
    """Get the current user's accessibility profile."""
    profile_data = user.accessibility_profile or {}
    disabilities = profile_data.get("disabilities", [])
    strengths = profile_data.get("strengths", [])

    prompt_modifier = _build_prompt_modifier(disabilities, strengths, profile_data.get("custom_note", ""))
    ui_hints = _collect_ui_hints(disabilities)

    return ProfileOut(
        disabilities=disabilities,
        strengths=strengths,
        preferred_language=profile_data.get("preferred_language", "en"),
        font_size=profile_data.get("font_size", "medium"),
        reduce_motion=profile_data.get("reduce_motion", False),
        voice_speed=profile_data.get("voice_speed", 1.0),
        custom_note=profile_data.get("custom_note", ""),
        prompt_modifier=prompt_modifier,
        ui_hints=ui_hints,
    )


@router.post("/me")
async def update_my_profile(
    profile: AccessibilityProfile,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update accessibility profile — immediately affects all future tutor responses."""
    invalid = [d for d in profile.disabilities if d not in DISABILITY_PROFILES]
    if invalid:
        raise HTTPException(400, f"Unknown disability IDs: {invalid}")

    invalid_s = [s for s in profile.strengths if s not in STRENGTH_PROFILES]
    if invalid_s:
        raise HTTPException(400, f"Unknown strength IDs: {invalid_s}")

    user.accessibility_profile = profile.model_dump()
    db.add(user)
    await db.commit()

    prompt_modifier = _build_prompt_modifier(profile.disabilities, profile.strengths, profile.custom_note)
    ui_hints = _collect_ui_hints(profile.disabilities)

    return {
        "saved": True,
        "prompt_modifier": prompt_modifier,
        "ui_hints": ui_hints,
        "active_profiles": [DISABILITY_PROFILES[d]["label"] for d in profile.disabilities],
    }


def _build_prompt_modifier(disabilities: list[str], strengths: list[str], custom: str) -> str:
    parts = []
    for d in disabilities:
        if d in DISABILITY_PROFILES:
            parts.append(DISABILITY_PROFILES[d]["prompt_modifier"])
    for s in strengths:
        if s in STRENGTH_PROFILES:
            parts.append(f"LEARNING STRENGTH - {s.upper()}: {STRENGTH_PROFILES[s]}")
    if custom:
        parts.append(f"STUDENT NOTE: {custom}")
    return "\n\n".join(parts)


def _collect_ui_hints(disabilities: list[str]) -> list[str]:
    hints = []
    for d in disabilities:
        if d in DISABILITY_PROFILES:
            hints.extend(DISABILITY_PROFILES[d]["ui_hints"])
    return list(set(hints))


def get_user_accessibility_modifier(user: User) -> str:
    """Helper called by the tutor router to inject accessibility context."""
    profile_data = getattr(user, "accessibility_profile", None) or {}
    disabilities = profile_data.get("disabilities", [])
    strengths = profile_data.get("strengths", [])
    custom = profile_data.get("custom_note", "")
    return _build_prompt_modifier(disabilities, strengths, custom)
