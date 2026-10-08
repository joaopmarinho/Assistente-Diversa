from typing import Literal

from pydantic import BaseModel, Field

# Limites fixos aqui; o limite de caracteres da pergunta configurável é validado na rota.
LIMITE_MENSAGEM_HISTORICO = 4000
LIMITE_MENSAGENS = 20


class Mensagem(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(max_length=LIMITE_MENSAGEM_HISTORICO)


class ChatRequest(BaseModel):
    pergunta: str = Field(min_length=1)
    perfil: str = "Professor"
    historico: list[Mensagem] = Field(default_factory=list, max_length=LIMITE_MENSAGENS)


class Fonte(BaseModel):
    titulo: str
    url: str
    score: float


class ChatResponse(BaseModel):
    resposta: str
    perfil: str
    fontes: list[Fonte]
    origem: Literal["fora_escopo", "llm", "demo", "garantida"]


class Perfil(BaseModel):
    nome: str
    saudacao: str


class PerfisResponse(BaseModel):
    perfis: list[Perfil]
    perguntas_sugeridas: list[str]
