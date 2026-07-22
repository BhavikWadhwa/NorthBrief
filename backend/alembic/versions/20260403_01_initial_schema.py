"""initial schema

Revision ID: 20260403_01
Revises:
Create Date: 2026-04-03
"""

from alembic import op
import sqlalchemy as sa

revision = "20260403_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("display_name", sa.String(length=100), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "user_preferences",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), unique=True),
        sa.Column("country", sa.String(length=100), nullable=False, server_default="Canada"),
        sa.Column("province", sa.String(length=100)),
        sa.Column("city", sa.String(length=100)),
        sa.Column("category_codes", sa.JSON(), nullable=False),
        sa.Column("local_global_weight", sa.Float(), nullable=False, server_default="0.7"),
        sa.Column("finance_weight", sa.Float(), nullable=False, server_default="0.4"),
        sa.Column("skip_personalization", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "news_sources",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False, unique=True),
        sa.Column("source_type", sa.String(length=30), nullable=False),
        sa.Column("feed_url", sa.String(length=1000), nullable=False),
        sa.Column("site_url", sa.String(length=1000)),
        sa.Column("default_region_code", sa.String(length=50)),
        sa.Column("default_category_code", sa.String(length=50)),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "categories",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("code", sa.String(length=50), nullable=False, unique=True),
        sa.Column("label", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "regions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("code", sa.String(length=100), nullable=False, unique=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("region_type", sa.String(length=30), nullable=False),
        sa.Column("parent_code", sa.String(length=100)),
        sa.Column("country", sa.String(length=100), nullable=False, server_default="Canada"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "ingestion_runs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("triggered_by", sa.String(length=50), nullable=False),
        sa.Column("fetched_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("inserted_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("deduped_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("logs", sa.JSON(), nullable=False),
    )

    op.create_table(
        "raw_articles",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("source_id", sa.String(length=36), sa.ForeignKey("news_sources.id")),
        sa.Column("ingestion_run_id", sa.String(length=36), sa.ForeignKey("ingestion_runs.id")),
        sa.Column("title", sa.String(length=600), nullable=False),
        sa.Column("canonical_url", sa.String(length=1500), nullable=False, unique=True),
        sa.Column("source_name", sa.String(length=255), nullable=False),
        sa.Column("source_domain", sa.String(length=255)),
        sa.Column("published_at", sa.DateTime(timezone=True)),
        sa.Column("snippet", sa.Text()),
        sa.Column("image_url", sa.String(length=1500)),
        sa.Column("raw_payload", sa.JSON(), nullable=False),
        sa.Column("region_candidates", sa.JSON(), nullable=False),
        sa.Column("category_candidates", sa.JSON(), nullable=False),
        sa.Column("processing_status", sa.String(length=30), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "processed_articles",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("raw_article_id", sa.String(length=36), sa.ForeignKey("raw_articles.id"), unique=True),
        sa.Column("headline", sa.String(length=600), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("why_this_matters", sa.Text(), nullable=False),
        sa.Column("key_impact", sa.Text()),
        sa.Column("region_confidence", sa.Float(), nullable=False, server_default="0"),
        sa.Column("category_confidence", sa.Float(), nullable=False, server_default="0"),
        sa.Column("summary_status", sa.String(length=30), nullable=False),
        sa.Column("quality_flags", sa.JSON(), nullable=False),
        sa.Column("rank_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "article_category_links",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("processed_article_id", sa.String(length=36), sa.ForeignKey("processed_articles.id", ondelete="CASCADE")),
        sa.Column("category_id", sa.String(length=36), sa.ForeignKey("categories.id", ondelete="CASCADE")),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0"),
        sa.Column("is_primary", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.UniqueConstraint("processed_article_id", "category_id", name="uq_article_category_link"),
    )

    op.create_table(
        "article_region_links",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("processed_article_id", sa.String(length=36), sa.ForeignKey("processed_articles.id", ondelete="CASCADE")),
        sa.Column("region_id", sa.String(length=36), sa.ForeignKey("regions.id", ondelete="CASCADE")),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0"),
        sa.Column("is_primary", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.UniqueConstraint("processed_article_id", "region_id", name="uq_article_region_link"),
    )

    op.create_table(
        "summarization_runs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("raw_article_id", sa.String(length=36), sa.ForeignKey("raw_articles.id")),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("prompt_version", sa.String(length=50), nullable=False),
        sa.Column("output_payload", sa.JSON(), nullable=False),
        sa.Column("error_message", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "bookmarks",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("processed_article_id", sa.String(length=36), sa.ForeignKey("processed_articles.id", ondelete="CASCADE")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "processed_article_id", name="uq_user_bookmark"),
    )

    op.create_table(
        "hidden_articles",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("processed_article_id", sa.String(length=36), sa.ForeignKey("processed_articles.id", ondelete="CASCADE")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "processed_article_id", name="uq_user_hidden"),
    )


def downgrade() -> None:
    for table in [
        "hidden_articles",
        "bookmarks",
        "summarization_runs",
        "article_region_links",
        "article_category_links",
        "processed_articles",
        "raw_articles",
        "ingestion_runs",
        "regions",
        "categories",
        "news_sources",
        "user_preferences",
        "users",
    ]:
        op.drop_table(table)

