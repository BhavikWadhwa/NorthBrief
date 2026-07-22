from app.services.ingestion.categorizer import detect_categories
from app.services.ingestion.deduper import is_near_duplicate
from app.services.ingestion.fetcher import MAX_ENTRIES_PER_SOURCE
from app.services.ingestion.region_tagger import detect_regions


def test_detect_categories_prefers_finance() -> None:
    matches = detect_categories("Bank of Canada updates interest rates", "Markets react to inflation report")
    assert matches[0][0] in {"finance", "canada"}


def test_detect_regions_vancouver() -> None:
    matches = detect_regions("Vancouver transit strike update", "Service disruption continues", None)
    codes = [code for code, _ in matches]
    assert "ca-vancouver" in codes


def test_near_duplicate_detection() -> None:
    existing = ["Bank of Canada holds rates steady as inflation cools"]
    assert is_near_duplicate("Bank of Canada holds rates steady as inflation cools", existing)


def test_feed_entry_limit_is_bounded() -> None:
    assert 1 <= MAX_ENTRIES_PER_SOURCE <= 100
