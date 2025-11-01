from pydantic import Field, PostgresDsn, model_validator
from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):
    secret_key: str = "ecrlnkognor"

    model_config = {"env_prefix": "AUTH_"}


class RedisSettings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"


class ProducerSettings(BaseSettings):
    bootstrap_servers: str = None

    model_config = {"env_prefix": "PRODUCER_"}


class ConsumerSettings(BaseSettings):
    topic_names: list[str] = Field(default_factory=list)
    bootstrap_servers: str = None
    group_id: str = None
    auto_offset_reset: str = "latest"
    enable_auto_commit: bool = True

    model_config = {"env_prefix": "CONSUMER_"}


class DatabaseSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_URL: PostgresDsn | None = None

    @model_validator(mode="after")
    def assemble_db_url(self) -> "DatabaseSettings":
        if self.DB_URL is None:
            self.DB_URL = PostgresDsn.build(scheme="postgresql+asyncpg",
                                            host=self.POSTGRES_HOST,
                                            port=self.POSTGRES_PORT,
                                            username=self.POSTGRES_USER,
                                            password=self.POSTGRES_PASSWORD,
                                            path=self.POSTGRES_DB)
        return self

    # model_config = {"env_prefix": "DB_"}
