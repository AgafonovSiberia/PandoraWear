
from apps.common.const import ServiceName
from apps.common.core.protocols.cache import ICache
from apps.common.core.protocols.repository import IConfigRepo, IUserRepo
from apps.common.dao.config import ConfigDomain, ConfigIn, PandoraCredDomain, PandoraCredIn


class ConfigService:
    PANDORA_CACHE_PREFIX = "pandora_cred:"
    def __init__(self, user_repo: IUserRepo, config_repo: IConfigRepo, cache: ICache) -> None:
        self.user_repo = user_repo
        self.config_repo = config_repo
        self.cache: ICache = cache


    def _get_pandora_cache_key(self, user_id: int) -> str:
        return f"{self.PANDORA_CACHE_PREFIX}{user_id}"

    async def save_pandora_cred(self, user_id: int, pandora_cred_in: PandoraCredIn) -> PandoraCredDomain:
        config_in = ConfigIn(
            user_id=user_id,
            service=ServiceName.PANDORA,
            creds={"email": pandora_cred_in.email, "password": pandora_cred_in.password}
        )
        config_out = await self.config_repo.upsert_config(config=config_in)
        if not config_out:
            return PandoraCredDomain()
        
        await self.cache.set_json(key=self._get_pandora_cache_key(user_id=user_id), data=config_out.creds)
        return PandoraCredDomain.model_validate(config_out.creds)

    async def get_pandora_config(self, user_id: int,) -> ConfigDomain | None:
        config = await self.config_repo.get_config(user_id=user_id, service=ServiceName.PANDORA)
        if not config:
            return None

        return ConfigDomain.model_validate(config)

    async def get_pandora_cred(self, user_id: int) -> PandoraCredDomain:
        pandora_cred_raw = await self.cache.get_json(self._get_pandora_cache_key(user_id=user_id))
        if pandora_cred_raw:
            return PandoraCredDomain.model_validate(pandora_cred_raw)

        config = await self.config_repo.get_config(user_id=user_id, service=ServiceName.PANDORA)
        if not config:
            return PandoraCredDomain()
        await self.cache.set_json(key=self._get_pandora_cache_key(user_id=user_id),data=config.creds)
        return PandoraCredDomain.model_validate(config.creds)