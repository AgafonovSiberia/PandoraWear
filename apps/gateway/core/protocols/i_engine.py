from typing import Protocol, Literal
from uuid import UUID


class IEngineService(Protocol):
    async def ping(
        self, user_id: UUID, device_id: UUID, action: Literal["start", "stop"]
    ) -> str: ...
