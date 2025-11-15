
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter

from apps.common.dao.pandora import AlarmActionIn, PandoraActionResponse, PandoraDeviceDomain
from apps.gateway.services.pandora import PandoraService

router = APIRouter(route_class=DishkaRoute, prefix="/api/alarm")

@router.post("/command", summary="Команда в сервис Pandora")
async def engine_command(
    action: AlarmActionIn,
    pandora_service: FromDishka[PandoraService] = None,
) -> PandoraActionResponse:
    return await pandora_service.execute_command(alarm_device_id=action.alarm_device_id, action=action.action)


@router.get("/devices", summary="Получить список доступных устройств")
async def get_devices(
    pandora_service: FromDishka[PandoraService] = None,
) -> list[PandoraDeviceDomain]:
    return await pandora_service.get_devices()