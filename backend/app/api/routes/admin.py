from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_admin_user
from app.db.session import get_db
from app.models import ProcessedArticle, RawArticle, SummarizationRun, User
from app.schemas import AdminIngestionResponse
from app.services.ingestion.pipeline import run_ingestion
from app.services.summarization.service import enforce_summary_guardrails, get_provider

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/ingestion/run", response_model=AdminIngestionResponse)
def trigger_ingestion(_: User = Depends(get_admin_user), db: Session = Depends(get_db)) -> AdminIngestionResponse:
    run = run_ingestion(db, triggered_by="admin")
    return AdminIngestionResponse(
        run_id=run.id,
        status=run.status,
        fetched_count=run.fetched_count,
        inserted_count=run.inserted_count,
        deduped_count=run.deduped_count,
        error_count=run.error_count,
    )


@router.get("/articles")
def list_ingested_articles(_: User = Depends(get_admin_user), db: Session = Depends(get_db), limit: int = 120) -> dict:
    rows = (
        db.query(ProcessedArticle)
        .join(RawArticle, RawArticle.id == ProcessedArticle.raw_article_id)
        .order_by(ProcessedArticle.created_at.desc())
        .limit(limit)
        .all()
    )
    return {
        "items": [
            {
                "processed_article_id": row.id,
                "raw_article_id": row.raw_article_id,
                "headline": row.headline,
                "summary_status": row.summary_status,
                "quality_flags": row.quality_flags,
                "category_confidence": row.category_confidence,
                "region_confidence": row.region_confidence,
            }
            for row in rows
        ]
    }


@router.post("/summaries/retry/{raw_article_id}")
def retry_summary(raw_article_id: str, _: User = Depends(get_admin_user), db: Session = Depends(get_db)) -> dict:
    raw = db.query(RawArticle).filter(RawArticle.id == raw_article_id).first()
    if not raw:
        raise HTTPException(status_code=404, detail="Raw article not found")

    processed = db.query(ProcessedArticle).filter(ProcessedArticle.raw_article_id == raw.id).first()
    if not processed:
        raise HTTPException(status_code=404, detail="Processed article not found")

    provider = get_provider()
    output = enforce_summary_guardrails(provider.summarize(raw.title, raw.snippet, raw.source_name))
    processed.summary = output.summary
    processed.why_this_matters = output.why_this_matters
    processed.key_impact = output.key_impact
    processed.quality_flags = output.quality_flags or []
    processed.summary_status = "ready" if not processed.quality_flags else "review"

    db.add(
        SummarizationRun(
            raw_article_id=raw.id,
            provider=provider.provider_name,
            status=processed.summary_status,
            output_payload={
                "summary": processed.summary,
                "why_this_matters": processed.why_this_matters,
                "key_impact": processed.key_impact,
                "quality_flags": processed.quality_flags,
            },
        )
    )
    db.commit()
    return {"ok": True, "summary_status": processed.summary_status}

