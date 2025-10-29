from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from apps.gateway.api import get_api_router
from apps.gateway.api.middleware.auth import AuthMiddleware
from apps.gateway.di import create_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    fastapi = FastAPI(title="Pandora Gateway API", version="1.0.0", lifespan=lifespan)
    container = create_container()
    fastapi.include_router(get_api_router())
    fastapi.add_middleware(AuthMiddleware)
    setup_dishka(container, fastapi)
    return fastapi


app = create_app()
