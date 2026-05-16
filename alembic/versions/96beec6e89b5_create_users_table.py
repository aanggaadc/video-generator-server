"""create users table

Revision ID: 96beec6e89b5
Revises:
Create Date: 2026-05-09 20:11:03.328971
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "96beec6e89b5"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Drop existing table if exists
    op.execute("DROP TABLE IF EXISTS users CASCADE")

    # Create users table
    op.create_table(
        "users",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False
        ),
        sa.Column(
            "name",
            sa.String(),
            nullable=False
        ),
        sa.Column(
            "email",
            sa.String(),
            nullable=False,
            unique=True
        ),
        sa.Column(
            "password",
            sa.String(),
            nullable=False
        ),
        sa.Column(
            "status",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true")
        ),
        sa.Column(
            "email_verified_at",
            sa.TIMESTAMP(),
            nullable=True
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            nullable=False,
            server_default=sa.text("now()")
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            nullable=False,
            server_default=sa.text("now()")
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("users")