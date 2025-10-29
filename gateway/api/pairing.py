from uuid import UUID

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, Depends, HTTPException, status

from gateway.api.schemas import (
    PairCodeCreateOut,
    PairClaimIn,
    PairClaimOut,
    DeviceOut,
    DeviceRenameIn,
    ApiMessage,
)
from gateway.auth.deps import get_current_admin
from gateway.core.protocols import IPairingService, IDeviceService

router = APIRouter()


@router.post(
    "/pair/code",
    response_model=PairCodeCreateOut,
    summary="Создать код привязки (админ)",
)
@inject
async def create_pair_code(
    admin=Depends(get_current_admin),
    pairing: FromDishka[IPairingService] = None,
):
    code, exp = await pairing.create_code(admin.user_id)
    return PairCodeCreateOut(code=code, expires_at=exp)


@router.post(
    "/pair/claim", response_model=PairClaimOut, summary="Привязать устройство по коду"
)
@inject
async def claim_device(
    payload: PairClaimIn,
    pairing: FromDishka[IPairingService] = None,
):
    token, device_id, user_id, exp = await pairing.claim(
        payload.code, payload.device_name
    )
    return PairClaimOut(
        token=token, device_id=device_id, user_id=user_id, expires_at=exp
    )


@router.get(
    "/devices", response_model=list[DeviceOut], summary="Список устройств (админ)"
)
@inject
async def list_devices(
    admin=Depends(get_current_admin),
    device_svc: FromDishka[IDeviceService] = None,
):
    devices = await device_svc.list_for_user(admin.user_id)
    return [DeviceOut(**d) for d in devices]


@router.post(
    "/devices/{device_id}/revoke",
    response_model=ApiMessage,
    summary="Отвязать устройство",
)
@inject
async def revoke_device(
    device_id: UUID,
    admin=Depends(get_current_admin),
    device_svc: FromDishka[IDeviceService] = None,
):
    ok = await device_svc.revoke(admin.user_id, device_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not_found")
    return ApiMessage(message="revoked")


@router.post(
    "/devices/{device_id}/rename",
    response_model=DeviceOut,
    summary="Переименовать устройство",
)
@inject
async def rename_device(
    device_id: UUID,
    payload: DeviceRenameIn,
    admin=Depends(get_current_admin),
    device_svc: FromDishka[IDeviceService] = None,
):
    dev = await device_svc.rename(admin.user_id, device_id, payload.name)
    if not dev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not_found")
    return DeviceOut(**dev)
