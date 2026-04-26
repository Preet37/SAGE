"""Learner profile API."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ..deps import get_current_user
from ..models.user import User
from ..models.profile import LearnerProfile
from ..services.learner_profile import (
    EXPERTISE_LEVELS,
    PREFERRED_STYLES,
    get_or_create,
    interests_list,
    update_profile,
)

router = APIRouter(prefix="/profile", tags=["profile"])


class ProfileResponse(BaseModel):
    user_id: str
    expertise_level: str
    preferred_style: str
    interests: list[str]
    goals: str
    updated_at: str


class ProfilePatch(BaseModel):
    expertise_level: str | None = Field(default=None)
    preferred_style: str | None = Field(default=None)
    interests: list[str] | None = Field(default=None)
    goals: str | None = Field(default=None)


def _serialize(profile: LearnerProfile) -> ProfileResponse:
    return ProfileResponse(
        user_id=profile.user_id,
        expertise_level=profile.expertise_level,
        preferred_style=profile.preferred_style,
        interests=interests_list(profile),
        goals=profile.goals,
        updated_at=profile.updated_at.isoformat(),
    )


@router.get("/me", response_model=ProfileResponse)
def get_me(user: User = Depends(get_current_user)):
    return _serialize(get_or_create(user.id))


@router.patch("/me", response_model=ProfileResponse)
def update_me(payload: ProfilePatch, user: User = Depends(get_current_user)):
    profile = update_profile(
        user.id,
        expertise_level=payload.expertise_level,
        preferred_style=payload.preferred_style,
        interests=payload.interests,
        goals=payload.goals,
    )
    return _serialize(profile)


@router.get("/options")
def profile_options(_user: User = Depends(get_current_user)):
    """Return the canonical option lists for the settings UI."""
    return {
        "expertise_levels": sorted(EXPERTISE_LEVELS),
        "preferred_styles": sorted(PREFERRED_STYLES),
    }
