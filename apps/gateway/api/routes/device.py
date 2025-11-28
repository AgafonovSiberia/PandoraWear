import uuid

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse

from apps.common.dao.device import DeviceDomain, DevicePairDataOut, DeviceRegData
from apps.common.dao.user import AuthUser, ConfirmDeviceIn
from apps.gateway.services.device import DeviceService

router = APIRouter(route_class=DishkaRoute, prefix="/api/devices")


@router.get("", include_in_schema=True, description="Получить список всех устройств")
async def get_all_devices(
    auth_user: FromDishka[AuthUser], device_service: FromDishka[DeviceService]
) -> list[DeviceDomain]:
    devices = await device_service.get_all(user_id=auth_user.id)
    return devices or []


@router.post("/pairing", include_in_schema=True, description="Получить код сопряжения")
async def pair(
    device_data: DeviceRegData, auth_user: FromDishka[AuthUser], device_service: FromDishka[DeviceService]
) -> JSONResponse:
    code = await device_service.generate_pair_code(user_id=auth_user.id, device_name=device_data.name)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"pair_code": code})


@router.post("/pairing/code/{code}", include_in_schema=True, description="Сопряжение устройства по коду")
async def pair_confirm(code: str, device_service: FromDishka[DeviceService]) -> DevicePairDataOut:
    paired_device_data = await device_service.pair_by_code(pair_code=code)
    return paired_device_data


@router.post("/pairing/cred", include_in_schema=True, description="Сопряжение устройства по данным авторизации")
async def pair_confirm_by_cred(
    confirm_in: ConfirmDeviceIn, request: Request, device_service: FromDishka[DeviceService]
) -> DevicePairDataOut:
    paired_device_data = await device_service.pair_by_cred(confirm_in=confirm_in)
    return paired_device_data


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=True,
    description="Отозвать сопряжение с устройством",
)
async def revoke(device_id: uuid.UUID, device_service: FromDishka[DeviceService]) -> Response:
    await device_service.device_revoke(device_id=device_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
