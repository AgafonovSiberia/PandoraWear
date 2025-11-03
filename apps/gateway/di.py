from typing import Any, AsyncGenerator

from aiohttp import TCPConnector
from dishka import (
    AsyncContainer,
    Scope,
    make_async_container,
    provide,
)
from dishka.integrations.fastapi import FastapiProvider
from fastapi import Request
from sqlalchemy.ext.asyncio.session import AsyncSession

from apps.common.config import (
    ConsumerSettings,
    DatabaseSettings,
    ProducerSettings,
    RedisSettings,
    SecureSettings,
)
from apps.common.core.protocols.broker.consumer import IConsumer, IConsumerSettings
from apps.common.core.protocols.broker.producer import IProducer, IProducerSettings
from apps.common.core.protocols.cache import ICache
from apps.common.core.protocols.repository import IDeviceRepo, IUserRepo
from apps.common.dao.user import AuthUser
from apps.common.infrastructure.broker.consumer import KafkaAsyncConsumer
from apps.common.infrastructure.broker.producer import KafkaAsyncProducer
from apps.common.infrastructure.cache.redis import RedisCache
from apps.common.infrastructure.database.database import DatabaseCore
from apps.common.repository.device import DeviceRepo
from apps.common.repository.user import UserRepo
from apps.gateway.common.context import UserContext
from apps.gateway.services.auth import AuthService
from apps.gateway.services.device import DeviceService
from apps.gateway.services.pandora.client import PandoraClient
from apps.gateway.services.pandora.session_manager import PandoraClientManager
from apps.gateway.services.user import UserService


class DatabaseProvider(FastapiProvider):
    @provide(scope=Scope.APP)
    async def database_core(self) -> DatabaseCore:
        db_settings = DatabaseSettings()
        return DatabaseCore(db_settings)

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def db_session(self, database: DatabaseCore) -> AsyncGenerator[AsyncSession, Any]:
        async with database.session_factory()() as session:
            async with session.begin():
                yield session


class ConfigProvider(FastapiProvider):
    @provide(scope=Scope.APP)
    async def producer_settings(self) -> IProducerSettings:
        return ProducerSettings()

    @provide(scope=Scope.APP)
    async def consumer_settings(self) -> IConsumerSettings:
        return ConsumerSettings()

    @provide(scope=Scope.APP)
    async def secure_settings(self) -> SecureSettings:
        return SecureSettings()


class InfraProvider(FastapiProvider):
    @provide(scope=Scope.APP)
    async def cache(self) -> ICache:
        settings = RedisSettings()
        return RedisCache(url=settings.redis_url, prefix="api")

    @provide(scope=Scope.APP)
    async def producer(self, settings: IProducerSettings) -> IProducer:
        return KafkaAsyncProducer(settings)

    @provide(scope=Scope.APP)
    async def consumer(self, settings: IConsumerSettings) -> IConsumer:
        return KafkaAsyncConsumer(settings)

    @provide(scope=Scope.APP)
    async def tcp_connector(self) -> TCPConnector:
        return TCPConnector(limit=10, limit_per_host=2, ttl_dns_cache=300, enable_cleanup_closed=True)


class RepoProvider(FastapiProvider):
    @provide(scope=Scope.REQUEST)
    async def user_repo(self, session: AsyncSession) -> IUserRepo:
        return UserRepo(session=session)


class ServiceProvider(FastapiProvider):
    @provide(scope=Scope.REQUEST)
    async def user_context(self, request: Request) -> UserContext:
        """Адаптер между FastAPI и внутренним контекстом запроса."""
        return UserContext(user_id=request.state.user_id)

    @provide(scope=Scope.REQUEST)
    async def user_repo(self, session: AsyncSession) -> IUserRepo:
        return UserRepo(session=session)

    @provide(scope=Scope.REQUEST)
    async def device_repo(self, session: AsyncSession) -> IDeviceRepo:
        return DeviceRepo(session=session)

    @provide(scope=Scope.REQUEST)
    async def user_service(self, user_repo: IUserRepo, cache: ICache, auth_settings: SecureSettings) -> UserService:
        return UserService(user_repo=user_repo, cache=cache, auth_settings=auth_settings)

    @provide(scope=Scope.REQUEST)
    async def auth_service(self, user_repo: IUserRepo, cache: ICache, auth_settings: SecureSettings) -> AuthService:
        return AuthService(user_repo=user_repo, cache=cache, auth_settings=auth_settings)

    @provide(scope=Scope.REQUEST)
    async def auth_guard(self, request: Request, auth_service: AuthService) -> AuthUser:
        user = await auth_service.verify_request(request)
        auth_user = AuthUser(id=user.id, username=user.username, email=user.email, active=user.active)
        return auth_user

    @provide(scope=Scope.REQUEST)
    async def device_service(self, user_repo: IUserRepo, device_repo: IDeviceRepo, cache: ICache) -> DeviceService:
        return DeviceService(user_repo=user_repo, device_repo=device_repo, cache=cache)

    @provide(scope=Scope.APP)
    async def pandora_manager(self, tcp_connector: TCPConnector) -> PandoraClientManager:
        return PandoraClientManager(connector=tcp_connector)

    @provide(scope=Scope.REQUEST)
    async def pandora_client(
        self,
        pandora_client_manager: PandoraClientManager,
        user_context: UserContext,
        user_repo: IUserRepo,
    ) -> PandoraClient:
        return await pandora_client_manager.get_pandora_client(user_id=user_context.user_id, user_repo=user_repo)


def create_container() -> AsyncContainer:
    container = make_async_container(ConfigProvider(), DatabaseProvider(), InfraProvider(), ServiceProvider())
    return container
