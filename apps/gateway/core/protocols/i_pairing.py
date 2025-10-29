from typing import Protocol
from uuid import UUID

from apps.gateway.core.models import CreatedCode, BindedDevice


class IPairingService(Protocol):
    async def create_code(self, user_id: UUID) -> CreatedCode: ...

    async def bind_device(self, code: str, device_name: str) -> BindedDevice: ...
