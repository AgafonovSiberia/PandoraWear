from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from apps.common.dao.config import PandoraConfig, PandoraCredDomain, PandoraCredIn
from apps.common.dao.user import AuthUser
from apps.gateway.services.config import ConfigService
from apps.gateway.services.user import UserService

router = APIRouter(route_class=DishkaRoute, prefix="/api/config")


@router.get("/pandora", include_in_schema=True)
async def get_pandora_config(
    auth_user: FromDishka[AuthUser], user_service: FromDishka[UserService], config_service: FromDishka[ConfigService]
) -> PandoraConfig | None:
    return await config_service.get_pandora_config(user_id=auth_user.id)


@router.get("/pandora/cred", include_in_schema=True)
async def get_pandora_credentials(
    auth_user: FromDishka[AuthUser], user_service: FromDishka[UserService], config_service: FromDishka[ConfigService]
) -> PandoraCredDomain | None:
    return await config_service.get_pandora_cred(user_id=auth_user.id)


@router.post("/pandora/cred", include_in_schema=True)
async def upsert_pandora_credentials(
    pandora_cred_in: FromDishka[PandoraCredIn],
    auth_user: FromDishka[AuthUser],
    user_service: FromDishka[UserService],
    config_service: FromDishka[ConfigService],
) -> PandoraCredDomain | None:
    return await config_service.upsert_pandora_cred(pandora_in=pandora_cred_in)

