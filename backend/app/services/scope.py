from app.services.persona import conteudo, normalizar_perfil
from app.services.text import limpar_texto, normalizar

_TEMAS_FORA_ESCOPO = {
    "esporte": (
        "futebol", "jogo", "placar", "brasil", "copa", "campeonato", "gol", "time",
        "selecao", "partida", "libertadores", "brasileirao", "vitoria", "derrota",
    ),
    "clima": ("clima", "tempo", "chuva", "temperatura", "previsao", "frio", "calor"),
    "politica": (
        "presidente", "eleicao", "partido", "governo", "prefeito", "governador",
        "senador", "deputado", "politica", "votar",
    ),
    "entretenimento": (
        "filme", "serie", "novela", "musica", "cantor", "atriz", "ator",
        "celebridade", "show", "anime", "jogo online", "games",
    ),
    "tecnologia_geral": (
        "celular", "iphone", "android", "notebook", "computador", "windows", "programacao",
        "codigo", "python", "java", "sql", "erro no sistema",
    ),
    "saude_geral": (
        "remedio", "medicamento", "dor", "sintoma", "tratamento", "doenca",
        "consulta medica", "exame", "hospital",
    ),
}

_MARCADORES_FORA_ESCOPO = (
    "minha especialidade e educacao inclusiva",
    "fora do foco do assistente",
    "fora do escopo do assistente",
    "fora do escopo do prototipo",
    "nao faz parte do escopo",
    "foco deste assistente e educacao inclusiva",
    "foco do assistente e educacao inclusiva",
    "assistente foi desenvolvido para responder sobre educacao inclusiva",
    "prototipo foi pensado para educacao inclusiva",
    "vou redirecionar para o tema central",
    "nao vou responder resultado de jogo",
    "nao vou responder sobre entretenimento geral",
    "nao vou responder sobre politica partidaria",
    "nao vou orientar sobre saude",
    "nao vou orientar sobre tratamento",
)

_MARCADORES_BASE_INSUFICIENTE = (
    "base atual nao contem",
    "base atual nao tem",
    "base atual nao possui",
    "base atual ainda nao possui",
    "base atual e insuficiente",
    "base atual nao tem informacoes suficientes",
    "nao tem informacoes suficientes",
    "nao possui trechos suficientes",
    "nao contem informacoes especificas",
    "nao contem informacoes suficientes",
    "informacoes especificas sobre estrategias",
    "nenhum trecho relevante foi encontrado",
    "informacao nao esteja nos trechos",
)


def pergunta_dentro_escopo(pergunta: str) -> bool:
    texto = limpar_texto(pergunta).lower()
    return any(palavra in texto for palavra in conteudo()["palavras_escopo"])


def identificar_tema_fora_escopo(pergunta: str) -> str:
    texto = normalizar(pergunta)
    for tema, palavras in _TEMAS_FORA_ESCOPO.items():
        if any(palavra in texto for palavra in palavras):
            return tema
    return "geral"


def gerar_resposta_fora_escopo(pergunta: str, perfil: str) -> str:
    perfil = normalizar_perfil(perfil)
    por_perfil = conteudo()["respostas_fora_escopo"][perfil]
    opcoes = por_perfil.get(identificar_tema_fora_escopo(pergunta)) or por_perfil["geral"]
    # Escolha determinística: a mesma pergunta recebe sempre a mesma variação.
    indice = sum(ord(ch) for ch in f"{normalizar(pergunta)}|{perfil}") % len(opcoes)
    return opcoes[indice]


def resposta_fora_escopo(texto: str) -> bool:
    texto = normalizar(texto)
    return any(m in texto for m in _MARCADORES_FORA_ESCOPO)


def resposta_base_insuficiente(texto: str) -> bool:
    texto = normalizar(texto)
    return any(m in texto for m in _MARCADORES_BASE_INSUFICIENTE)
