def compact_text(text: str, limit: int = 1200) -> str:
    normalized = " ".join((text or "").split())
    return normalized[:limit]
