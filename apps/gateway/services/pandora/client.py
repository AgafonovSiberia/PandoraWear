from apps.gateway.services.pandora import (
    URL,
    RequestMethod,
    Command,
)
from apps.gateway.services.pandora.session import PandoraSession


class PandoraClient:
    def __init__(self, session: PandoraSession):
        self._session = session

    async def get_all_devices(self):
        response = await self._session.request(
            method=RequestMethod.GET, path=URL.DEVICES_PATH
        )
        return await response.json()

    # async def get_device_id(self, device_name: str = None) -> int:
    #     """Get device id"""
    #     if not device_name:
    #         raise pandora_exeption.NotDeviceId(device_name=str(device_name))
    #
    #     if self.devices is None:
    #         await self.get_all_devices()
    #
    #     for device in self.devices:
    #         if device.name == device_name:
    #             return device.device_id
    #
    #     raise pandora_exeption.NotDeviceId(device_name=str(device_name))

    async def engine_control(
        self,
        device_id: int = None,
        command: Command = Command.STOP_ENGINE,
    ):

        return await self._session.request(
            method=RequestMethod.POST,
            url=URL.COMMAND_PATH,
            data={"id": device_id, "command": command},
        )
