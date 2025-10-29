from typing import TypeVar

from aiokafka import AIOKafkaConsumer


class IConsumerSettings:
    topic_names: list[str]
    bootstrap_servers: str
    group_id: str
    auto_offset_reset: str = "earliest"
    enable_auto_commit: bool = True


TSettings = TypeVar("TSettings", bound=IConsumerSettings)


class AsyncConsumer[TSettings](AIOKafkaConsumer):
    def __init__(
        self,
        settings: TSettings,
        **kwargs,
    ) -> None:
        super().__init__(
            *settings.topic_names,
            bootstrap_servers=settings.bootstrap_servers,
            group_id=settings.group_id,
            auto_offset_reset=settings.auto_offset_reset,
            enable_auto_commit=settings.enable_auto_commit,
            **kwargs,
        )
        self._settings = settings
