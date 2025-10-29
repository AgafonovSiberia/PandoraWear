from typing import Optional

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import Header, HTTPException, status

from gateway.core.models import DevicePrincipal, AdminPrincipal
from gateway.core.protocols import DeviceAuthPort, AdminAuthPort


def _bearer_from_header(authorization: Optional[str]) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing_or_invalid_authorization",
        )
    return authorization[7:]


@inject
async def get_current_device(
    authorization: Optional[str] = Header(default=None),
    auth: FromDishka[DeviceAuthPort] = None,
) -> DevicePrincipal:
    token = _bearer_from_header(authorization)
    try:
        return await auth.verify_device_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_token"
        )


@inject
async def get_current_admin(
    authorization: Optional[str] = Header(default=None),
    auth: FromDishka[AdminAuthPort] = None,
) -> AdminPrincipal:
    token = _bearer_from_header(authorization)
    try:
        return await auth.verify_admin_jwt(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid_token"
        )
