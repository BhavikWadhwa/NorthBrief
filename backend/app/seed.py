import secrets

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import hash_password
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import (
    ArticleCategoryLink,
    ArticleRegionLink,
    Category,
    ProcessedArticle,
    RawArticle,
    Region,
    User,
    UserPreference,
)
from app.services.bootstrap import ensure_static_data


def seed(db: Session) -> None:
    ensure_static_data(db)
    settings = get_settings()
    admin_password = settings.admin_password
    if not admin_password and settings.environment == "development":
        admin_password = "password123"

    admin = db.query(User).filter(User.email == settings.admin_email).first()
    if admin_password and not admin:
        admin = User(
            email=settings.admin_email,
            display_name="NorthBrief Admin",
            password_hash=hash_password(admin_password),
            is_admin=True,
        )
        db.add(admin)
        db.flush()
        db.add(UserPreference(user_id=admin.id, province="bc", city="vancouver", category_codes=["local", "canada"]))
    elif admin_password and admin:
        admin.password_hash = hash_password(admin_password)
        admin.is_admin = True
    elif admin:
        admin.password_hash = hash_password(secrets.token_urlsafe(32))
        admin.is_admin = False

    existing = db.query(RawArticle).first()
    if existing:
        db.commit()
        return

    samples = [
        {
            "title": "BC announces updated housing acceleration targets for municipalities",
            "url": "https://example.ca/news/bc-housing-targets",
            "source": "CBC News",
            "domain": "cbc.ca",
            "snippet": "British Columbia unveiled revised housing targets, with Vancouver and Surrey among cities expected to expand multi-unit approvals.",
            "category_code": "local",
            "region_code": "ca-bc",
        },
        {
            "title": "Bank of Canada holds benchmark rate steady amid mixed inflation signals",
            "url": "https://example.ca/news/boc-rate-hold",
            "source": "The Globe and Mail",
            "domain": "theglobeandmail.com",
            "snippet": "The central bank maintained its policy rate and said future decisions will depend on shelter and services inflation data.",
            "category_code": "finance",
            "region_code": "ca",
        },
        {
            "title": "UN agencies launch expanded aid corridor for conflict-affected civilians",
            "url": "https://example.org/world/aid-corridor",
            "source": "Reuters",
            "domain": "reuters.com",
            "snippet": "International organizations announced a coordinated aid plan to improve food and medicine access in heavily affected districts.",
            "category_code": "humanitarian",
            "region_code": "global",
        },
    ]

    for item in samples:
        raw = RawArticle(
            title=item["title"],
            canonical_url=item["url"],
            source_name=item["source"],
            source_domain=item["domain"],
            snippet=item["snippet"],
            processing_status="processed",
            category_candidates=[item["category_code"]],
            region_candidates=[item["region_code"]],
        )
        db.add(raw)
        db.flush()

        processed = ProcessedArticle(
            raw_article_id=raw.id,
            headline=item["title"],
            summary=item["snippet"],
            why_this_matters="This update may shape policy, budgets, or day-to-day planning for affected communities.",
            key_impact="Follow official updates for implementation timelines.",
            summary_status="ready",
            category_confidence=0.8,
            region_confidence=0.75,
            rank_score=0.66,
        )
        db.add(processed)
        db.flush()

        category = db.query(Category).filter(Category.code == item["category_code"]).first()
        region = db.query(Region).filter(Region.code == item["region_code"]).first()
        if category:
            db.add(
                ArticleCategoryLink(
                    processed_article_id=processed.id, category_id=category.id, confidence=0.8, is_primary=True
                )
            )
        if region:
            db.add(
                ArticleRegionLink(
                    processed_article_id=processed.id, region_id=region.id, confidence=0.75, is_primary=True
                )
            )

    db.commit()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        seed(session)
    finally:
        session.close()
