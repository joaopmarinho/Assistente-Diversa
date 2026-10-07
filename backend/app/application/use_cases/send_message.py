import re
import unicodedata

from app.domain.entities.article import Article
from app.domain.entities.profile import UserProfile
from app.domain.repositories.article_repository import ArticleRepository


class SendMessage:
    _profile_openings = {
        UserProfile.PROFESSOR: "Para apoiar seu trabalho pedagógico",
        UserProfile.FAMILIA: "Para apoiar a criança e a família",
        UserProfile.GESTOR: "Como encaminhamento para a gestão escolar",
    }

    def __init__(self, article_repository: ArticleRepository) -> None:
        self._article_repository = article_repository

    def execute(self, question: str, profile: UserProfile) -> tuple[str, list[Article]]:
        articles = self._find_relevant_articles(question)
        if not articles:
            return (
                "Não encontrei informações suficientes na base demonstrativa para responder. "
                "Tente perguntar sobre educação inclusiva, acessibilidade ou atendimento educacional especializado.",
                [],
            )

        answer = " ".join(
            (
                f"{self._profile_openings[profile]},",
                articles[0].summary,
                "Esta resposta usa somente o conteúdo mockado; confirme orientações "
                "específicas com a equipe responsável.",
            )
        )
        return answer, articles

    def _find_relevant_articles(self, question: str) -> list[Article]:
        question_terms = self._terms(question)
        scored_articles = []
        for article in self._article_repository.list_all():
            article_terms = self._terms(
                " ".join((article.title, article.summary, *article.keywords))
            )
            score = len(question_terms & article_terms)
            if score:
                scored_articles.append((score, article))
        scored_articles.sort(key=lambda result: (-result[0], result[1].title))
        return [article for _, article in scored_articles[:3]]

    @staticmethod
    def _terms(text: str) -> set[str]:
        normalized = unicodedata.normalize("NFKD", text.casefold())
        without_accents = "".join(
            character for character in normalized if not unicodedata.combining(character)
        )
        return {
            term
            for term in re.findall(r"[a-z0-9]+", without_accents)
            if len(term) > 2
        }
