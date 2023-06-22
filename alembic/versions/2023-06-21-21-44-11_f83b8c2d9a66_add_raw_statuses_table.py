"""Add raw_statuses table

Revision ID: f83b8c2d9a66
Revises: 5c17476b0330
Create Date: 2023-06-21 21:44:11.015831

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f83b8c2d9a66'
down_revision = '5c17476b0330'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "raw_statuses",
        sa.Column("id", sa.BigInteger(), nullable=False, comment="Status ID"),
        sa.Column("created_at", sa.DateTime(), nullable=True, comment="Created At"),
        sa.Column("in_reply_to_id", sa.BigInteger(), nullable=True, comment="In Reply To ID"),
        sa.Column("in_reply_to_account_id", sa.BigInteger(), nullable=True, comment="In Reply To Account ID"),
        sa.Column("sensitive", sa.Boolean(), nullable=True, comment="Sensitive"),
        sa.Column("spoiler_text", sa.String(), nullable=True, comment="Spoiler Text"),
        sa.Column("visibility", sa.String(), nullable=True, comment="Visibility"),
        sa.Column("language", sa.String(), nullable=True, comment="Language"),
        sa.Column("uri", sa.String(), nullable=True, comment="URI"),
        sa.Column("url", sa.String(), nullable=True, comment="URL"),
        sa.Column("replies_count", sa.Integer(), nullable=True, comment="Replies Count"),
        sa.Column("reblogs_count", sa.Integer(), nullable=True, comment="ReBlogs Count"),
        sa.Column("favourites_count", sa.Integer(), nullable=True, comment="Favourites Count"),
        sa.Column("edited_at", sa.DateTime(), nullable=True, comment="Edited At"),
        sa.Column("content", sa.String(), nullable=True, comment="Content"),
        sa.Column("tags", postgresql.ARRAY(sa.String), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema="mastodon_service",
    )


def downgrade() -> None:
    op.drop_table("raw_statuses", schema="mastodon_service")

