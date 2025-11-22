
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status
from starlette.responses import JSONResponse

from apps.common.dao.device import AuthDevice
from apps.common.dao.pandora import AlarmActionIn, PandoraDeviceDomain
from apps.gateway.services.pandora import PandoraService

router = APIRouter(route_class=DishkaRoute, prefix="/api/alarm")

@router.post("/command", summary="Команда в сервис Pandora")
async def engine_command(
    action: AlarmActionIn,
    pandora_service: FromDishka[PandoraService],
) -> JSONResponse:
    pandora_response = await pandora_service.execute_command(
        alarm_device_id=action.alarm_device_id, action=action.action
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content=pandora_response.model_dump())


@router.get("/devices", summary="Получить список доступных устройств")
async def get_devices(
    auth_device: FromDishka[AuthDevice],
    pandora_service: FromDishka[PandoraService],
) -> list[PandoraDeviceDomain]:
    return await pandora_service.get_devices()