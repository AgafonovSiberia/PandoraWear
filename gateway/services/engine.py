from gateway.core.protocols import EngineServicePort


class EngineService(EngineServicePort):
    def __init__(self, pandora, kafka):
        self._pandora = pandora
        self._kafka = kafka

    async def ping(self, user_id, device_id, action):
        await self._pandora.check_vehicle_state(device_id)
        # публикуем команду
        await self._kafka.publish(
            {
                "user": str(user_id),
                "device": str(device_id),
                "action": action,
            }
        )
        return "evt_" + str(device_id)  # идентификатор события
