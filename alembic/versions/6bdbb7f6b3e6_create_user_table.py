"""create user table

Revision ID: 6bdbb7f6b3e6
Revises: 
Create Date: 2023-06-27 23:17:10.949925

"""
from alembic import op
import sqlalchemy as sa

from app.schemas.user_schema import Roles

# revision identifiers, used by Alembic.
revision = "6bdbb7f6b3e6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("role", sa.Enum(Roles), nullable=False, default="user"),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("(datetime('now', 'localtime'))"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("users")
