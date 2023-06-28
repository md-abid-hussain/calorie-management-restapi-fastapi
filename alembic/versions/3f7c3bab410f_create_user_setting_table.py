"""create user setting table

Revision ID: 3f7c3bab410f
Revises: 00d47e4ae9b5
Create Date: 2023-06-28 10:39:43.031666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3f7c3bab410f"
down_revision = "00d47e4ae9b5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_settings",
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
        ),
        sa.Column(
            "expected_calories", sa.Integer, nullable=False, default=sa.text("2250")
        ),
    )


def downgrade() -> None:
    op.drop_table("user_settings")
