from apps.gateway.services.pandora.session import PandoraSession
from common.infrastructure.repository.user import UserRepo


class PandoraSessionManager:
    def __init__(self, user_repository: UserRepo):
        self._sessions: dict[int, PandoraSession] = {}
        self._user_repository = user_repository

    def get_session(self, user_id: int) -> PandoraSession: ...

    def _save_session(self, user_id: int, session: PandoraSession) -> None:
        self._sessions.update({user_id: session})
