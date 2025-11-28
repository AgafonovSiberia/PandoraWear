import logging
import os
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.gateway.api import get_api_router
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


ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]


def create_app() -> FastAPI:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    container = create_container()

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        try:
            yield
        finally:
            await container.close()

    fastapi = FastAPI(title="Pandora Gateway API", version="1.0.0", lifespan=lifespan)

    fastapi.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    fastapi.include_router(get_api_router())
    setup_dishka(container, fastapi)

    return fastapi


app = create_app()
