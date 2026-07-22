import re
from difflib import SequenceMatcher


def normalize_title(title: str) -> str:
    text = re.sub(r"[^a-z0-9\s]", "", title.lower())
    return re.sub(r"\s+", " ", text).strip()


def is_near_duplicate(current_title: str, existing_titles: list[str], threshold: float = 0.9) -> bool:
    normalized_current = normalize_title(current_title)
    for existing in existing_titles:
        ratio = SequenceMatcher(None, normalized_current, normalize_title(existing)).ratio()
        if ratio >= threshold:
            return True
    return False

