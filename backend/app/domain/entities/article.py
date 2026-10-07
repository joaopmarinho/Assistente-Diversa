from dataclasses import dataclass


@dataclass(frozen=True)
class Article:
    id: str
    title: str
    summary: str
    content: str
    source_url: str
    keywords: tuple[str, ...]
