from typing import TypeVar

from aiokafka import AIOKafkaProducer


class IProducerSettings:
    bootstrap_servers: str


TSettings = TypeVar("TSettings", bound=IProducerSettings)


class AsyncProducer[TSettings](AIOKafkaProducer):
    def __init__(
        self,
        settings: TSettings,
        **kwargs,
    ) -> None:
        super().__init__(bootstrap_servers=settings.bootstrap_servers, **kwargs)
        self._settings = settings
