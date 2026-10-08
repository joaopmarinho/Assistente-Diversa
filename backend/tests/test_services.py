from app.services.rag import tokens_busca
from app.services.scope import identificar_tema_fora_escopo, pergunta_dentro_escopo
from app.services.text import limpar_fontes_da_resposta, remover_paragrafos_duplicados


def test_tokens_busca_expande_sinonimos_e_remove_stopwords():
    tokens = tokens_busca("Como incluir aluno com TEA?")
    assert "tea" in tokens and "autismo" in tokens
    assert "como" not in tokens and "aluno" not in tokens


def test_escopo():
    assert pergunta_dentro_escopo("O que é AEE?")
    assert not pergunta_dentro_escopo("Qual é a capital da França?")
    assert identificar_tema_fora_escopo("Quem ganhou o jogo do Brasil?") == "esporte"


def test_limpar_fontes():
    texto = "Resposta útil.\n\nFonte: Portal\nhttps://diversa.org.br/x\n---"
    assert limpar_fontes_da_resposta(texto) == "Resposta útil."


def test_remover_duplicados():
    assert remover_paragrafos_duplicados("Olá mundo.\n\nOlá mundo.") == "Olá mundo."
