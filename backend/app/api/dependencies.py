from functools import lru_cache

from app.domain.repositories.article_repository import ArticleRepository
from app.infrastructure.repositories.static_article_repository import StaticArticleRepository


@lru_cache
def get_article_repository() -> ArticleRepository:
    return StaticArticleRepository()
