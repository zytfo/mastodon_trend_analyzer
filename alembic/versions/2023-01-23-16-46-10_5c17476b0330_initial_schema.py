"""Initial schema

Revision ID: 5c17476b0330
Revises:
Create Date: 2023-03-18 10:46:10.804032

"""
# thirdparty

import sqlalchemy as sa
# project
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5c17476b0330"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS mastodon_service")

    op.create_table(
        "instances",
        sa.Column("id", sa.String(length=24), nullable=False, comment="Instance ID"),
        sa.Column("name", sa.String(length=50), nullable=True, comment="Instance Name"),
        sa.Column("added_at", sa.DateTime(), nullable=True, comment="Added At"),
        sa.Column("updated_at", sa.DateTime(), nullable=True, comment="Updated At"),
        sa.Column("uptime", sa.Integer(), nullable=True, comment="Uptime"),
        sa.Column("up", sa.Boolean(), nullable=True, comment="Is Instance Up?"),
        sa.Column("dead", sa.Boolean(), nullable=True, comment="Is Instance Dead?"),
        sa.Column("version", sa.String(), nullable=True, comment="Instance Version"),
        sa.Column("ipv6", sa.Boolean(), nullable=True, comment="Is IPv6 Enabled?"),
        sa.Column("https_score", sa.Integer(), nullable=True, comment="Https Score"),
        sa.Column("https_rank", sa.String(), nullable=True, comment="Https Rank"),
        sa.Column("obs_score", sa.Integer(), nullable=True, comment="OBS Score"),
        sa.Column("obs_rank", sa.String(), nullable=True, comment="OBS Rank"),
        sa.Column("users", sa.String(), nullable=True, comment="Number of Users"),
        sa.Column("statuses", sa.String(), nullable=True, comment="Number of Statuses"),
        sa.Column("connections", sa.String(), nullable=True, comment="Number of Statuses"),
        sa.Column("open_registrations", sa.Boolean(), nullable=True, comment="Is Open to Register?"),
        sa.Column("info", sa.JSON(), nullable=True, comment="Instance Info", ),
        sa.Column("thumbnail", sa.String(), nullable=True, comment="Thumbnail"),
        sa.Column("thumbnail_proxy", sa.String(), nullable=True, comment="Thumbnail Proxy"),
        sa.Column("active_users", sa.Integer(), nullable=True, comment="Number of Active Users"),
        sa.Column("email", sa.String(), nullable=True, comment="Owner E-mail"),
        sa.Column("admin", sa.String(), nullable=True, comment="Admin"),
        sa.PrimaryKeyConstraint("id"),
        schema="mastodon_service",
    )

    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer(), nullable=False, comment="Account ID"),
        sa.Column("username", sa.String(), nullable=True, comment="Username"),
        sa.Column("acct", sa.String(), nullable=True, comment="Acct"),
        sa.Column("display_name", sa.String(), nullable=True, comment="Display Name"),
        sa.Column("locked", sa.Boolean(), nullable=True, comment="Is Locked?"),
        sa.Column("bot", sa.Boolean(), nullable=True, comment="Is Bot?"),
        sa.Column("discoverable", sa.Boolean(), nullable=True, comment="Is Discoverable?"),
        sa.Column("group", sa.Boolean(), nullable=True, comment="Is Group?"),
        sa.Column("created_at", sa.DateTime(), nullable=True, comment="Created At"),
        sa.Column("note", sa.String(), nullable=True, comment="Note"),
        sa.Column("url", sa.String(), nullable=True, comment="URL"),
        sa.Column("avatar", sa.String(), nullable=True, comment="Avatar"),
        sa.Column("avatar_static", sa.String(), nullable=True, comment="Avatar Static"),
        sa.Column("header", sa.String(), nullable=True, comment="Header"),
        sa.Column("header_static", sa.String(), nullable=True, comment="Header Static"),
        sa.Column("followers_count", sa.Integer(), nullable=True, comment="Followers Count"),
        sa.Column("following_count", sa.Integer(), nullable=True, comment="Following Count"),
        sa.Column("statuses_count", sa.Integer(), nullable=True, comment="Statuses Count"),
        sa.Column("last_status_at", sa.DateTime(), nullable=True, comment="Last Status At"),
        schema="mastodon_service",
    )

    op.create_table(
        "statuses",
        sa.Column("id", sa.String(length=18), nullable=False, comment="Status ID"),
        sa.Column("created_at", sa.DateTime(), nullable=True, comment="Created At"),
        sa.Column("in_reply_to_id", sa.Integer(), nullable=True, comment="In Reply To ID"),
        sa.Column("in_reply_to_account_id", sa.Integer(), nullable=True, comment="In Reply To Account ID"),
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
        sa.Column('tags', postgresql.ARRAY(sa.String), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema="mastodon_service",
    )


def downgrade() -> None:
    op.drop_table("statuses", schema="mastodon_service")
    op.drop_table("accounts", schema="mastodon_service")
    op.drop_table("instances", schema="mastodon_service")
