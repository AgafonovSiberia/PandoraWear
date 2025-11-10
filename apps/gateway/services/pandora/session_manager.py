import asyncio

from aiohttp import TCPConnector

from apps.common.core.protocols.cache import ICache
from apps.common.core.protocols.repository import IConfigRepo
from apps.common.dao.device import AuthDevice
from apps.gateway.services.pandora.client import PandoraClient
from apps.gateway.services.pandora.session import PandoraSession

MAX_SESSION = 4
GARBAGE_COLLECT_INTERVAL = 60 * 60 * 2


class PandoraClientManager:
    def __init__(self, connector: TCPConnector, cache: ICache) -> None:
        self._connector: TCPConnector = connector
        self._sessions: dict[int, PandoraSession] = {}
        self._garbage_session_collector_task: asyncio.Task[None] | None = None
        self._cache: ICache = cache

    async def start(self) -> None:
        if self._garbage_session_collector_task is None:
            self._garbage_session_collector_task = asyncio.create_task(self._garbage_session_collect())

    async def _garbage_session_collect(self) -> None:
        try:
            while True:
                await asyncio.sleep(GARBAGE_COLLECT_INTERVAL)
                expired_sessions = [user_id for user_id, session in self._sessions.items() if session.is_expired]
                for user_id in expired_sessions:
                    session = self._sessions.pop(user_id, None)
                    if not session:
                        continue
                    await session.close()
        except asyncio.CancelledError:
            return

    async def stop(self) -> None:
        if self._garbage_session_collector_task:
            self._garbage_session_collector_task.cancel()
            try:
                await self._garbage_session_collector_task
            except asyncio.CancelledError:
                pass
            self._garbage_session_collector_task = None

        for session in self._sessions.values():
            await session.close()
        self._sessions.clear()

    async def get_or_create_session(self, user_id: int, config_repo: IConfigRepo) -> PandoraSession:
        session = self._sessions.get(user_id)
        if session:
            return session
        return await self._create_session(user_id=user_id, config_repo=config_repo)

    async def _create_session(self, user_id: int, config_repo: IConfigRepo) -> PandoraSession:
        cred = await config_repo.get_pandora_credentials(user_id=user_id)
        session = PandoraSession(connector=self._connector, cred=cred)
        await session.login()
        self._sessions[user_id] = session
        return session

    async def get_pandora_client(self, auth_device: AuthDevice, config_repo: IConfigRepo) -> PandoraClient:
        session = await self.get_or_create_session(user_id=auth_device.user_id, config_repo=config_repo)
        return PandoraClient(session=session)
