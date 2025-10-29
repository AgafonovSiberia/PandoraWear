from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, Depends, HTTPException, status

from gateway.api.schemas import EngineCommandIn, EngineAcceptedOut
from gateway.auth.deps import get_current_device
from gateway.core.protocols import IEngineService

router = APIRouter()


@router.post(
    "/engine", response_model=EngineAcceptedOut, summary="Старт/стоп двигателя (часы)"
)
@inject
async def engine_command(
    payload: EngineCommandIn,
    dev=Depends(get_current_device),
    engine: FromDishka[IEngineService] = None,
):
    try:
        event_id = await engine.enqueue(dev.user_id, dev.device_id, payload.action)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(e)
        )
    return EngineAcceptedOut(event_id=event_id)
