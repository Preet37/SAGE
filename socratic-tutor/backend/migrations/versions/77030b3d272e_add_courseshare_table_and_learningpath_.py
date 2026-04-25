"""add courseshare table and learningpath sharing columns

Revision ID: 77030b3d272e
Revises: 4169bfdde374
Create Date: 2026-04-11 15:47:59.929920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel  # noqa: F401


revision: str = '77030b3d272e'
down_revision: Union[str, Sequence[str], None] = '4169bfdde374'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_exists(conn, table: str, column: str) -> bool:
    rows = conn.execute(sa.text(f"PRAGMA table_info({table})")).fetchall()
    return any(row[1] == column for row in rows)


def _table_exists(conn, table: str) -> bool:
    rows = conn.execute(
        sa.text("SELECT name FROM sqlite_master WHERE type='table' AND name=:t"),
        {"t": table},
    ).fetchall()
    return len(rows) > 0


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    if not _table_exists(conn, "courseshare"):
        op.create_table('courseshare',
            sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column('learning_path_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column('user_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.ForeignKeyConstraint(['learning_path_id'], ['learningpath.id']),
            sa.ForeignKeyConstraint(['user_id'], ['user.id']),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index('ix_courseshare_learning_path_id', 'courseshare', ['learning_path_id'])
        op.create_index('ix_courseshare_user_id', 'courseshare', ['user_id'])

    if not _column_exists(conn, "learningpath", "created_by"):
        op.add_column('learningpath', sa.Column('created_by', sqlmodel.sql.sqltypes.AutoString(), nullable=True))

    if not _column_exists(conn, "learningpath", "visibility"):
        op.add_column('learningpath', sa.Column('visibility', sqlmodel.sql.sqltypes.AutoString(), nullable=False, server_default='public'))

    if not _column_exists(conn, "learningpath", "share_token"):
        op.add_column('learningpath', sa.Column('share_token', sqlmodel.sql.sqltypes.AutoString(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('courseshare')
    # SQLite doesn't support DROP COLUMN before 3.35; skip column removal
