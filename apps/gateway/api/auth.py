from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse

from apps.gateway.auth.crypto import crypt_password, check_password
from common.infrastructure.repository.user import UserRepo
from common.models.user import User, UserIn, FormUserReg

router = APIRouter(route_class=DishkaRoute, prefix="/api/users")


@router.get("/login", include_in_schema=True)
async def login(user_in: UserIn, user_repo: FromDishka[UserRepo]) -> JSONResponse:
    user: User = await user_repo.find_user_by_email(email=user_in.email)
    if user is None:
        raise HTTPException(
            status_code=400, detail=f"User with email {user_in.email} not exists"
        )

    if not check_password(user_in.password, user.password_hash):
        raise HTTPException(status_code=403, detail=f"Incorrect password")

    return JSONResponse(content={"status": "ok"})


@router.post("/", response_model=User)
async def create_user(
    reg_form: FormUserReg, user_repo: FromDishka[UserRepo]
) -> RedirectResponse:
    user = await user_repo.find_user_by_email(email=reg_form.email)
    if user is not None:
        raise HTTPException(
            status_code=400, detail=f"User with email {reg_form.email} already exists"
        )

    reg_form.password = crypt_password(reg_form.password)
    await user_repo.save_user(user=reg_form)
    return RedirectResponse(url="/login")
