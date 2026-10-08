import logging

import httpx

from app.core.config import get_settings
from app.services.persona import parametros_geracao

logger = logging.getLogger(__name__)

_PARAMS_BASE = {"max_tokens": 600, "temperature": 0.3, "top_p": 0.9}


def chamar_groq(
    mensagens: list[dict[str, str]],
    perfil: str,
    timeout_segundos: float = 22,
    max_tokens: int | None = None,
) -> str:
    """Devolve o texto gerado ou "" quando a chave falta ou a API falha (o chamador faz o fallback)."""
    settings = get_settings()
    chave = settings.groq_key.strip()
    if not chave:
        return ""

    payload = {
        "model": settings.groq_model,
        **_PARAMS_BASE,
        **parametros_geracao(perfil),
        "messages": mensagens,
    }
    if max_tokens:
        payload["max_tokens"] = max_tokens

    try:
        resposta = httpx.post(
            settings.groq_url,
            headers={"Authorization": f"Bearer {chave}"},
            json=payload,
            timeout=timeout_segundos,
        )
        if resposta.status_code != 200:
            logger.warning("Groq respondeu HTTP %s", resposta.status_code)
            return ""
        return str(resposta.json()["choices"][0]["message"]["content"] or "").strip()
    except (httpx.HTTPError, KeyError, IndexError, ValueError) as erro:
        logger.warning("Falha ao chamar a Groq: %s", type(erro).__name__)
        return ""
