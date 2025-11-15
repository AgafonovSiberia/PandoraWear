from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from apps.common.dao.user import AuthUser, UserInLogin, UserInRegister
from apps.gateway.services.user import UserService

router = APIRouter(route_class=DishkaRoute, prefix="/api/users")


@router.post("/login", include_in_schema=True)
async def login(user_in: UserInLogin, user_service: FromDishka[UserService]) -> JSONResponse:
    token = await user_service.login(user_in=user_in)
    response = JSONResponse(status_code=200, content={"access_token": token, "token_type": "bearer"})
    return response


@router.post("/register", include_in_schema=True)
async def create_user(
    user_in: UserInRegister,
    user_service: FromDishka[UserService],
) -> JSONResponse:
    user = await user_service.register(user_in=user_in)
    response = JSONResponse(status_code=status.HTTP_201_CREATED, content="USER_CREATED")
    return response


@router.post("/logout", include_in_schema=True)
async def logout_user(
    auth_user: FromDishka[AuthUser],
    user_service: FromDishka[UserService],
) -> JSONResponse:
    await user_service.logout(user_id=auth_user.id, token=auth_user.token)
    response = JSONResponse(status_code=status.HTTP_200_OK, content="TOKEN_REJECTED")
    return response


@router.get("/me", include_in_schema=True)
async def me(
    auth_user: FromDishka[AuthUser],
) -> AuthUser:
    return auth_user
