import pytest

DENTRO = [
    "O que é tecnologia assistiva?",
    "Como trabalhar com alunos com TDAH em sala?",
    "Quais são os direitos do aluno com deficiência?",
    "O que diz o Decreto 12.686/2025 sobre AEE?",
    "Como orientar a família de uma criança autista recém-diagnosticada?",
]
FORA = [
    "Qual é a capital da França?",
    "Me dê uma receita de bolo.",
    "Quem você acha que vai ganhar a próxima eleição?",
]


def _chat(client, pergunta, perfil="Professor", historico=None):
    return client.post("/api/chat", json={"pergunta": pergunta, "perfil": perfil, "historico": historico or []})


def test_health(client):
    corpo = client.get("/api/health").json()
    assert corpo["status"] == "ok"
    assert corpo["artigos"] > 0


def test_profiles(client):
    corpo = client.get("/api/profiles").json()
    assert [p["nome"] for p in corpo["perfis"]] == ["Professor", "Família", "Gestor"]
    assert len(corpo["perguntas_sugeridas"]) == 3


@pytest.mark.parametrize("pergunta", DENTRO)
def test_pergunta_dentro_do_escopo(client, pergunta):
    r = _chat(client, pergunta)
    assert r.status_code == 200
    corpo = r.json()
    assert corpo["origem"] != "fora_escopo"
    assert len(corpo["resposta"]) > 100


@pytest.mark.parametrize("pergunta", FORA)
def test_pergunta_fora_do_escopo(client, pergunta):
    corpo = _chat(client, pergunta).json()
    assert corpo["origem"] == "fora_escopo"
    assert corpo["fontes"] == []


@pytest.mark.parametrize("perfil", ["Professor", "Família", "Gestor"])
def test_pergunta_sugerida_tem_resposta_e_fontes(client, perfil):
    corpo = _chat(client, "O que é Atendimento Educacional Especializado?", perfil).json()
    assert corpo["perfil"] == perfil
    assert "AEE" in corpo["resposta"]
    assert corpo["fontes"]
    assert {"titulo", "url", "score"} <= corpo["fontes"][0].keys()


def test_perfil_invalido_cai_em_professor(client):
    assert _chat(client, "O que é AEE?", "Alien").json()["perfil"] == "Professor"


def test_resposta_nao_contem_urls(client):
    assert "http" not in _chat(client, "Como incluir aluno com TEA?").json()["resposta"]


def test_validacao_de_entrada(client):
    assert _chat(client, "").status_code == 422
    assert _chat(client, "   ").status_code == 422
    assert _chat(client, "a" * 1001).status_code == 422
    assert client.post("/api/chat", json={"pergunta": "oi", "historico": [{"role": "system", "content": "x"}]}).status_code == 422


def test_rate_limit(client, monkeypatch):
    from app.core.config import get_settings
    from app.main import create_app
    from fastapi.testclient import TestClient

    monkeypatch.setenv("RATE_LIMIT_POR_MINUTO", "3")
    get_settings.cache_clear()
    with TestClient(create_app()) as limitado:
        codigos = [_chat(limitado, "O que é AEE?").status_code for _ in range(5)]
    assert codigos == [200, 200, 200, 429, 429]
