"""Models for the Arista 'Connect the Dots' track: peer presence + resource cache."""

from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from cuid2 import cuid_wrapper

cuid = cuid_wrapper()


class PeerPresence(SQLModel, table=True):
    """Snapshot of a learner's current activity for peer matching.

    A row exists per (user_id, lesson_id) pair and is upserted on heartbeat.
    A user is 'online' if `last_seen` is within the activity window
    (managed by the network router).
    """

    __tablename__ = "peerpresence"

    id: str = Field(default_factory=cuid, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    lesson_id: Optional[str] = Field(default=None, foreign_key="lesson.id", index=True)
    display_name: str = ""
    status: str = "studying"            # "studying" | "stuck" | "review" | "idle"
    note: str = ""                      # optional public message ("looking for a study buddy")
    looking_for_pair: bool = False
    last_seen: datetime = Field(default_factory=datetime.utcnow, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ResourceCacheEntry(SQLModel, table=True):
    """Cached external resource (arXiv paper, GitHub repo, YouTube video, etc.)
    pulled by the resource router. Cached so repeated queries don't hammer APIs.
    """

    __tablename__ = "resourcecacheentry"

    id: str = Field(default_factory=cuid, primary_key=True)
    query_hash: str = Field(index=True)         # sha1 of (source, query)
    source: str                                 # "arxiv" | "github" | "youtube" | "wiki"
    payload: str                                # JSON-serialized list of items
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
