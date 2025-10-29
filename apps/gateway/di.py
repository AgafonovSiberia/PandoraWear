from aiohttp import TCPConnector
from dishka import (
    Scope,
    provide,
    make_async_container,
    AsyncContainer,
)
from dishka.integrations.fastapi import FastapiProvider
from fastapi import Request

from apps.common.core.protocols import IUserRepo
from apps.common.core.protocols.broker.consumer import IConsumerSettings, IConsumer
from apps.common.core.protocols.broker.producer import IProducer, IProducerSettings
from apps.common.core.protocols.icache import ICache
from apps.common.infrastructure.broker.consumer import KafkaAsyncConsumer
from apps.common.infrastructure.broker.producer import KafkaAsyncProducer
from apps.common.infrastructure.cache.redis import RedisCache
from apps.common.infrastructure.repository.user import UserRepo
from apps.gateway.common.context import UserContext
from apps.gateway.config import (
    RedisSettings,
    GatewayConsumerSettings,
    GatewayProducerSettings,
)
# from apps.gateway.core.protocols import (
#     IPairingService,
#     IDeviceService,
#     ITelemetryService,
#     IEngineService,
#     IDeviceAuth,
#     IAdminAuth,
# )
from apps.gateway.services.pandora.client import PandoraClient
from apps.gateway.services.pandora.session_manager import PandoraClientManager


class ConfigProvider(FastapiProvider):
    @provide(scope=Scope.APP)
    async def producer_settings(self) -> IProducerSettings:
        return GatewayProducerSettings()

    @provide(scope=Scope.APP)
    async def consumer_settings(self) -> IConsumerSettings:
        return GatewayConsumerSettings()


class InfraProvider(FastapiProvider):
    @provide(scope=Scope.APP)
    async def cache(self) -> ICache:
        settings = RedisSettings()
        return RedisCache(url=settings.REDIS_URL, prefix="api")

    @provide(scope=Scope.APP)
    async def producer(self, settings: IProducerSettings) -> IProducer:
        return KafkaAsyncProducer(settings)

    @provide(scope=Scope.APP)
    async def consumer(self, settings: IConsumerSettings) -> IConsumer:
        return KafkaAsyncConsumer(settings)


class ServiceProvider(FastapiProvider):
    @provide(scope=Scope.APP)
    async def tcp_connector(self) -> TCPConnector:
        return TCPConnector(
            limit=10, limit_per_host=2, ttl_dns_cache=300, enable_cleanup_closed=True
        )

    @provide(scope=Scope.REQUEST)
    async def user_context(self, request: Request) -> UserContext:
        """Адаптер между FastAPI и внутренним контекстом запроса."""
        return UserContext(user_id=request.state.user_id)

    @provide(scope=Scope.APP)
    async def user_repo(self) -> IUserRepo:
        return UserRepo()

    @provide(scope=Scope.APP)
    async def pandora_manager(
        self, user_repo: IUserRepo, tcp_connector: TCPConnector
    ) -> PandoraClientManager:
        return PandoraClientManager(user_repo=user_repo, connector=tcp_connector)

    @provide(scope=Scope.REQUEST)
    async def pandora_client(
        self,
        pandora_client_manager: PandoraClientManager,
        user_context: UserContext,
    ) -> PandoraClient:
        return await pandora_client_manager.get_pandora_client(
            user_id=user_context.user_id
        )


def create_container() -> AsyncContainer:
    container = make_async_container(
        ConfigProvider(), InfraProvider(), ServiceProvider()
    )
    return container
