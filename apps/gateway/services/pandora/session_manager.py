import asyncio

from aiohttp import TCPConnector

from apps.common.core.protocols.repository import IUserRepo
from apps.gateway.services.pandora.client import PandoraClient
from apps.gateway.services.pandora.session import PandoraSession

MAX_SESSION = 4
GARBAGE_COLLECT_INTERVAL = 60 * 60


class PandoraClientManager:
    def __init__(
        self,
        connector: TCPConnector,
    ) -> None:
        self._connector: TCPConnector = connector
        self._sessions: dict[str, PandoraSession] = {}
        self._garbage_session_collector_task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        if self._garbage_session_collector_task is not None:
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
        for session in self._sessions.values():
            await session.close()
        self._sessions.clear()

    async def _get_session_id_by_user(self, user_id: int, user_repo: IUserRepo) -> str | None:
        user = await user_repo.get(user_id=user_id)
        if not user:
            return None
        return user.session_id

    async def get_or_create_session(self, user_id: int, user_repo: IUserRepo) -> PandoraSession:
        session_id = await self._get_session_id_by_user(user_id=user_id, user_repo=IUserRepo)
        if not session_id:
            return await self._create_session(user_id=user_id, user_repo=user_repo)
        session = self._sessions.get(session_id, None)
        if not session:
            return await self._create_session(user_id=user_id, user_repo=user_repo)
        return session

    async def _create_session(self, user_id: int, user_repo: IUserRepo) -> PandoraSession:
        cred = await user_repo.get_credentials(user_id=user_id)
        session = PandoraSession(connector=self._connector, cred=cred)
        await session.login()
        session_id = str(session.session_id)

        self._sessions[session_id] = session
        # await user_repo.save_pandora_session(
        #     session=SessionIn(
        #         user_id=user_id,
        #         pandora_user_id=session.user_id,
        #         pandora_session_id=session_id,
        #     )
        # )
        return self._sessions.get(session_id, None)

    async def get_pandora_client(self, user_id: int, user_repo: IUserRepo) -> PandoraClient:
        session = await self.get_or_create_session(user_id=user_id, user_repo=user_repo)
        return PandoraClient(session=session)
