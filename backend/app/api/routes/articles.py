from fastapi import APIRouter, Depends

from app.api.dependencies import get_article_repository
from app.api.schemas.article import ArticleResponse
from app.application.use_cases.list_articles import ListArticles
from app.domain.repositories.article_repository import ArticleRepository

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=list[ArticleResponse])
def list_articles(
    article_repository: ArticleRepository = Depends(get_article_repository),
) -> list[ArticleResponse]:
    articles = ListArticles(article_repository).execute()
    return [ArticleResponse.from_entity(article) for article in articles]
