from typing import Protocol


class IConsumerSettings(Protocol):
    topic_names: list[str]
    bootstrap_servers: str
    group_id: str
    auto_offset_reset: str = "earliest"
    enable_auto_commit: bool = True


class IConsumer(Protocol): ...
