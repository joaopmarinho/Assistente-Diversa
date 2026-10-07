from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.api.schemas.article import ArticleResponse
from app.domain.entities.profile import UserProfile


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str = Field(min_length=1, max_length=2000)
    profile: UserProfile = UserProfile.PROFESSOR

    @field_validator("message")
    @classmethod
    def strip_message(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("A mensagem não pode estar vazia.")
        return normalized


class ChatResponse(BaseModel):
    answer: str
    profile: UserProfile
    sources: list[ArticleResponse]
