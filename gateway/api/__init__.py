from fastapi import APIRouter

from .engine import router as engine_router
from .health import router as health_router
from .pairing import router as pairing_router
from .telemetry import router as telemetry_router


def get_api_router() -> APIRouter:
    router = APIRouter()
    router.include_router(health_router, tags=["health"])
    router.include_router(pairing_router, tags=["pairing"])
    router.include_router(telemetry_router, tags=["telemetry"])
    router.include_router(engine_router, tags=["engine"])
    return router
