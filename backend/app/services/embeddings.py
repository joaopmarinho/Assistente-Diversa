import logging
from collections import OrderedDict
from typing import Protocol

import numpy as np

from app.core.config import get_settings

logger = logging.getLogger(__name__)

_CACHE_CONSULTAS = 256


class Embedder(Protocol):
    modelo: str

    def embed(self, textos: list[str]) -> np.ndarray:
        """Matriz (n, d) com vetores normalizados."""

    def embed_consulta(self, texto: str) -> np.ndarray:
        """Vetor normalizado (d,)."""


def _normalizar_linhas(vetores: np.ndarray) -> np.ndarray:
    normas = np.linalg.norm(vetores, axis=1, keepdims=True)
    return vetores / np.where(normas == 0, 1, normas)


class FastEmbedEmbedder:
    def __init__(self, modelo: str, cache_dir: str | None):
        from fastembed import TextEmbedding  # import tardio: carregar o ONNX custa

        self.modelo = modelo
        self._modelo = TextEmbedding(modelo, cache_dir=cache_dir)
        self._consultas: OrderedDict[str, np.ndarray] = OrderedDict()

    def embed(self, textos: list[str]) -> np.ndarray:
        return _normalizar_linhas(np.array(list(self._modelo.embed(textos)), dtype=np.float32))

    def embed_consulta(self, texto: str) -> np.ndarray:
        # As perguntas sugeridas se repetem muito; o cache evita reprocessá-las.
        if texto in self._consultas:
            self._consultas.move_to_end(texto)
            return self._consultas[texto]
        vetor = self.embed([texto])[0]
        self._consultas[texto] = vetor
        if len(self._consultas) > _CACHE_CONSULTAS:
            self._consultas.popitem(last=False)
        return vetor


def criar_embedder() -> Embedder | None:
    """Devolve None quando desabilitado ou quando o modelo não pode ser carregado."""
    settings = get_settings()
    if not settings.embeddings_habilitados:
        return None
    try:
        return FastEmbedEmbedder(settings.embedding_modelo, settings.embedding_cache_dir)
    except Exception:
        logger.exception("Embeddings indisponíveis; a busca usará só o índice lexical.")
        return None
