"""add learnerprofile table

Revision ID: 9c1f4a3e2b80
Revises: 77030b3d272e
Create Date: 2026-04-25

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel  # noqa: F401
from alembic import op


revision: str = "9c1f4a3e2b80"
down_revision: Union[str, Sequence[str], None] = "77030b3d272e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(conn, table: str) -> bool:
    rows = conn.execute(
        sa.text("SELECT name FROM sqlite_master WHERE type='table' AND name=:t"),
        {"t": table},
    ).fetchall()
    return len(rows) > 0


def upgrade() -> None:
    conn = op.get_bind()
    if _table_exists(conn, "learnerprofile"):
        return
    op.create_table(
        "learnerprofile",
        sa.Column(
            "user_id",
            sqlmodel.sql.sqltypes.AutoString(),
            sa.ForeignKey("user.id"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "expertise_level",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
            server_default="unspecified",
        ),
        sa.Column(
            "preferred_style",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
            server_default="default",
        ),
        sa.Column(
            "interests",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
            server_default="[]",
        ),
        sa.Column(
            "goals",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
            server_default="",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
    )


def downgrade() -> None:
    op.drop_table("learnerprofile")
