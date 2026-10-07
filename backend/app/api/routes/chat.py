from fastapi import APIRouter, Depends

from app.api.dependencies import get_article_repository
from app.api.schemas.article import ArticleResponse
from app.api.schemas.chat import ChatRequest, ChatResponse
from app.application.use_cases.send_message import SendMessage
from app.domain.repositories.article_repository import ArticleRepository

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def send_message(
    request: ChatRequest,
    article_repository: ArticleRepository = Depends(get_article_repository),
) -> ChatResponse:
    answer, sources = SendMessage(article_repository).execute(
        request.message,
        request.profile,
    )
    return ChatResponse(
        answer=answer,
        profile=request.profile,
        sources=[ArticleResponse.from_entity(article) for article in sources],
    )
