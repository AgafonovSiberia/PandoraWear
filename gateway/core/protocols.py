from datetime import datetime
from typing import Protocol, Literal, Optional
from uuid import UUID

from .models import DevicePrincipal, AdminPrincipal, CreatedCode, BindedDevice


class ErrInvalidCode(Exception): ...


class ErrExpired(Exception): ...


class ErrAlreadyUsed(Exception): ...


class ErrTooManyRequests(Exception): ...


class ErrForbidden(Exception): ...


class ErrNotFound(Exception): ...


class DeviceAuthPort(Protocol):
    async def verify_device_token(self, token: str) -> DevicePrincipal: ...


class AdminAuthPort(Protocol):
    async def verify_admin_jwt(self, token: str) -> AdminPrincipal: ...


class PairingServicePort(Protocol):
    async def create_code(self, user_id: UUID) -> CreatedCode: ...

    async def bind_device(self, code: str, device_name: str) -> BindedDevice: ...


class DeviceServicePort(Protocol):
    async def list_for_user(self, user_id: UUID) -> list[dict]: ...
    async def revoke(self, user_id: UUID, device_id: UUID) -> bool: ...


class TelemetryServicePort(Protocol):
    async def get_snapshot(self, user_id: UUID) -> Optional[dict]: ...


class EngineServicePort(Protocol):
    async def ping(
        self, user_id: UUID, device_id: UUID, action: Literal["start", "stop"]
    ) -> str: ...
