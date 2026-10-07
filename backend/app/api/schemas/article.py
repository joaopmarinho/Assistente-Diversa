from pydantic import BaseModel, ConfigDict

from app.domain.entities.article import Article


class ArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    summary: str
    content: str
    source_url: str

    @classmethod
    def from_entity(cls, article: Article) -> "ArticleResponse":
        return cls(
            id=article.id,
            title=article.title,
            summary=article.summary,
            content=article.content,
            source_url=article.source_url,
        )
