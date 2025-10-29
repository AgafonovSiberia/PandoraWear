from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    KAFKA_BROKER_URL: str = "kafka://localhost:9092"
    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = {"env_prefix": "API_"}
