from apps.gateway.services.pandora_client.command import PandoraCommand
from apps.gateway.services.pandora_client.session import PandoraSession
from apps.gateway.services.pandora_client.url import URL


class PandoraClient:
    def __init__(self, session: PandoraSession):
        self._session = session

    async def get_all_devices(self) -> dict:
        response = await self._session.request(method="GET", path=URL.devices)
        return await response.json()

    async def get_updates(self) -> dict:
        response = await self._session.request(method="GET", path=URL.update, params={"ts": -1})
        return await response.json()

    async def run_command(
        self,
        pandora_command: PandoraCommand,
        device_id: int = None,
    ) -> dict:
        response = await self._session.request(
            method="POST", path=URL.command, data={"id": device_id, "command": pandora_command.value}
        )
        return await response.json()
