import json
from functools import lru_cache
from typing import Any

from app.core.config import get_settings

PERFIL_PADRAO = "Professor"
PERFIS = ("Professor", "Família", "Gestor")

_ALIASES = {
    "professor": "Professor",
    "familia": "Família",
    "família": "Família",
    "gestor": "Gestor",
}


@lru_cache
def conteudo() -> dict[str, Any]:
    """Prompts, respostas fixas e listas de palavras extraídos do notebook."""
    with get_settings().conteudo_json.open(encoding="utf-8") as arquivo:
        return json.load(arquivo)


def normalizar_perfil(perfil: str | None) -> str:
    return _ALIASES.get(str(perfil or PERFIL_PADRAO).strip().lower(), PERFIL_PADRAO)


def system_prompt(perfil: str) -> str:
    perfil = normalizar_perfil(perfil)
    return f"{conteudo()['system_prompts'][perfil]}\n\n{conteudo()['instrucoes_perfil'][perfil]}"


def parametros_geracao(perfil: str) -> dict[str, Any]:
    return conteudo()["parametros_perfil"][normalizar_perfil(perfil)]
