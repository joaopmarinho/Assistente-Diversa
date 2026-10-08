import time
from collections import defaultdict, deque

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Janela deslizante de 60 s por IP, só na rota de chat; o estado vive em cada instância."""

    def __init__(self, app, limite_por_minuto: int):
        super().__init__(app)
        self._limite = limite_por_minuto
        self._acessos: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        if request.url.path != "/api/chat" or self._limite <= 0:
            return await call_next(request)

        ip = request.client.host if request.client else "desconhecido"
        agora = time.monotonic()
        janela = self._acessos[ip]
        while janela and agora - janela[0] > 60:
            janela.popleft()

        if len(janela) >= self._limite:
            return JSONResponse(
                {"detail": "Muitas requisições. Tente novamente em instantes."},
                status_code=429,
                headers={"Retry-After": "60"},
            )

        janela.append(agora)
        return await call_next(request)
