import re

from app.services.persona import conteudo, normalizar_perfil
from app.services.rag import ArtigoEncontrado, IndiceArtigos
from app.services.text import normalizar


def chave_pergunta(texto: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", normalizar(texto))).strip()


def eh_pergunta_sugerida(pergunta: str) -> bool:
    chave = chave_pergunta(pergunta)
    return any(item in chave for item in conteudo()["perguntas_sugeridas_garantidas"])


def _chave_resposta(pergunta: str) -> str:
    chave = chave_pergunta(pergunta)
    if chave in conteudo()["respostas_garantidas"]:
        return chave
    if "atendimento educacional especializado" in chave or f" {chave}".endswith(" aee") or " aee " in f" {chave} ":
        return "o que e atendimento educacional especializado"
    if any(t in chave for t in ("tea", "autismo", "autista")):
        return "como incluir um aluno com tea em sala de aula"
    if "educacao inclusiva" in chave or "inclusao" in chave:
        return "o que e educacao inclusiva"
    return ""


def resposta_garantida(pergunta: str, perfil: str) -> str:
    chave = _chave_resposta(pergunta)
    if not chave:
        return ""
    respostas = conteudo()["respostas_garantidas"].get(chave, {})
    return respostas.get(normalizar_perfil(perfil)) or respostas.get("Professor", "")


def resposta_por_chave(chave: str, perfil: str) -> str:
    respostas = conteudo()["respostas_garantidas"][chave]
    return respostas.get(normalizar_perfil(perfil)) or respostas["Professor"]


def reforcar_artigos(
    pergunta: str, artigos: list[ArtigoEncontrado], indice: IndiceArtigos
) -> list[ArtigoEncontrado]:
    """Para as perguntas sugeridas, completa a busca com termos-chave até ter 3 artigos."""
    artigos = list(artigos)
    if len(artigos) >= 3 or not eh_pergunta_sugerida(pergunta):
        return artigos

    vistos = {(a.url, a.titulo) for a in artigos}
    for consulta in conteudo()["consultas_reforco"].get(_chave_resposta(pergunta), []):
        for extra in indice.buscar(consulta, top_k=3, score_minimo=0.005):
            if (extra.url, extra.titulo) not in vistos:
                vistos.add((extra.url, extra.titulo))
                artigos.append(extra)
            if len(artigos) >= 3:
                return artigos
    return artigos
