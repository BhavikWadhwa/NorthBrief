from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import Bookmark, ProcessedArticle, User
from app.schemas import BookmarkCreate, FeedItem, FeedResponse

router = APIRouter(prefix="/bookmarks", tags=["bookmarks"])


def serialize(article: ProcessedArticle) -> FeedItem:
    primary_category = next((link.category.label for link in article.category_links if link.is_primary), "Canada")
    primary_region = next((link.region.name for link in article.region_links if link.is_primary), None)
    return FeedItem(
        id=article.id,
        headline=article.headline,
        summary=article.summary,
        why_this_matters=article.why_this_matters,
        key_impact=article.key_impact,
        category=primary_category,
        region=primary_region,
        source_name=article.raw_article.source_name,
        source_domain=article.raw_article.source_domain,
        published_at=article.raw_article.published_at,
        canonical_url=article.raw_article.canonical_url,
        image_url=article.raw_article.image_url,
        rank_score=article.rank_score,
    )


@router.get("", response_model=FeedResponse)
def list_bookmarks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> FeedResponse:
    rows = (
        db.query(ProcessedArticle)
        .join(Bookmark, Bookmark.processed_article_id == ProcessedArticle.id)
        .filter(Bookmark.user_id == current_user.id)
        .all()
    )
    return FeedResponse(items=[serialize(item) for item in rows], total=len(rows))


@router.post("", status_code=201)
def create_bookmark(
    payload: BookmarkCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    article = db.query(ProcessedArticle).filter(ProcessedArticle.id == payload.processed_article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    existing = (
        db.query(Bookmark)
        .filter(
            Bookmark.user_id == current_user.id,
            Bookmark.processed_article_id == payload.processed_article_id,
        )
        .first()
    )
    if not existing:
        db.add(Bookmark(user_id=current_user.id, processed_article_id=payload.processed_article_id))
        db.commit()
    return {"ok": True}


@router.delete("/{processed_article_id}", status_code=204)
def remove_bookmark(
    processed_article_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> None:
    bookmark = (
        db.query(Bookmark)
        .filter(Bookmark.user_id == current_user.id, Bookmark.processed_article_id == processed_article_id)
        .first()
    )
    if bookmark:
        db.delete(bookmark)
        db.commit()

