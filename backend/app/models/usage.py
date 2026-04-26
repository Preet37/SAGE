import datetime

from sqlmodel import SQLModel, Field, UniqueConstraint
from cuid2 import cuid_wrapper

cuid = cuid_wrapper()


class DailyUsage(SQLModel, table=True):
    __tablename__ = "dailyusage"
    __table_args__ = (UniqueConstraint("user_id", "date"),)

    id: str = Field(default_factory=cuid, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    date: datetime.date = Field(default_factory=datetime.date.today, index=True)
    message_count: int = 0
