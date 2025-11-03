import os
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.gateway.api import get_api_router
from apps.gateway.api.middleware.auth import AuthMiddleware
from apps.gateway.di import create_container

if os.getenv("DEBUG_MODE") == "1":
    import pydevd

    pydevd.settrace(
        "host.docker.internal",
        port=5678,
        stdout_to_server=True,
        stderr_to_server=True,
        overwrite_prev_trace=True,
        suspend=False,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


def create_app() -> FastAPI:
    fastapi = FastAPI(title="Pandora Gateway API", version="1.0.0", lifespan=lifespan)
    container = create_container()
    fastapi.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    fastapi.add_middleware(AuthMiddleware)
    fastapi.include_router(get_api_router())
    setup_dishka(container, fastapi)

    return fastapi


app = create_app()
