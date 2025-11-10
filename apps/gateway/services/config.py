
from apps.common.const import ServiceName
from apps.common.core.protocols.repository import IConfigRepo, IUserRepo
from apps.common.dao.config import ConfigDomain, ConfigIn, PandoraCredDomain, PandoraCredIn


class ConfigService:
    def __init__(self, user_repo: IUserRepo, config_repo: IConfigRepo) -> None:
        self.user_repo = user_repo
        self.config_repo = config_repo

    async def save_pandora_cred(self, user_id: int, pandora_cred_in: PandoraCredIn) -> PandoraCredDomain:
        config_in = ConfigIn(
            user_id=user_id,
            service=ServiceName.PANDORA,
            creds={"email": pandora_cred_in.email, "password": pandora_cred_in.password}
        )
        config_out = await self.config_repo.upsert_config(config=config_in)
        if not config_out:
            return PandoraCredDomain()
        return PandoraCredDomain.model_validate(config_out.creds)

    async def get_pandora_config(self, user_id: int,) -> ConfigDomain | None:
        config = await self.config_repo.get_config(user_id=user_id, service=ServiceName.PANDORA)
        if not config:
            return None

        return ConfigDomain.model_validate(config)

    async def get_pandora_cred(self, user_id: int) -> PandoraCredDomain:
        config = await self.config_repo.get_config(user_id=user_id, service=ServiceName.PANDORA)
        if not config:
            return PandoraCredDomain()

        return PandoraCredDomain.model_validate(config.creds)