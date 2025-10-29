from gateway.pandora import URL, RequestMethod, Command, excepton as pandora_exeption

from gateway.pandora.base import BaseClient
from gateway.pandora.models.device import Device


class PandoraClient(BaseClient):
    """Pandora API-class"""

    def __init__(self, username: str, password: str):
        super().__init__(username, password)
        self.devices: list[Device] | None = None

    async def get_all_devices(self):
        """Get all devices"""
        devices_data = await self.request(url=URL.DEVICES_PATH)
        self.devices = [Device(**device) for device in devices_data]

    async def get_device_id(self, device_name: str = None) -> int:
        """Get device id"""
        if not device_name:
            raise pandora_exeption.NotDeviceId(device_name=str(device_name))

        if self.devices is None:
            await self.get_all_devices()

        for device in self.devices:
            if device.name == device_name:
                return device.device_id

        raise pandora_exeption.NotDeviceId(device_name=str(device_name))

    async def engine_control(
        self,
        device_name: str = None,
        device_id: int = None,
        command: Command = Command.STOP_ENGINE,
    ):
        """Engine control method"""
        if device_id is None:
            device_id = await self.get_device_id(device_name=device_name)

        return await self.session.request(
            method=RequestMethod.POST,
            url=URL.COMMAND_PATH,
            data={"id": device_id, "command": command},
        )
