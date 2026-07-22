import logging
from datetime import UTC, datetime, timedelta
from threading import Thread

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import IngestionRun
from app.services.bootstrap import ensure_static_data
from app.services.ingestion.pipeline import run_ingestion

settings = get_settings()
logger = logging.getLogger(__name__)
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix=settings.api_v1_prefix)


def run_startup_ingestion() -> None:
    db = SessionLocal()
    try:
        latest_run = db.query(IngestionRun).order_by(IngestionRun.started_at.desc()).first()
        cutoff = datetime.now(UTC) - timedelta(minutes=settings.ingestion_startup_min_interval_minutes)
        if latest_run and latest_run.status == "completed" and latest_run.started_at:
            started_at = latest_run.started_at
            if started_at.tzinfo is None:
                started_at = started_at.replace(tzinfo=UTC)
            if started_at >= cutoff:
                logger.info("Skipping startup ingestion because a recent run already exists")
                return
        result = run_ingestion(db, triggered_by="deployment")
        logger.info(
            "Startup ingestion completed: fetched=%s inserted=%s deduped=%s errors=%s",
            result.fetched_count,
            result.inserted_count,
            result.deduped_count,
            result.error_count,
        )
    except Exception:  # noqa: BLE001
        logger.exception("Startup ingestion failed")
    finally:
        db.close()


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        ensure_static_data(db)
    finally:
        db.close()
    if settings.ingest_on_startup:
        Thread(target=run_startup_ingestion, name="startup-ingestion", daemon=True).start()
