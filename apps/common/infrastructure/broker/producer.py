import json

from aiokafka import AIOKafkaProducer

from apps.common.core.protocols.broker.producer import IProducer, IProducerSettings
from apps.common.tools.date import json_serializer


class KafkaAsyncProducer(IProducer):
    def __init__(self, settings: IProducerSettings) -> None:
        self._broker = AIOKafkaProducer(
            bootstrap_servers=settings.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, default=json_serializer).encode(
                "utf-8"
            ),
        )
        self.settings = settings

    async def send(self, topic: str, payload: dict) -> None:
        await self._broker.send_and_wait(topic=topic, value=payload)
