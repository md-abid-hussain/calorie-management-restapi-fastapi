"""create entries table

Revision ID: 00d47e4ae9b5
Revises: 6bdbb7f6b3e6
Create Date: 2023-06-27 23:33:36.429694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "00d47e4ae9b5"
down_revision = "6bdbb7f6b3e6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "entries",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("date", sa.DATE, nullable=False, default=sa.text("date('now')")),
        sa.Column("time", sa.TIME, nullable=False, default=sa.text("time('now')")),
        sa.Column("meal_desc", sa.String, nullable=False),
        sa.Column("calories", sa.Integer, nullable=False, default=sa.text("0")),
        sa.Column(
            "below_expected", sa.Boolean, nullable=False, default=sa.text("true")
        ),
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("entries")
