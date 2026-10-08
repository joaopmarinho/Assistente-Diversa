import json
import logging
from datetime import datetime, timezone

# Uma linha JSON por interação; em Lambda o stdout já vai para o CloudWatch.
_logger = logging.getLogger("interacoes")


def registrar_interacao(perfil: str, pergunta: str, origem: str, fontes: list[dict]) -> None:
    _logger.info(
        json.dumps(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "perfil": perfil,
                "pergunta": pergunta,
                "origem": origem,
                "artigos": [f["titulo"] for f in fontes],
                "scores": [f["score"] for f in fontes],
            },
            ensure_ascii=False,
        )
    )
