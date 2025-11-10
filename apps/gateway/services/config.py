from apps.common.core.protocols.repository import IConfigRepo, IUserRepo
from apps.common.dao.config import PandoraConfig, PandoraCredDomain, PandoraCredIn


class ConfigService:
    def __init__(self, user_repo: IUserRepo, config_repo: IConfigRepo) -> None:
        self.user_repo = user_repo
        self.config_repo = config_repo

    async def upsert_pandora_cred(self, pandora_in: PandoraCredIn) -> PandoraCredDomain:
        return await self.config_repo.upsert_pandora_credentials(pandora_cred=pandora_in)

    async def get_pandora_config(self, user_id: int) -> PandoraConfig | None:
        pandora = await self.config_repo.get_pandora_credentials(user_id=user_id)
        if not pandora:
            return None
        return PandoraConfig(credentials=pandora)

    async def get_pandora_cred(self, user_id: int) -> PandoraCredDomain:
        pandora = await self.config_repo.get_pandora_credentials(user_id=user_id)
        if not pandora:
            return PandoraCredDomain(id=None, user_id=user_id)
        return pandora