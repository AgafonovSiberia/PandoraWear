from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse

from apps.common.dao.user import UserInLogin, UserInRegister
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
        secure=True,
        max_age=60 * 60 * 24,
    )
    return response


@router.post("/register", include_in_schema=True)
async def create_user(
    user_in: UserInRegister,
    user_service: FromDishka[UserService],
) -> RedirectResponse:
    user = user_service.get_user(email=user_in.email)

    if user is not None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = await user_service.register(user_in=user_in)
    response = RedirectResponse(url="/app", status_code=303)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=True,
        max_age=60 * 60 * 24,
    )

    return response
