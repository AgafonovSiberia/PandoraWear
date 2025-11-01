from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from apps.common.core.protocols.repository import IUserRepo

router = APIRouter(route_class=DishkaRoute, prefix="/app")


@router.get("/", include_in_schema=True)
async def login(user_repo: FromDishka[IUserRepo]) -> JSONResponse:
    return JSONResponse(content={"status": "ok"})
