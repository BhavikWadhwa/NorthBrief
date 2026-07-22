from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_admin_user
from app.db.session import get_db
from app.models import NewsSource, User
from app.schemas import SourceCreate, SourceResponse, SourceUpdate
from app.services.ingestion.pipeline import sync_sources

router = APIRouter(prefix="/sources", tags=["sources"])


def serialize_source(row: NewsSource) -> SourceResponse:
    return SourceResponse(
        id=row.id,
        name=row.name,
        feed_url=row.feed_url,
        site_url=row.site_url,
        source_type=row.source_type,
        default_region_code=row.default_region_code,
        default_category_code=row.default_category_code,
        priority=row.priority,
        is_active=row.is_active,
        last_fetched_at=row.last_fetched_at,
        last_status=row.last_status,
        failure_count=row.failure_count,
    )


@router.get("", response_model=list[SourceResponse])
def list_sources(_: User = Depends(get_admin_user), db: Session = Depends(get_db)) -> list[SourceResponse]:
    sync_sources(db)
    rows = db.query(NewsSource).order_by(NewsSource.name.asc()).all()
    return [serialize_source(row) for row in rows]


@router.post("", response_model=SourceResponse, status_code=201)
def create_source(payload: SourceCreate, _: User = Depends(get_admin_user), db: Session = Depends(get_db)) -> SourceResponse:
    exists = db.query(NewsSource).filter(NewsSource.name == payload.name.strip()).first()
    if exists:
        raise HTTPException(status_code=409, detail="Source name already exists")
    url_exists = db.query(NewsSource).filter(NewsSource.feed_url == str(payload.feed_url)).first()
    if url_exists:
        raise HTTPException(status_code=409, detail="Feed URL already exists")
    source = NewsSource(
        name=payload.name.strip(),
        source_type=payload.source_type,
        feed_url=str(payload.feed_url),
        site_url=str(payload.site_url) if payload.site_url else None,
        default_region_code=payload.default_region_code,
        default_category_code=payload.default_category_code,
        priority=payload.priority,
        is_active=payload.is_active,
        last_status="created",
        last_fetched_at=datetime.now(UTC),
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return serialize_source(source)


@router.patch("/{source_id}", response_model=SourceResponse)
def update_source(
    source_id: str, payload: SourceUpdate, _: User = Depends(get_admin_user), db: Session = Depends(get_db)
) -> SourceResponse:
    source = db.query(NewsSource).filter(NewsSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    if payload.is_active is not None:
        source.is_active = payload.is_active
    if payload.default_region_code is not None:
        source.default_region_code = payload.default_region_code
    if payload.default_category_code is not None:
        source.default_category_code = payload.default_category_code
    if payload.priority is not None:
        source.priority = payload.priority
    db.commit()
    db.refresh(source)
    return serialize_source(source)
