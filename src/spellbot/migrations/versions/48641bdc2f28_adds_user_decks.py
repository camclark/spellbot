"""Adds user decks

Revision ID: 48641bdc2f28
Revises: 42f55401ef2b
Create Date: 2022-01-09 20:01:17.109085

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "48641bdc2f28"
down_revision = "42f55401ef2b"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "decks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(now() at time zone 'utc')"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("(now() at time zone 'utc')"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("link", sa.String(length=255), nullable=True),
        sa.Column("user_xid", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(["user_xid"], ["users.xid"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", "user_xid"),
    )
    op.create_index(op.f("ix_decks_user_xid"), "decks", ["user_xid"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_decks_user_xid"), table_name="decks")
    op.drop_table("decks")
