import json
from pathlib import Path

from app.domain.entities.article import Article
from app.domain.repositories.article_repository import ArticleRepository


class StaticArticleRepository(ArticleRepository):
    def __init__(self, data_path: Path | None = None) -> None:
        self._data_path = data_path or Path(__file__).parents[2] / "data" / "articles.json"

    def list_all(self) -> list[Article]:
        records = json.loads(self._data_path.read_text(encoding="utf-8"))
        return [
            Article(
                id=record["id"],
                title=record["title"],
                summary=record["summary"],
                content=record["content"],
                source_url=record["source_url"],
                keywords=tuple(record["keywords"]),
            )
            for record in records
        ]
