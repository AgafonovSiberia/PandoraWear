# from dishka.integrations.fastapi import inject, FromDishka
# from fastapi import APIRouter, Depends, HTTPException, status
#
# from apps.gateway.api.schemas import TelemetryOut
# from apps.gateway.auth.deps import get_current_device
# from apps.gateway.core.protocols import ITelemetryService
#
# router = APIRouter()
#
#
# @router.get(
#     "/telemetry", response_model=TelemetryOut, summary="Текущая телеметрия (часы)"
# )
# @inject
# async def get_telemetry(
#     dev=Depends(get_current_device),
#     telemetry: FromDishka[ITelemetryService] = None,
# ):
#     data = await telemetry.get_snapshot(dev.user_id)
#     if data is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="not_available"
#         )
#     return TelemetryOut(**data)
