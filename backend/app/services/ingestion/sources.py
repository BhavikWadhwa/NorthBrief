import json
from pathlib import Path

from pydantic import BaseModel, HttpUrl


class SourceConfig(BaseModel):
    name: str
    source_type: str = "rss"
    feed_url: HttpUrl
    site_url: HttpUrl | None = None
    default_region_code: str | None = None
    default_category_code: str | None = None
    priority: float = 0.5
    is_active: bool = True


def load_source_registry() -> list[SourceConfig]:
    config_path = Path(__file__).resolve().parents[3] / "config" / "sources.json"
    data = json.loads(config_path.read_text(encoding="utf-8"))
    return [SourceConfig(**item) for item in data["sources"]]
