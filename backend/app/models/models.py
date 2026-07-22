import enum
from datetime import datetime
from uuid import uuid4

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def uuid_str() -> str:
    return str(uuid4())


class SourceType(str, enum.Enum):
    rss = "rss"
    api = "api"
    government = "government"


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    preference: Mapped["UserPreference"] = relationship(back_populates="user", uselist=False)
    bookmarks: Mapped[list["Bookmark"]] = relationship(back_populates="user")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    country: Mapped[str] = mapped_column(String(100), default="Canada")
    province: Mapped[str | None] = mapped_column(String(100), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    category_codes: Mapped[list[str]] = mapped_column(JSON, default=list)
    local_global_weight: Mapped[float] = mapped_column(Float, default=0.7)
    finance_weight: Mapped[float] = mapped_column(Float, default=0.4)
    skip_personalization: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="preference")


class NewsSource(Base):
    __tablename__ = "news_sources"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    source_type: Mapped[str] = mapped_column(String(30), default=SourceType.rss.value)
    feed_url: Mapped[str] = mapped_column(String(1000))
    site_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    default_region_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    default_category_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    priority: Mapped[float] = mapped_column(Float, default=0.5)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_fetched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    success_count: Mapped[int] = mapped_column(Integer, default=0)
    failure_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    raw_articles: Mapped[list["RawArticle"]] = relationship(back_populates="news_source")
    ingestion_statuses: Mapped[list["SourceIngestionRun"]] = relationship(back_populates="news_source")


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    status: Mapped[str] = mapped_column(String(30), default="running")
    triggered_by: Mapped[str] = mapped_column(String(50), default="system")
    fetched_count: Mapped[int] = mapped_column(Integer, default=0)
    inserted_count: Mapped[int] = mapped_column(Integer, default=0)
    deduped_count: Mapped[int] = mapped_column(Integer, default=0)
    error_count: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    logs: Mapped[dict] = mapped_column(JSON, default=dict)


class RawArticle(Base):
    __tablename__ = "raw_articles"
    __table_args__ = (UniqueConstraint("canonical_url", name="uq_raw_articles_canonical_url"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    source_id: Mapped[str | None] = mapped_column(ForeignKey("news_sources.id"), nullable=True)
    ingestion_run_id: Mapped[str | None] = mapped_column(ForeignKey("ingestion_runs.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(600))
    canonical_url: Mapped[str] = mapped_column(String(1500))
    source_name: Mapped[str] = mapped_column(String(255))
    source_domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    duplicate_of_raw_article_id: Mapped[str | None] = mapped_column(ForeignKey("raw_articles.id"), nullable=True)
    cluster_key: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    snippet: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(1500), nullable=True)
    raw_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    region_candidates: Mapped[list[str]] = mapped_column(JSON, default=list)
    category_candidates: Mapped[list[str]] = mapped_column(JSON, default=list)
    processing_status: Mapped[str] = mapped_column(String(30), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    news_source: Mapped["NewsSource"] = relationship(back_populates="raw_articles")
    processed_article: Mapped["ProcessedArticle"] = relationship(back_populates="raw_article", uselist=False)


class ProcessedArticle(Base):
    __tablename__ = "processed_articles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    raw_article_id: Mapped[str] = mapped_column(ForeignKey("raw_articles.id"), unique=True)
    headline: Mapped[str] = mapped_column(String(600))
    summary: Mapped[str] = mapped_column(Text)
    why_this_matters: Mapped[str] = mapped_column(Text)
    key_impact: Mapped[str | None] = mapped_column(Text, nullable=True)
    region_confidence: Mapped[float] = mapped_column(Float, default=0.0)
    category_confidence: Mapped[float] = mapped_column(Float, default=0.0)
    summary_status: Mapped[str] = mapped_column(String(30), default="ready")
    quality_flags: Mapped[list[str]] = mapped_column(JSON, default=list)
    source_priority: Mapped[float] = mapped_column(Float, default=0.5)
    rank_score: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    raw_article: Mapped["RawArticle"] = relationship(back_populates="processed_article")
    category_links: Mapped[list["ArticleCategoryLink"]] = relationship(back_populates="processed_article")
    region_links: Mapped[list["ArticleRegionLink"]] = relationship(back_populates="processed_article")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    code: Mapped[str] = mapped_column(String(50), unique=True)
    label: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    article_links: Mapped[list["ArticleCategoryLink"]] = relationship(back_populates="category")


class Region(Base):
    __tablename__ = "regions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    code: Mapped[str] = mapped_column(String(100), unique=True)
    name: Mapped[str] = mapped_column(String(150))
    region_type: Mapped[str] = mapped_column(String(30))
    parent_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100), default="Canada")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    article_links: Mapped[list["ArticleRegionLink"]] = relationship(back_populates="region")


class ArticleCategoryLink(Base):
    __tablename__ = "article_category_links"
    __table_args__ = (
        UniqueConstraint("processed_article_id", "category_id", name="uq_article_category_link"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    processed_article_id: Mapped[str] = mapped_column(ForeignKey("processed_articles.id", ondelete="CASCADE"))
    category_id: Mapped[str] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)

    processed_article: Mapped["ProcessedArticle"] = relationship(back_populates="category_links")
    category: Mapped["Category"] = relationship(back_populates="article_links")


class ArticleRegionLink(Base):
    __tablename__ = "article_region_links"
    __table_args__ = (
        UniqueConstraint("processed_article_id", "region_id", name="uq_article_region_link"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    processed_article_id: Mapped[str] = mapped_column(ForeignKey("processed_articles.id", ondelete="CASCADE"))
    region_id: Mapped[str] = mapped_column(ForeignKey("regions.id", ondelete="CASCADE"))
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)

    processed_article: Mapped["ProcessedArticle"] = relationship(back_populates="region_links")
    region: Mapped["Region"] = relationship(back_populates="article_links")


class SummarizationRun(Base):
    __tablename__ = "summarization_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    raw_article_id: Mapped[str] = mapped_column(ForeignKey("raw_articles.id"))
    provider: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(30), default="started")
    prompt_version: Mapped[str] = mapped_column(String(50), default="v1")
    output_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class SourceIngestionRun(Base):
    __tablename__ = "source_ingestion_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    ingestion_run_id: Mapped[str] = mapped_column(ForeignKey("ingestion_runs.id", ondelete="CASCADE"))
    source_id: Mapped[str] = mapped_column(ForeignKey("news_sources.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(30), default="running")
    fetched_count: Mapped[int] = mapped_column(Integer, default=0)
    inserted_count: Mapped[int] = mapped_column(Integer, default=0)
    deduped_count: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    attempt_count: Mapped[int] = mapped_column(Integer, default=1)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    news_source: Mapped["NewsSource"] = relationship(back_populates="ingestion_statuses")


class Bookmark(Base):
    __tablename__ = "bookmarks"
    __table_args__ = (UniqueConstraint("user_id", "processed_article_id", name="uq_user_bookmark"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    processed_article_id: Mapped[str] = mapped_column(ForeignKey("processed_articles.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="bookmarks")


class HiddenArticle(Base):
    __tablename__ = "hidden_articles"
    __table_args__ = (UniqueConstraint("user_id", "processed_article_id", name="uq_user_hidden"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    processed_article_id: Mapped[str] = mapped_column(ForeignKey("processed_articles.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
