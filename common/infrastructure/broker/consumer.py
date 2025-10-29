from aiokafka import AIOKafkaConsumer

from common.core.protocols.broker.consumer import IConsumerSettings, IConsumer


class KafkaAsyncConsumer(IConsumer):
    def __init__(self, settings: IConsumerSettings) -> None:
        self._broker = AIOKafkaConsumer(
            *settings.topic_names,
            bootstrap_servers=settings.bootstrap_servers,
            group_id=settings.group_id,
            auto_offset_reset=settings.auto_offset_reset,
            enable_auto_commit=settings.enable_auto_commit,
        )
        self.settings = settings
