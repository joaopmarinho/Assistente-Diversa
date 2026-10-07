from app.domain.entities.article import Article
from app.domain.repositories.article_repository import ArticleRepository


class ListArticles:
    def __init__(self, article_repository: ArticleRepository) -> None:
        self._article_repository = article_repository

    def execute(self) -> list[Article]:
        return self._article_repository.list_all()
