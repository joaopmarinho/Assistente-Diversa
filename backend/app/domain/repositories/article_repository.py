from abc import ABC, abstractmethod

from app.domain.entities.article import Article


class ArticleRepository(ABC):
    @abstractmethod
    def list_all(self) -> list[Article]:
        raise NotImplementedError
