from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.const import ServiceName
from apps.common.core.protocols.repository import IConfigRepo
from apps.common.dao.config import PandoraCredDomain, PandoraCredIn
from apps.common.infrastructure.database.models.credentials import Credential


class ConfigRepo(IConfigRepo):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_pandora_credentials(self, pandora_cred: PandoraCredIn) -> PandoraCredDomain:
        result = await self._session.scalar(
            insert(Credential)
            .values(**pandora_cred.model_dump(exclude={"id"}, exclude_none=True))
            .on_conflict_do_update(
                index_elements=[Credential.id],
                set_=pandora_cred.model_dump(exclude_unset=True),
            )
            .returning(Credential)
        )
        await self._session.flush()
        await self._session.refresh(result)

        return PandoraCredDomain.model_validate(result)

    async def get_pandora_credentials(self, user_id: int) -> PandoraCredDomain | None:
        res = await self._session.execute(
            select(Credential).where(Credential.user_id == user_id, Credential.service == ServiceName.PANDORA)
        )
        cred = res.scalar_one_or_none()
        if not cred:
            return None

        return PandoraCredDomain.model_validate(**cred.creds) if cred and cred.creds else None
