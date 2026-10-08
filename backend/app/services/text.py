import re
import unicodedata


def limpar_texto(texto: str) -> str:
    texto = re.sub(r"\s+", " ", str(texto))
    texto = re.sub(r"\[.*?\]", "", texto)
    texto = re.sub(r"http\S+", "", texto)
    return texto.strip()


def normalizar(texto: str) -> str:
    """Minúsculas, sem acentos e com espaços colapsados."""
    texto = unicodedata.normalize("NFD", str(texto or "").lower())
    texto = "".join(ch for ch in texto if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", texto).strip()


def remover_paragrafos_duplicados(texto: str) -> str:
    texto = str(texto or "").strip()
    if not texto:
        return ""

    unicos, vistos = [], set()
    for paragrafo in (p.strip() for p in re.split(r"\n\s*\n", texto)):
        chave = normalizar(paragrafo)
        if paragrafo and chave not in vistos:
            vistos.add(chave)
            unicos.append(paragrafo)
    texto = "\n\n".join(unicos)

    frases_unicas, frases_vistas = [], set()
    for frase in re.split(r"(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ])", texto):
        frase = frase.strip()
        chave = normalizar(frase)
        if frase and chave not in frases_vistas:
            frases_vistas.add(chave)
            frases_unicas.append(frase)
    return " ".join(frases_unicas).strip()


_MARCADORES_FONTE = (
    "fonte:", "fontes:", "fonte consultada:", "fontes consultadas:",
    "referência:", "referências:", "referencia:", "referencias:",
    "url:", "link:", "links:", "leia mais:", "saiba mais:",
    "artigo consultado:", "artigos consultados:",
)


def limpar_fontes_da_resposta(texto: str) -> str:
    """Remove linhas de fonte/URL; as fontes são exibidas só no painel."""
    texto = str(texto or "").strip()
    if not texto:
        return ""

    linhas = []
    for linha in texto.splitlines():
        conteudo = linha.strip()
        baixo = conteudo.lower()
        if baixo.startswith(_MARCADORES_FONTE):
            continue
        if re.fullmatch(r"[\(\[]?https?://\S+[\)\]]?", conteudo):
            continue
        if "diversa.org.br" in baixo and (conteudo.startswith("(") or baixo.startswith("http")):
            continue
        if re.fullmatch(r"[-–—_ ]{3,}", conteudo):
            continue
        linhas.append(linha)

    return re.sub(r"\n{3,}", "\n\n", "\n".join(linhas)).strip()
