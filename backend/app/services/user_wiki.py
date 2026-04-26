"""Per-user wiki overlay.

The shared wiki (``content/pedagogy-wiki/``) is canonical and read-only at
serve time. Each learner gets a private overlay directory at
``content/users/{user_id}/wiki/`` where they can drop personal annotations,
custom notes, or topic-specific reminders. The tutor reads from the user
overlay first, then falls back to the shared wiki.

Path traversal is locked down: the user_id and slug are both validated against
a strict regex before being joined to the base directory.
"""

from __future__ import annotations

import re
from pathlib import Path

from ..config import CONTENT_DIR, WIKI_DIR

USERS_ROOT: Path = CONTENT_DIR / "users"

_SAFE_USER_ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
_SAFE_SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{0,80}$")


def _validate_user_id(user_id: str) -> None:
    if not _SAFE_USER_ID.match(user_id):
        raise ValueError(f"Invalid user_id for wiki overlay: {user_id!r}")


def _validate_slug(slug: str) -> None:
    if not _SAFE_SLUG.match(slug):
        raise ValueError(f"Invalid topic slug: {slug!r}")


def user_wiki_root(user_id: str) -> Path:
    """Return the personal wiki root for a user (creating it on first use)."""
    _validate_user_id(user_id)
    root = USERS_ROOT / user_id / "wiki"
    root.mkdir(parents=True, exist_ok=True)
    return root


def user_note_path(user_id: str, topic_slug: str) -> Path:
    """Path to a learner's personal note file for a topic."""
    _validate_slug(topic_slug)
    root = user_wiki_root(user_id)
    return root / "notes" / f"{topic_slug}.md"


def read_user_note(user_id: str, topic_slug: str) -> str:
    """Read a user's note for a topic (empty string if none exists)."""
    path = user_note_path(user_id, topic_slug)
    if not path.is_file():
        return ""
    return path.read_text()


def write_user_note(user_id: str, topic_slug: str, content: str) -> Path:
    """Write a user's note. Empty content removes the file."""
    path = user_note_path(user_id, topic_slug)
    if content.strip() == "":
        path.unlink(missing_ok=True)
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return path


def find_topic_page(topic_slug: str, user_id: str | None = None) -> Path | None:
    """Resolve a topic page, checking the user overlay first when given.

    Returns the full path if found, ``None`` otherwise. Files under the user
    overlay directory take precedence over the shared wiki, which lets a
    learner override or supplement a topic privately without forking the
    canonical wiki.
    """
    _validate_slug(topic_slug)

    if user_id:
        try:
            override = user_wiki_root(user_id) / "topics" / f"{topic_slug}.md"
            if override.is_file():
                return override
        except ValueError:
            # Bad user_id — fall through to shared wiki rather than 500.
            pass

    shared = WIKI_DIR / "resources" / "by-topic" / f"{topic_slug}.md"
    if shared.is_file():
        return shared
    return None
