from pydantic import Field
from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379/0"
    redis_url: str = "redis://localhost:6379/0"


class GatewayProducerSettings(BaseSettings):
    bootstrap_servers: str = None

    model_config = {"env_prefix": "PRODUCER_"}


class GatewayConsumerSettings(BaseSettings):
    topic_names: list[str] = Field(default_factory=list)
    bootstrap_servers: str = None
    group_id: str = None
    auto_offset_reset: str = "latest"
    enable_auto_commit: bool = True

    model_config = {"env_prefix": "CONSUMER_"}
