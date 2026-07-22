from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session, joinedload
from typing import Literal

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import ArticleCategoryLink, ArticleRegionLink, ProcessedArticle, RawArticle, User, UserPreference
from app.schemas import FeedItem, FeedResponse
from app.services.ranking import compute_rank_score

router = APIRouter(prefix="/feed", tags=["feed"])


def to_feed_item(article: ProcessedArticle) -> FeedItem:
    primary_category = next((link.category.label for link in article.category_links if link.is_primary), "Canada")
    primary_region = next((link.region.name for link in article.region_links if link.is_primary), None)
    raw = article.raw_article
    return FeedItem(
        id=article.id,
        headline=article.headline,
        summary=article.summary,
        why_this_matters=article.why_this_matters,
        key_impact=article.key_impact,
        category=primary_category,
        region=primary_region,
        source_name=raw.source_name,
        source_domain=raw.source_domain,
        published_at=raw.published_at,
        canonical_url=raw.canonical_url,
        image_url=raw.image_url,
        rank_score=article.rank_score,
    )


@router.get("", response_model=FeedResponse)
def get_feed(
    tab: Literal["for-you", "local", "canada", "world", "finance", "trending"] = Query(default="for-you"),
    limit: int = Query(default=40, ge=1, le=120),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> FeedResponse:
    pref = db.query(UserPreference).filter(UserPreference.user_id == current_user.id).first()
    query = (
        db.query(ProcessedArticle)
        .join(ProcessedArticle.raw_article)
        .filter(RawArticle.duplicate_of_raw_article_id.is_(None))
        .options(
            joinedload(ProcessedArticle.raw_article),
            joinedload(ProcessedArticle.category_links).joinedload(ArticleCategoryLink.category),
            joinedload(ProcessedArticle.region_links).joinedload(ArticleRegionLink.region),
        )
        .order_by(desc(ProcessedArticle.created_at))
        .limit(limit * 2)
    )
    candidates = query.all()

    if tab != "for-you":
        expected = tab.lower()
        candidates = [
            article
            for article in candidates
            if any(link.category.code == expected for link in article.category_links)
            or any(link.region.code == expected for link in article.region_links)
        ]

    for item in candidates:
        item.rank_score = compute_rank_score(item, pref)

    ranked = sorted(candidates, key=lambda article: article.rank_score, reverse=True)[:limit]
    return FeedResponse(items=[to_feed_item(item) for item in ranked], total=len(ranked))
