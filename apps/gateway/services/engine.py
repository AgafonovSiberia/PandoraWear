from apps.common.core.protocols.repository import IUserRepo
from apps.gateway.services.pandora.client import PandoraClient


class EngineService:
    def __init__(self, user_repo: IUserRepo, pandora_client: PandoraClient):
        self._pandora = pandora_client
        self._user_repo = user_repo

