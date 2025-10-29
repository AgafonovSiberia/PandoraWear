from aiokafka import AIOKafkaProducer

from common.core.protocols.broker.producer import IProducer, IProducerSettings


class KafkaAsyncProducer(IProducer):
    def __init__(self, settings: IProducerSettings) -> None:
        self._broker = AIOKafkaProducer(bootstrap_servers=settings.bootstrap_servers)
        self.settings = settings

    async def send(self, topic: str, payload: dict) -> None:
        await self._broker.send_and_wait(topic=topic, value=payload)
