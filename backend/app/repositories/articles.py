import csv
from pathlib import Path

from app.services.rag import Artigo, IndiceArtigos


def carregar_indice(caminho: Path) -> IndiceArtigos:
    # Os artigos completos passam do limite padrão de tamanho de campo do csv.
    csv.field_size_limit(10**9)
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        artigos = [
            Artigo(titulo=linha["titulo"], url=linha["url"], texto=linha["artigo_completo"])
            for linha in csv.DictReader(arquivo)
        ]
    return IndiceArtigos(artigos)
