import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import get_settings
from app.core.rate_limit import RateLimitMiddleware
from app.repositories.articles import carregar_indice

logging.basicConfig(level=logging.INFO, format="%(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.indice = carregar_indice(get_settings().artigos_csv)
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Assistente Diversa API", lifespan=lifespan)

    app.add_middleware(RateLimitMiddleware, limite_por_minuto=settings.rate_limit_por_minuto)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )
    app.include_router(router)
    return app


app = create_app()
