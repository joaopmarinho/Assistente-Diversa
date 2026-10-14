from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BACKEND_DIR.parent / ".env", BACKEND_DIR / ".env"),
        extra="ignore",
        populate_by_name=True,
    )

    # Nomes alternativos mantidos por compatibilidade com o notebook.
    groq_key: str = Field("", validation_alias=AliasChoices("GROQ_KEY", "GROQ_API_KEY", "GROQ_API_TOKEN"))
    groq_model: str = "openai/gpt-oss-20b"
    groq_url: str = "https://api.groq.com/openai/v1/chat/completions"

    artigos_csv: Path = BACKEND_DIR / "app" / "data" / "artigos.csv"
    conteudo_json: Path = BACKEND_DIR / "app" / "data" / "conteudo.json"

    cors_origins: str = "http://localhost:5173"
    rate_limit_por_minuto: int = 20
    max_chars_pergunta: int = 1000
    max_mensagens_historico: int = 8

    # Embeddings locais (ONNX): sem chave e sem cota; se falharem, a busca segue só lexical.
    embeddings_habilitados: bool = True
    embedding_modelo: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    embedding_cache_dir: str | None = None
    embeddings_npz: Path = BACKEND_DIR / "app" / "data" / "embeddings.npz"
    # Similaridade de cosseno mínima para um trecho contar como relevante sem nenhuma palavra em comum.
    limiar_semantico: float = 0.40
    # Acima disto, uma pergunta sem palavra-chave ainda é aceita como sendo sobre educação inclusiva.
    limiar_escopo_semantico: float = 0.50


@lru_cache
def get_settings() -> Settings:
    return Settings()
