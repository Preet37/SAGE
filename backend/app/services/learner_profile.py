"""Helpers for the learner profile — DB access + system-prompt summary."""

from __future__ import annotations

import json
import logging
from datetime import datetime

from sqlmodel import Session

from ..db import engine
from ..models.profile import LearnerProfile

logger = logging.getLogger(__name__)

# Whitelisted values the tutor recognizes. The DB column is free-form so
# adding a new option doesn't require a migration; unknown values fall back
# to ``unspecified``/``default`` in the prompt summary.
EXPERTISE_LEVELS = {"beginner", "intermediate", "advanced", "unspecified"}
PREFERRED_STYLES = {"default", "eli5", "analogy", "code", "deep_dive"}


def get_or_create(user_id: str) -> LearnerProfile:
    with Session(engine) as session:
        profile = session.get(LearnerProfile, user_id)
        if profile is None:
            profile = LearnerProfile(user_id=user_id)
            session.add(profile)
            session.commit()
            session.refresh(profile)
        return profile


def update_profile(
    user_id: str,
    *,
    expertise_level: str | None = None,
    preferred_style: str | None = None,
    interests: list[str] | None = None,
    goals: str | None = None,
) -> LearnerProfile:
    with Session(engine) as session:
        profile = session.get(LearnerProfile, user_id)
        if profile is None:
            profile = LearnerProfile(user_id=user_id)
            session.add(profile)
        if expertise_level is not None:
            profile.expertise_level = (
                expertise_level if expertise_level in EXPERTISE_LEVELS else "unspecified"
            )
        if preferred_style is not None:
            profile.preferred_style = (
                preferred_style if preferred_style in PREFERRED_STYLES else "default"
            )
        if interests is not None:
            cleaned = [t.strip()[:40] for t in interests if isinstance(t, str) and t.strip()]
            profile.interests = json.dumps(cleaned[:20])
        if goals is not None:
            profile.goals = goals[:500]
        profile.updated_at = datetime.utcnow()
        session.add(profile)
        session.commit()
        session.refresh(profile)
        return profile


def interests_list(profile: LearnerProfile) -> list[str]:
    try:
        data = json.loads(profile.interests or "[]")
        return [t for t in data if isinstance(t, str)]
    except json.JSONDecodeError:
        return []


def profile_summary_for_prompt(user_id: str) -> str:
    """Build a 2-4 line summary the agent loop folds into the system prompt.

    Returns an empty string when the profile is empty/unspecified — the prompt
    builder skips the section entirely in that case.
    """
    profile = get_or_create(user_id)
    lines: list[str] = []
    if profile.expertise_level and profile.expertise_level != "unspecified":
        lines.append(f"Self-described expertise: {profile.expertise_level}.")
    if profile.preferred_style and profile.preferred_style != "default":
        lines.append(f"Preferred explanation style: {profile.preferred_style}.")
    interests = interests_list(profile)
    if interests:
        lines.append("Interests: " + ", ".join(interests[:8]) + ".")
    if profile.goals:
        lines.append(f"Goal: {profile.goals.strip()}")
    if not lines:
        return ""
    lines.append(
        "Adapt depth, vocabulary, and analogies to the above without "
        "explicitly mentioning the profile."
    )
    return "\n".join(lines)
