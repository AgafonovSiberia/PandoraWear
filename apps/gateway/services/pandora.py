from fastapi import HTTPException, status

from apps.common.const import AlarmAction
from apps.common.core.protocols.repository import IUserRepo
from apps.common.dao.pandora import PandoraActionResponse, PandoraDevice
from apps.gateway.services.pandora_client.client import PandoraClient
from apps.gateway.services.pandora_client.command import PandoraCommand


def resolve_pandora_action(action: AlarmAction) -> PandoraCommand | None:
    action_map = {
        AlarmAction.START: PandoraCommand.START,
        AlarmAction.STOP: PandoraCommand.STOP,
    }
    return action_map.get(action)


class PandoraService:
    def __init__(self, user_repo: IUserRepo, pandora_client: PandoraClient):
        self._pandora = pandora_client
        self._user_repo = user_repo

    async def get_devices(self) -> list[PandoraDevice]:
        devices = await self._pandora.get_all_devices()
        return [PandoraDevice.model_validate(device) for device in devices]

    async def execute_command(self, alarm_device_id: int, action: AlarmAction) -> PandoraActionResponse:
        pandora_command = resolve_pandora_action(action)
        if pandora_command is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="UNKNOWN_COMMAND",
            )
        request = await self._pandora.run_command(device_id=alarm_device_id, pandora_command=pandora_command)
        return PandoraActionResponse.model_validate(request)
