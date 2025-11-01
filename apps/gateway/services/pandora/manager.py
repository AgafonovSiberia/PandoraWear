from apps.common.core.protocols.repository import IUserRepo

from apps.gateway.services.pandora.session import PandoraSession


class PandoraSessionManager:
    def __init__(self, user_repository: IUserRepo):
        self._sessions: dict[int, PandoraSession] = {}
        self._user_repository = user_repository

    def get_session(self, user_id: int) -> PandoraSession: ...

    def _save_session(self, user_id: int, session: PandoraSession) -> None:
        self._sessions.update({user_id: session})
