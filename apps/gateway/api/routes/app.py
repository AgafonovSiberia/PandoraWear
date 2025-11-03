from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from apps.common.dao.user import AuthUser, UserDomain

router = APIRouter(route_class=DishkaRoute, prefix="/api/app")


@router.get("/", response_model=UserDomain, include_in_schema=True)
async def login(current_user: FromDishka[AuthUser]) -> AuthUser:
    return current_user
