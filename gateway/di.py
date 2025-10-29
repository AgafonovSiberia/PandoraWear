from dishka import Container, Provider, Scope, make_container, provide

from gateway.config import Settings
from gateway.core.protocols import (
    PairingServicePort,
    DeviceServicePort,
    TelemetryServicePort,
    EngineServicePort,
    DeviceAuthPort,
    AdminAuthPort,
)


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    async def settings(self) -> Settings:
        """Загружает конфигурацию из env"""
        return Settings()


class InfraProvider(Provider):
    @provide(scope=Scope.APP)
    async def redis_cache(self, settings: Settings) -> RedisCache:
        """Единый Redis для всех сервисов"""
        return RedisCache(url=settings.REDIS_URL)

    @provide(scope=Scope.APP)
    async def kafka_producer(self, settings: Settings) -> KafkaProducer:
        """Kafka-продьюсер"""
        return KafkaProducer(settings.KAFKA_BROKER_URL)

    @provide(scope=Scope.APP)
    async def pandora_client(self, settings: Settings) -> PandoraHttpClient:
        """HTTP-клиент Pandora"""
        return PandoraHttpClient(base_url=settings.PANDORA_BASE_URL)


# ---------- СЕРВИСЫ (РЕАЛИЗАЦИИ ПОРТОВ) ----------


class ServiceProvider(Provider):
    @provide(scope=Scope.APP)
    async def engine_service(
        self,
        pandora: PandoraHttpClient,
        kafka: KafkaProducer,
    ) -> EngineServicePort:
        return EngineService(pandora=pandora, kafka=kafka)

    @provide(scope=Scope.APP)
    async def telemetry_service(
        self,
        pandora: PandoraHttpClient,
        cache: RedisCache,
    ) -> TelemetryServicePort:
        return TelemetryService(pandora=pandora, cache=cache)

    @provide(scope=Scope.APP)
    async def pairing_service(
        self,
        cache: RedisCache,
    ) -> PairingServicePort:
        return PairingService(cache=cache)

    @provide(scope=Scope.APP)
    async def device_service(
        self,
        cache: RedisCache,
    ) -> DeviceServicePort:
        return DeviceService(cache=cache)

    @provide(scope=Scope.APP)
    async def device_auth_service(
        self,
        cache: RedisCache,
    ) -> DeviceAuthPort:
        return DeviceAuthService(redis=cache)

    @provide(scope=Scope.APP)
    async def admin_auth_service(
        self,
        cache: RedisCache,
    ) -> AdminAuthPort:
        return AdminAuthService(redis=cache)


def create_container() -> Container:
    provider = Provider(scope=Scope.APP)
    container = make_container(ConfigProvider(), InfraProvider(), ServiceProvider())
    return container
