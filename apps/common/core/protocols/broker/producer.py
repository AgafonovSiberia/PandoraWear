from typing import Protocol


class IProducerSettings(Protocol):
    bootstrap_servers: str


class IProducer(Protocol): ...
