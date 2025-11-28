
from apps.common.core.protocols.cache import ICache
from apps.common.dao.config import PandoraCredDomain
from apps.gateway.services.pandora_client.const import URL, PandoraCommand
from apps.gateway.services.pandora_client.session import PandoraSession


class PandoraClient:
    def __init__(self, session: PandoraSession):
        self._session = session

    async def get_all_devices(self) -> dict:
        return await self._session.request_json(method="GET", path=URL.devices)

    async def get_updates(self) -> dict:
        return await self._session.request_json(method="GET", path=URL.update, params={"ts": -1})

    async def run_command(
        self,
        pandora_command: PandoraCommand,
        device_id: int,
    ) -> dict:
        return await self._session.request_json(
            method="POST", path=URL.command, data={"id": device_id, "command": pandora_command.value}
        )


async def resolve_pandora_client(user_id: int, pandora_cred: PandoraCredDomain, cache: ICache) -> PandoraClient:
    session = PandoraSession(cred=pandora_cred, user_id=user_id, cache=cache)
    return PandoraClient(session=session)
