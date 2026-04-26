"""Per-user wiki overlay — personal notes layered on top of the shared wiki.

Each learner gets a private storage area under
``content/users/{user_id}/wiki/`` where they can keep notes per topic without
touching the canonical wiki. This router exposes read/write endpoints; the
filesystem layer (and path-traversal hardening) lives in
``services/user_wiki.py``.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..deps import get_current_user
from ..models.user import User
from ..services.user_wiki import read_user_note, write_user_note

router = APIRouter(prefix="/wiki/notes", tags=["wiki-notes"])


class NotePayload(BaseModel):
    content: str


@router.get("/{topic_slug}")
def get_note(topic_slug: str, user: User = Depends(get_current_user)):
    """Read the current learner's personal note for a topic."""
    try:
        content = read_user_note(user.id, topic_slug)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"topic_slug": topic_slug, "content": content}


@router.put("/{topic_slug}")
def put_note(
    topic_slug: str,
    payload: NotePayload,
    user: User = Depends(get_current_user),
):
    """Write a learner's personal note. Empty content deletes the file."""
    try:
        write_user_note(user.id, topic_slug, payload.content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"topic_slug": topic_slug, "saved": True}
