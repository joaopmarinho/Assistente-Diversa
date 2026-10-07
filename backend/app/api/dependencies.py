from functools import lru_cache
import os

from app.domain.repositories.article_repository import ArticleRepository
from app.infrastructure.repositories.postgres_article_repository import (
    PostgresArticleRepository,
)
from app.infrastructure.repositories.static_article_repository import StaticArticleRepository


@lru_cache
def get_article_repository() -> ArticleRepository:
    if os.getenv("DATABASE_HOST"):
        return PostgresArticleRepository()
    return StaticArticleRepository()
