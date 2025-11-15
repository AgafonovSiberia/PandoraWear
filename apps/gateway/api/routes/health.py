from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(route_class=DishkaRoute, prefix="/api", tags=["health"])


@router.get("")
async def root():
    return {"message": "Pandora Wear"}


@router.get("/health", include_in_schema=True)
async def health():
    return JSONResponse(content={"status": "ok"})


@router.get("/ready", include_in_schema=True)
async def ready():
    return JSONResponse(content={"status": "ok"})
