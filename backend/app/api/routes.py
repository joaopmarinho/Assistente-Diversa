from fastapi import APIRouter, HTTPException, Request

from app.core.config import get_settings
from app.repositories.interaction_log import registrar_interacao
from app.schemas.chat import ChatRequest, ChatResponse, Fonte, Perfil, PerfisResponse
from app.services.answer import responder
from app.services.persona import PERFIS, normalizar_perfil

router = APIRouter(prefix="/api")

PERGUNTAS_SUGERIDAS = [
    "O que é educação inclusiva?",
    "O que é Atendimento Educacional Especializado?",
    "Como incluir um aluno com TEA em sala de aula?",
]


@router.get("/health")
def health(request: Request) -> dict[str, object]:
    return {"status": "ok", "artigos": len(request.app.state.indice)}


@router.get("/profiles", response_model=PerfisResponse)
def perfis() -> PerfisResponse:
    return PerfisResponse(
        perfis=[
            Perfil(
                nome=nome,
                saudacao=f"Olá! Sou o Assistente Diversa em modo {nome}. Como posso ajudar com educação inclusiva?",
            )
            for nome in PERFIS
        ],
        perguntas_sugeridas=PERGUNTAS_SUGERIDAS,
    )


# Rota síncrona: o FastAPI a executa em thread, então a chamada bloqueante à Groq não trava o servidor.
@router.post("/chat", response_model=ChatResponse)
def chat(corpo: ChatRequest, request: Request) -> ChatResponse:
    pergunta = corpo.pergunta.strip()
    if not pergunta:
        raise HTTPException(status_code=422, detail="A pergunta não pode ficar vazia.")
    if len(pergunta) > get_settings().max_chars_pergunta:
        raise HTTPException(status_code=422, detail="Pergunta longa demais.")

    perfil = normalizar_perfil(corpo.perfil)
    resposta = responder(
        pergunta,
        perfil,
        [m.model_dump() for m in corpo.historico],
        request.app.state.indice,
    )
    fontes = [Fonte(titulo=a.titulo, url=a.url, score=a.score) for a in resposta.artigos]
    registrar_interacao(perfil, pergunta, resposta.origem, [f.model_dump() for f in fontes])

    return ChatResponse(resposta=resposta.texto, perfil=perfil, fontes=fontes, origem=resposta.origem)
