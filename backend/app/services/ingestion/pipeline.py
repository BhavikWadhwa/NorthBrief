import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models import (
    ArticleCategoryLink,
    ArticleRegionLink,
    Category,
    IngestionRun,
    NewsSource,
    ProcessedArticle,
    RawArticle,
    Region,
    SourceIngestionRun,
    SummarizationRun,
)
from app.services.ingestion.categorizer import detect_categories
from app.services.ingestion.deduper import is_near_duplicate
from app.services.ingestion.fetcher import fetch_rss_entries
from app.services.ingestion.region_tagger import detect_regions
from app.services.ingestion.sources import load_source_registry
from app.services.summarization.service import enforce_summary_guardrails, get_provider


def to_json_safe(data: dict) -> dict:
    safe: dict = {}
    for key, value in data.items():
        if isinstance(value, datetime):
            safe[key] = value.isoformat()
        else:
            safe[key] = value
    return safe


def sync_sources(db: Session) -> None:
    configured = load_source_registry()
    existing = {src.name: src for src in db.query(NewsSource).all()}
    for source in configured:
        current = existing.get(source.name)
        if current:
            current.feed_url = str(source.feed_url)
            current.source_type = source.source_type
            current.site_url = str(source.site_url) if source.site_url else None
            current.default_region_code = source.default_region_code
            current.default_category_code = source.default_category_code
        else:
            db.add(
                NewsSource(
                    name=source.name,
                    source_type=source.source_type,
                    feed_url=str(source.feed_url),
                    site_url=str(source.site_url) if source.site_url else None,
                    default_region_code=source.default_region_code,
                    default_category_code=source.default_category_code,
                    priority=source.priority,
                    is_active=source.is_active,
                    last_status="configured",
                )
            )
    db.commit()


def cluster_key_for(title: str) -> str:
    normalized = " ".join(title.lower().split())
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:20]


def fetch_with_retry(source: NewsSource, attempts: int = 2) -> tuple[list[dict], str | None, int]:
    last_error: str | None = None
    for attempt in range(1, attempts + 1):
        try:
            return fetch_rss_entries(source), None, attempt
        except Exception as exc:  # noqa: BLE001
            last_error = str(exc)
    return [], last_error, attempts


def run_ingestion(db: Session, triggered_by: str = "system") -> IngestionRun:
    sync_sources(db)
    run = IngestionRun(status="running", triggered_by=triggered_by)
    db.add(run)
    db.commit()
    db.refresh(run)

    provider = get_provider()
    existing_titles = [item[0] for item in db.query(RawArticle.title).all()]
    category_by_code = {item.code: item for item in db.query(Category).all()}
    region_by_code = {item.code: item for item in db.query(Region).all()}

    sources = db.query(NewsSource).filter(NewsSource.is_active.is_(True)).all()
    fetched_by_source: dict[str, tuple[list[dict], str | None, int]] = {}
    with ThreadPoolExecutor(max_workers=min(10, max(len(sources), 1))) as executor:
        future_map = {executor.submit(fetch_with_retry, source): source for source in sources}
        for future in as_completed(future_map):
            source = future_map[future]
            try:
                fetched_by_source[source.id] = future.result()
            except Exception as exc:  # noqa: BLE001
                fetched_by_source[source.id] = ([], str(exc), 2)

    for source in sources:
        entries, fetch_error, attempt_count = fetched_by_source.get(source.id, ([], "unknown fetch error", 1))
        source_run = SourceIngestionRun(
            ingestion_run_id=run.id,
            source_id=source.id,
            status="running",
            attempt_count=attempt_count,
            fetched_count=len(entries),
        )
        db.add(source_run)
        db.flush()

        run.fetched_count += len(entries)
        if fetch_error:
            source.last_status = "failed"
            source.last_error = fetch_error
            source.last_fetched_at = datetime.now(UTC)
            source.failure_count += 1
            source_run.status = "failed"
            source_run.error_message = fetch_error
            source_run.completed_at = datetime.now(UTC)
            run.error_count += 1
            run.logs = {**(run.logs or {}), source.name: fetch_error}
            db.commit()
            continue

        try:
            for entry in entries:
                current_cluster = cluster_key_for(entry["title"])
                existing_primary = (
                    db.query(RawArticle)
                    .join(ProcessedArticle, ProcessedArticle.raw_article_id == RawArticle.id, isouter=True)
                    .filter(
                        RawArticle.duplicate_of_raw_article_id.is_(None),
                        RawArticle.cluster_key == current_cluster,
                    )
                    .first()
                )
                duplicate_by_url = db.query(RawArticle).filter(RawArticle.canonical_url == entry["canonical_url"]).first()
                near_duplicate = is_near_duplicate(entry["title"], existing_titles)

                if duplicate_by_url:
                    run.deduped_count += 1
                    source_run.deduped_count += 1
                    continue

                if existing_primary or near_duplicate:
                    duplicate_target = existing_primary
                    if not duplicate_target:
                        run.deduped_count += 1
                        source_run.deduped_count += 1
                        continue
                    raw = RawArticle(
                        source_id=source.id,
                        ingestion_run_id=run.id,
                        title=entry["title"],
                        canonical_url=entry["canonical_url"],
                        source_name=entry["source_name"],
                        source_domain=entry["source_domain"],
                        published_at=entry["published_at"],
                        snippet=entry["snippet"],
                        image_url=entry["image_url"],
                        category_candidates=[source.default_category_code] if source.default_category_code else [],
                        region_candidates=[source.default_region_code] if source.default_region_code else [],
                        processing_status="duplicate_clustered",
                        raw_payload=to_json_safe(entry),
                        duplicate_of_raw_article_id=duplicate_target.id,
                        cluster_key=current_cluster,
                    )
                    db.add(raw)
                    run.deduped_count += 1
                    source_run.deduped_count += 1
                    continue

                categories = detect_categories(entry["title"], entry["snippet"])
                regions = detect_regions(entry["title"], entry["snippet"], source.default_region_code)
                if source.default_category_code:
                    categories = [(source.default_category_code, 0.9)] + [
                        item for item in categories if item[0] != source.default_category_code
                    ]
                if source.default_region_code:
                    regions = [(source.default_region_code, 0.9)] + [
                        item for item in regions if item[0] != source.default_region_code
                    ]

                raw = RawArticle(
                    source_id=source.id,
                    ingestion_run_id=run.id,
                    title=entry["title"],
                    canonical_url=entry["canonical_url"],
                    source_name=entry["source_name"],
                    source_domain=entry["source_domain"],
                    published_at=entry["published_at"],
                    snippet=entry["snippet"],
                    image_url=entry["image_url"],
                    category_candidates=[code for code, _ in categories[:3]],
                    region_candidates=[code for code, _ in regions[:3]],
                    processing_status="processing",
                    raw_payload=to_json_safe(entry),
                    cluster_key=current_cluster,
                )
                db.add(raw)
                db.flush()

                summary_run = SummarizationRun(raw_article_id=raw.id, provider=provider.provider_name, status="started")
                db.add(summary_run)

                output = enforce_summary_guardrails(provider.summarize(raw.title, raw.snippet, raw.source_name))
                status = "ready" if not output.quality_flags else "review"

                processed = ProcessedArticle(
                    raw_article_id=raw.id,
                    headline=raw.title,
                    summary=output.summary,
                    why_this_matters=output.why_this_matters,
                    key_impact=output.key_impact,
                    quality_flags=output.quality_flags or [],
                    summary_status=status,
                    category_confidence=categories[0][1],
                    region_confidence=regions[0][1],
                    source_priority=source.priority,
                )
                db.add(processed)
                db.flush()

                for idx, (code, confidence) in enumerate(categories[:2]):
                    category = category_by_code.get(code)
                    if category:
                        db.add(
                            ArticleCategoryLink(
                                processed_article_id=processed.id,
                                category_id=category.id,
                                confidence=confidence,
                                is_primary=idx == 0,
                            )
                        )

                for idx, (code, confidence) in enumerate(regions[:2]):
                    region = region_by_code.get(code)
                    if region:
                        db.add(
                            ArticleRegionLink(
                                processed_article_id=processed.id,
                                region_id=region.id,
                                confidence=confidence,
                                is_primary=idx == 0,
                            )
                        )

                raw.processing_status = "processed"
                summary_run.status = status
                summary_run.output_payload = {
                    "summary": output.summary,
                    "why_this_matters": output.why_this_matters,
                    "key_impact": output.key_impact,
                    "quality_flags": output.quality_flags or [],
                }
                run.inserted_count += 1
                source_run.inserted_count += 1
                existing_titles.append(raw.title)

            source.last_status = "success"
            source.last_error = None
            source.last_fetched_at = datetime.now(UTC)
            source.success_count += 1
            source_run.status = "success"
            source_run.completed_at = datetime.now(UTC)
            db.commit()
        except Exception as exc:  # noqa: BLE001
            db.rollback()
            run = db.query(IngestionRun).filter(IngestionRun.id == run.id).first()
            source = db.query(NewsSource).filter(NewsSource.id == source.id).first()
            failed_source_run = db.query(SourceIngestionRun).filter(SourceIngestionRun.id == source_run.id).first()
            if run and source:
                source.last_status = "failed"
                source.last_error = str(exc)
                source.last_fetched_at = datetime.now(UTC)
                source.failure_count += 1
                if failed_source_run:
                    failed_source_run.status = "failed"
                    failed_source_run.error_message = str(exc)
                    failed_source_run.completed_at = datetime.now(UTC)
                else:
                    db.add(
                        SourceIngestionRun(
                            ingestion_run_id=run.id,
                            source_id=source.id,
                            status="failed",
                            fetched_count=0,
                            inserted_count=0,
                            deduped_count=0,
                            error_message=str(exc),
                            attempt_count=attempt_count,
                            completed_at=datetime.now(UTC),
                        )
                    )
                run.error_count += 1
                run.logs = {**(run.logs or {}), source.name: str(exc)}
                db.commit()

    run.status = "completed"
    run.completed_at = datetime.now(UTC)
    db.commit()
    db.refresh(run)
    return run
