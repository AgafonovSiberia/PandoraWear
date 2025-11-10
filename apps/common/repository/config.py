from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.const import ServiceName
from apps.common.core.protocols.repository import IConfigRepo
from apps.common.dao.config import ConfigIn
from apps.common.infrastructure.database.models.credentials import Credential


class ConfigRepo(IConfigRepo):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def upsert_config(self, config: ConfigIn) -> Credential | None:
        result = await self._session.scalar(
            insert(Credential)
            .values(**config.model_dump(exclude={"id"}, exclude_none=True))
            .on_conflict_do_update(
                index_elements=[Credential.service, Credential.user_id],
                set_={"creds": config.creds},
            )
            .returning(Credential)
        )
        await self._session.flush()
        await self._session.refresh(result)
        return result


    async def get_config(self, user_id: int, service: ServiceName | str) -> Credential | None:
        res = await self._session.execute(
            select(Credential).where(Credential.user_id == user_id, Credential.service == service)
        )
        return res.scalar_one_or_none()