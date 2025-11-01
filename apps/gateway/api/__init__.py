from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from apps.gateway.api.routes.auth import router as auth_router

# from .engine import router as engine_router
from apps.gateway.api.routes.health import router as health_router


# from .pairing import router as pairing_router
# from .telemetry import router as telemetry_router


def get_api_router() -> APIRouter:
    router = APIRouter(route_class=DishkaRoute)
    router.include_router(health_router, tags=["health"])
    router.include_router(auth_router, tags=["auth"])
    # router.include_router(pairing_router, tags=["pairing"])
    # router.include_router(telemetry_router, tags=["telemetry"])
    # router.include_router(engine_router, tags=["engine"])
    return router
