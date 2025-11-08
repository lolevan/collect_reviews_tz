from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20241115_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("text", sa.String(length=1024), nullable=False, unique=True),
        sa.Column(
            "sentiment",
            sa.Enum(
                "positive",
                "negative",
                "neutral",
                name="sentiment_enum",
                native_enum=False,
            ),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("reviews")
    op.execute("DROP TYPE IF EXISTS sentiment_enum")
