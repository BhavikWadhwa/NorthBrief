from datetime import UTC, datetime

from app.models import ProcessedArticle, UserPreference


def freshness_score(article: ProcessedArticle) -> float:
    published = article.raw_article.published_at
    if not published:
        return 0.2
    age_hours = max((datetime.now(UTC) - published).total_seconds() / 3600, 0.0)
    return max(0.0, 1.0 - age_hours / 96.0)


def preference_score(article: ProcessedArticle, preference: UserPreference | None) -> float:
    if not preference or preference.skip_personalization:
        return 0.45
    category_bonus = 0.0
    region_bonus = 0.0
    category_codes = {link.category.code for link in article.category_links}
    region_codes = {link.region.code for link in article.region_links}
    if set(preference.category_codes).intersection(category_codes):
        category_bonus += 0.35

    preferred_region_codes = {"ca"}
    if preference.province:
        preferred_region_codes.add(f"ca-{preference.province.lower()}")
    if preference.city:
        preferred_region_codes.add(f"ca-{preference.city.lower()}")

    if preferred_region_codes.intersection(region_codes):
        region_bonus += 0.45 * preference.local_global_weight
    elif "global" in region_codes:
        region_bonus += 0.2 * (1.0 - preference.local_global_weight)

    finance_bonus = 0.2 * preference.finance_weight if "finance" in category_codes else 0.0
    return min(1.0, 0.2 + category_bonus + region_bonus + finance_bonus)


def compute_rank_score(article: ProcessedArticle, preference: UserPreference | None) -> float:
    diversity_discount = 0.05 if article.raw_article.source_name.lower() in {"reuters", "associated press"} else 0.0
    source_priority = article.source_priority if article.source_priority is not None else 0.5
    return round(
        (freshness_score(article) * 0.35)
        + (preference_score(article, preference) * 0.45)
        + (source_priority * 0.2)
        - diversity_discount,
        4,
    )
