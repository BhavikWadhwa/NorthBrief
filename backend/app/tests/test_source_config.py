from app.services.ingestion.sources import load_source_registry


def test_source_registry_contains_priority_and_activation() -> None:
    sources = load_source_registry()
    assert len(sources) >= 28
    assert all(0 <= source.priority <= 1 for source in sources)
    assert all(isinstance(source.is_active, bool) for source in sources)
    assert len({str(source.feed_url) for source in sources}) == len(sources)
