REGION_KEYWORDS = {
    "ca": ["canada", "federal", "ottawa"],
    "ca-bc": ["british columbia", "bc", "victoria"],
    "ca-on": ["ontario", "on", "queen's park"],
    "ca-qc": ["quebec", "qc", "quebec city"],
    "ca-ab": ["alberta", "ab", "edmonton", "calgary"],
    "ca-vancouver": ["vancouver", "burnaby", "surrey", "richmond"],
    "ca-toronto": ["toronto", "mississauga", "scarborough"],
    "ca-montreal": ["montreal", "laval", "longueuil"],
    "global": ["united states", "europe", "asia", "global", "world"],
}


def detect_regions(title: str, snippet: str | None, default_region: str | None = None) -> list[tuple[str, float]]:
    text = f"{title} {snippet or ''}".lower()
    matches: list[tuple[str, float]] = []
    for region_code, keywords in REGION_KEYWORDS.items():
        hit_count = sum(1 for keyword in keywords if keyword in text)
        if hit_count:
            confidence = min(0.4 + hit_count * 0.2, 0.95)
            matches.append((region_code, confidence))
    if default_region and all(code != default_region for code, _ in matches):
        matches.append((default_region, 0.55))
    if not matches:
        matches.append(("ca", 0.25))
    matches.sort(key=lambda item: item[1], reverse=True)
    return matches

