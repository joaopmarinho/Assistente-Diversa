from dataclasses import dataclass, field
from typing import Literal

from app.core.config import get_settings
from app.services import scope, sugestoes
from app.services.demo import resposta_demo
from app.services.llm import chamar_groq
from app.services.persona import normalizar_perfil, system_prompt
from app.services.rag import ArtigoEncontrado, IndiceArtigos
from app.services.text import limpar_fontes_da_resposta, remover_paragrafos_duplicados

Origem = Literal["fora_escopo", "llm", "demo", "garantida"]

_FINAL_VALIDO = ".!?…:)”’"
_PALAVRAS_FRACAS = {"com", "para", "por", "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas", "e", "ou", "que", "transtorno"}

_COMPLEMENTO = {
    "Professor": (
        " Para completar, o mais importante é transformar esse conceito em prática: observar as barreiras que impedem "
        "a participação do estudante, planejar estratégias acessíveis, articular o AEE quando necessário e acompanhar "
        "se os apoios estão realmente favorecendo aprendizagem, autonomia e participação."
    ),
    "Família": (
        " Em resumo, a família pode buscar diálogo com a escola, entender quais apoios estão sendo oferecidos e acompanhar "
        "se a criança ou adolescente está participando das atividades com segurança, respeito e oportunidades reais de aprendizagem."
    ),
    "Gestor": (
        " Na prática, a gestão deve organizar processos, responsabilidades, recursos de acessibilidade, articulação com o AEE "
        "e acompanhamento pedagógico para que a inclusão aconteça de forma planejada e contínua."
    ),
}


@dataclass
class Resposta:
    texto: str
    origem: Origem
    artigos: list[ArtigoEncontrado] = field(default_factory=list)


def _parece_incompleta(texto: str) -> bool:
    texto = str(texto or "").strip()
    if not texto:
        return True
    if scope.resposta_fora_escopo(texto) or scope.resposta_base_insuficiente(texto):
        return False
    if len(texto) < 220 or texto[-1] not in _FINAL_VALIDO:
        return True
    return texto.lower().split()[-1].strip(".,;:") in _PALAVRAS_FRACAS


def _finalizar_incompleta(texto: str, perfil: str) -> str:
    texto = remover_paragrafos_duplicados(texto)
    if scope.resposta_fora_escopo(texto) or scope.resposta_base_insuficiente(texto):
        return texto
    if texto and texto[-1] not in _FINAL_VALIDO:
        texto += "."
    return (texto + _COMPLEMENTO[perfil]).strip()


def _limpar(texto: str) -> str:
    return remover_paragrafos_duplicados(limpar_fontes_da_resposta(texto))


def _montar_instrucao(pergunta: str, artigos: list[ArtigoEncontrado]) -> str:
    contexto = "\n\n".join(f"Artigo: {a.titulo}\nTrecho: {a.trecho[:1800]}" for a in artigos) or (
        "Nenhum trecho relevante foi encontrado na base atual."
    )
    return (
        "Use os TÍTULOS E TRECHOS DO PORTAL DIVERSA abaixo para responder. "
        "Não invente informações. Primeiro verifique se os artigos recuperados têm relação direta ou parcial com a pergunta. "
        "Se houver relação direta ou parcial, responda com base no que os trechos permitem e informe com cuidado quando faltar um passo a passo específico. "
        "Só diga que a base atual é insuficiente quando nenhum título ou trecho tiver relação útil com a pergunta. "
        "Quando a base for insuficiente, escreva apenas uma mensagem curta, sem repetir a mesma frase e sem introdução, desenvolvimento ou conclusão. "
        "Não escreva fonte, título de artigo, URL, link, referência, leia mais ou seção de fontes no corpo da resposta. "
        "As fontes serão exibidas apenas no painel lateral Fontes consultadas. "
        "Quando houver informação suficiente ou parcialmente suficiente, a resposta precisa estar completa, com começo, desenvolvimento e conclusão. "
        "Não pare no meio de uma frase. Finalize sempre a última ideia antes de encerrar.\n\n"
        f"TÍTULOS E TRECHOS DO PORTAL DIVERSA:\n{contexto}\n\n"
        f"PERGUNTA DO USUÁRIO: {pergunta}"
    )


def responder(
    pergunta: str,
    perfil: str,
    historico: list[dict[str, str]],
    indice: IndiceArtigos,
) -> Resposta:
    pergunta = (pergunta or "").strip()
    perfil = normalizar_perfil(perfil)
    tem_chave = bool(get_settings().groq_key.strip())

    if not scope.pergunta_dentro_escopo(pergunta):
        return Resposta(scope.gerar_resposta_fora_escopo(pergunta, perfil), "fora_escopo")

    artigos = sugestoes.reforcar_artigos(pergunta, indice.buscar(pergunta, top_k=3), indice)

    mensagens = [
        {"role": "system", "content": system_prompt(perfil)},
        *historico[-get_settings().max_mensagens_historico:],
        {"role": "user", "content": _montar_instrucao(pergunta, artigos)},
    ]

    origem: Origem = "llm"
    texto = chamar_groq(mensagens, perfil)
    if not texto:
        origem = "demo"
        texto = resposta_demo(pergunta, artigos, perfil)
    texto = _limpar(texto)

    if scope.resposta_base_insuficiente(texto) and artigos and tem_chave:
        revisao = chamar_groq(
            [
                *mensagens,
                {"role": "assistant", "content": texto},
                {
                    "role": "user",
                    "content": (
                        "Você respondeu que a base é insuficiente, mas existem artigos recuperados no contexto. "
                        "Reavalie os títulos e trechos. Se eles tiverem relação útil com a pergunta, responda usando apenas essas informações, "
                        "sem citar fontes no corpo da resposta. Só mantenha base insuficiente se realmente não houver relação útil."
                    ),
                },
            ],
            perfil,
            timeout_segundos=18,
            max_tokens=650,
        )
        revisao = _limpar(revisao)
        if revisao and not scope.resposta_base_insuficiente(revisao):
            texto = revisao

    garantida = sugestoes.resposta_garantida(pergunta, perfil)
    if garantida and (scope.resposta_base_insuficiente(texto) or len(texto) < 120):
        return Resposta(garantida, "garantida", artigos)

    if scope.resposta_base_insuficiente(texto):
        return Resposta(texto, origem, artigos)

    if _parece_incompleta(texto) and tem_chave:
        complemento = limpar_fontes_da_resposta(
            chamar_groq(
                [
                    *mensagens,
                    {"role": "assistant", "content": texto},
                    {
                        "role": "user",
                        "content": "A resposta anterior ficou incompleta ou curta demais. Complete a explicação em português brasileiro, sem repetir o início e sem citar fontes no corpo da resposta.",
                    },
                ],
                perfil,
                timeout_segundos=18,
                max_tokens=450,
            )
        )
        if complemento:
            texto = remover_paragrafos_duplicados(f"{texto.rstrip()}\n\n{complemento.strip()}")

    texto = remover_paragrafos_duplicados(texto)
    if _parece_incompleta(texto):
        texto = _finalizar_incompleta(texto, perfil)

    return Resposta(texto, origem, artigos)
