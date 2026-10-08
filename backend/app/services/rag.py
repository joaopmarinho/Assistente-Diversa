import re
from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.text import limpar_texto, normalizar

_STOPWORDS = {
    "como", "para", "com", "uma", "um", "uns", "umas", "que", "qual", "quais", "onde", "quando",
    "sobre", "sala", "aula", "aluno", "alunos", "estudante", "estudantes", "criança", "crianca",
    "trabalhar", "incluir", "inclusao", "inclusão", "educacao", "educação", "escola", "escolar",
    "def", "dos", "das", "por", "sem", "mais", "menos", "isso", "essa", "esse", "esta", "este",
}

_SINONIMOS = {
    "tea": ["autismo", "autista", "transtorno do espectro autista"],
    "autismo": ["tea", "autista", "transtorno do espectro autista"],
    "autista": ["tea", "autismo", "transtorno do espectro autista"],
    "tdah": ["atenção", "atencao", "hiperatividade", "transtorno do déficit de atenção", "transtorno do deficit de atencao"],
    "aee": ["atendimento educacional especializado", "sala de recursos", "recursos multifuncionais"],
}


@dataclass(frozen=True)
class Artigo:
    titulo: str
    url: str
    texto: str


@dataclass(frozen=True)
class ArtigoEncontrado:
    titulo: str
    url: str
    trecho: str
    score: float


def tokens_busca(pergunta: str) -> list[str]:
    tokens = re.findall(r"\b[a-z0-9]{3,}\b", normalizar(pergunta))
    expandidos: list[str] = []
    for token in (t for t in tokens if t not in _STOPWORDS):
        expandidos.append(token)
        expandidos.extend(_SINONIMOS.get(token, []))

    vistos: set[str] = set()
    resultado = []
    for token in expandidos:
        chave = normalizar(token)
        if chave and chave not in vistos:
            vistos.add(chave)
            resultado.append(chave)
    return resultado


def extrair_trecho_relevante(texto: str, pergunta: str, janela: int = 1800) -> str:
    """Devolve a região do artigo onde os termos da pergunta aparecem, não só o início."""
    texto = limpar_texto(texto)
    if len(texto) <= janela:
        return texto

    texto_norm = normalizar(texto)
    posicoes = sorted(p for p in (texto_norm.find(t) for t in tokens_busca(pergunta)) if p >= 0)
    if not posicoes:
        return texto[:janela].strip()

    centro = posicoes[len(posicoes) // 2]
    inicio = max(0, centro - janela // 3)
    fim = min(len(texto), inicio + janela)
    inicio = max(0, fim - janela)

    trecho = texto[inicio:fim].strip()
    if inicio > 0:
        trecho = "..." + trecho
    if fim < len(texto):
        trecho += "..."
    return trecho


class IndiceArtigos:
    """Índice TF-IDF em memória, construído uma vez na subida da aplicação."""

    def __init__(self, artigos: list[Artigo]):
        self._artigos = [
            Artigo(a.titulo, a.url, limpar_texto(a.texto))
            for a in artigos
            if len(limpar_texto(a.texto)) > 120
        ]
        self._vetorizador = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=8000,
            sublinear_tf=True,
            strip_accents="unicode",
            lowercase=True,
        )
        # O título entra duas vezes para pesar mais na busca.
        self._matriz = self._vetorizador.fit_transform(
            [f"{a.titulo}. {a.titulo}. {a.texto}" for a in self._artigos]
        )

    def __len__(self) -> int:
        return len(self._artigos)

    def buscar(self, pergunta: str, top_k: int = 3, score_minimo: float = 0.012) -> list[ArtigoEncontrado]:
        scores = cosine_similarity(self._vetorizador.transform([pergunta]), self._matriz)[0]
        resultados = []
        for i in scores.argsort()[::-1][:top_k]:
            if scores[i] >= score_minimo:
                artigo = self._artigos[i]
                resultados.append(
                    ArtigoEncontrado(
                        titulo=artigo.titulo,
                        url=artigo.url,
                        trecho=extrair_trecho_relevante(artigo.texto, pergunta),
                        score=round(float(scores[i]), 4),
                    )
                )
        return resultados
