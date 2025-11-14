from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from apps.gateway.api.routes.auth import router as auth_router
from apps.gateway.api.routes.config import router as config_router
from apps.gateway.api.routes.health import router as health_router
from apps.gateway.api.routes.pandora import router as pandora_router

from .routes.device import router as device_router


def get_api_router() -> APIRouter:
    router = APIRouter(route_class=DishkaRoute)
    router.include_router(health_router, tags=["health"])
    router.include_router(auth_router, tags=["auth"])
    router.include_router(device_router, tags=["devices"])
    router.include_router(config_router, tags=["config"])
    router.include_router(pandora_router, tags=["pandora_client"])
    return router
