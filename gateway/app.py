from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from gateway.api import get_api_router
from gateway.di import create_container


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Управляет жизненным циклом Dishka-контейнера и ресурсов."""
#     container = create_container()
#     setup_dishka(container, app)
#
#     kafka = await container.get("KafkaProducer", optional=True)
#     pandora = await container.get("PandoraHttpClient", optional=True)
#
#     try:
#         yield
#     finally:
#         if kafka and hasattr(kafka, "stop"):
#             await kafka.stop()
#         if pandora and hasattr(pandora, "_client"):
#             await pandora._client.aclose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Pandora Gateway API",
        version="1.0.0",
        # lifespan=lifespan,
    )

    app.include_router(get_api_router())
    return app


app = create_app()
# @app.post("/control_engine")
# async def control_engine(request: Request):
#     async with PandoraClient(username=config.login, password=config.password) as client:
#         await client.login()
#         await client.get_all_devices()
#         await client.engine_control(
#             device_name="FREELANDER", command=Command.RUN_ENGINE
#         )
#
#
# @app.get("/")
# def root():
#     return Response(
#         status_code=200, content="Hello! I am Alice-skill for engine control"
#     )
