CATEGORY_KEYWORDS = {
    "ai": ["ai", "artificial intelligence", "openai", "machine learning", "llm", "model"],
    "finance": ["stocks", "bank", "inflation", "market", "interest rates", "tsx", "earnings"],
    "global_finance": ["imf", "g20", "global market", "opec", "federal reserve"],
    "politics": ["election", "parliament", "policy", "minister", "legislation", "senate"],
    "war_conflict": ["war", "conflict", "ceasefire", "military", "invasion"],
    "humanitarian": ["aid", "relief", "refugee", "food insecurity", "displacement"],
    "wholesome": ["community", "volunteer", "school win", "fundraiser", "rescued"],
    "trending": ["viral", "trend", "social media", "popular"],
    "world": ["united nations", "international", "global"],
    "canada": ["canada", "ottawa", "federal"],
    "local": ["city", "municipal", "transit", "neighbourhood", "province"],
}


def detect_categories(title: str, snippet: str | None) -> list[tuple[str, float]]:
    text = f"{title} {snippet or ''}".lower()
    matches: list[tuple[str, float]] = []
    for code, keywords in CATEGORY_KEYWORDS.items():
        hit_count = sum(1 for keyword in keywords if keyword in text)
        if hit_count:
            confidence = min(0.45 + hit_count * 0.18, 0.95)
            matches.append((code, confidence))
    if not matches:
        matches.append(("canada", 0.35))
    matches.sort(key=lambda item: item[1], reverse=True)
    return matches
