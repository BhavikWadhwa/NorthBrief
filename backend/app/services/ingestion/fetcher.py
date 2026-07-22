from datetime import UTC, datetime
from urllib.parse import urlparse

import feedparser

from app.services.ingestion.sources import SourceConfig


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    clean_path = parsed.path.rstrip("/")
    return f"{parsed.scheme}://{parsed.netloc}{clean_path}"


def extract_image_url(entry: dict) -> str | None:
    media_content = entry.get("media_content")
    if media_content and isinstance(media_content, list):
        candidate = media_content[0].get("url")
        if candidate:
            return candidate

    media_thumbnail = entry.get("media_thumbnail")
    if media_thumbnail and isinstance(media_thumbnail, list):
        candidate = media_thumbnail[0].get("url")
        if candidate:
            return candidate

    links = entry.get("links")
    if links and isinstance(links, list):
        for link in links:
            if "image" in (link.get("type") or "") and link.get("href"):
                return link["href"]

    image = entry.get("image")
    if image and isinstance(image, dict) and image.get("href"):
        return image["href"]

    return None


def fetch_rss_entries(source: SourceConfig) -> list[dict]:
    parsed = feedparser.parse(str(source.feed_url))
    items: list[dict] = []
    for entry in parsed.entries:
        published_struct = entry.get("published_parsed")
        published = datetime(*published_struct[:6], tzinfo=UTC) if published_struct else None
        items.append(
            {
                "title": entry.get("title", "").strip(),
                "canonical_url": normalize_url(entry.get("link", "")),
                "snippet": (entry.get("summary") or "")[:1500] or None,
                "published_at": published,
                "image_url": extract_image_url(entry),
                "source_name": source.name,
                "source_domain": urlparse(str(source.site_url or source.feed_url)).netloc,
            }
        )
    return [item for item in items if item["title"] and item["canonical_url"]]
