"""source scaling and clustering

Revision ID: 20260404_02
Revises: 20260403_01
Create Date: 2026-04-04
"""

from alembic import op
import sqlalchemy as sa

revision = "20260404_02"
down_revision = "20260403_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("news_sources", sa.Column("priority", sa.Float(), nullable=False, server_default="0.5"))
    op.add_column("news_sources", sa.Column("last_fetched_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("news_sources", sa.Column("last_status", sa.String(length=30), nullable=True))
    op.add_column("news_sources", sa.Column("last_error", sa.Text(), nullable=True))
    op.add_column("news_sources", sa.Column("success_count", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("news_sources", sa.Column("failure_count", sa.Integer(), nullable=False, server_default="0"))

    op.add_column("raw_articles", sa.Column("duplicate_of_raw_article_id", sa.String(length=36), nullable=True))
    op.add_column("raw_articles", sa.Column("cluster_key", sa.String(length=100), nullable=True))
    op.create_index("ix_raw_articles_cluster_key", "raw_articles", ["cluster_key"])
    op.create_foreign_key(
        "fk_raw_articles_duplicate_of",
        "raw_articles",
        "raw_articles",
        ["duplicate_of_raw_article_id"],
        ["id"],
    )

    op.add_column("processed_articles", sa.Column("source_priority", sa.Float(), nullable=False, server_default="0.5"))

    op.create_table(
        "source_ingestion_runs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("ingestion_run_id", sa.String(length=36), sa.ForeignKey("ingestion_runs.id", ondelete="CASCADE")),
        sa.Column("source_id", sa.String(length=36), sa.ForeignKey("news_sources.id", ondelete="CASCADE")),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("fetched_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("inserted_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("deduped_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("source_ingestion_runs")
    op.drop_column("processed_articles", "source_priority")

    op.drop_constraint("fk_raw_articles_duplicate_of", "raw_articles", type_="foreignkey")
    op.drop_index("ix_raw_articles_cluster_key", table_name="raw_articles")
    op.drop_column("raw_articles", "cluster_key")
    op.drop_column("raw_articles", "duplicate_of_raw_article_id")

    op.drop_column("news_sources", "failure_count")
    op.drop_column("news_sources", "success_count")
    op.drop_column("news_sources", "last_error")
    op.drop_column("news_sources", "last_status")
    op.drop_column("news_sources", "last_fetched_at")
    op.drop_column("news_sources", "priority")

