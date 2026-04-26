from typing import Optional
from sqlmodel import SQLModel, Field
from cuid2 import cuid_wrapper

cuid = cuid_wrapper()


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default_factory=cuid, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
