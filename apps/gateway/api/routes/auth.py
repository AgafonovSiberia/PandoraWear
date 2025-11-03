from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from apps.common.dao.user import AuthUser, UserInLogin, UserInRegister
from apps.gateway.services.user import UserService

router = APIRouter(route_class=DishkaRoute, prefix="/api/users")


@router.post("/login", include_in_schema=True)
async def login(user_in: UserInLogin, user_service: FromDishka[UserService]) -> JSONResponse:
    token = await user_service.login(user_in=user_in)
    response = JSONResponse(status_code=200, content={})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=60 * 60 * 24,
        path="/",
    )
    return response


@router.post("/register", include_in_schema=True)
async def create_user(
    user_in: UserInRegister,
    user_service: FromDishka[UserService],
) -> JSONResponse:
    user = await user_service.register(user_in=user_in)
    response = JSONResponse(status_code=status.HTTP_201_CREATED, content="USER_CREATED")
    return response

@router.get("/me", include_in_schema=True)
async def me(
    auth_user: FromDishka[AuthUser],
) -> AuthUser:
    return auth_user

