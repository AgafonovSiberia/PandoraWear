from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.core.protocols.repository import IUserRepo
from apps.common.dao.user import CreateUser, PandoraCredDomain, PandoraCredIn, UserDomain
from apps.common.infrastructure.database.models.credentials import Credential
from apps.common.infrastructure.database.models.user import User


class UserRepo(IUserRepo):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_email(self, email: str) -> UserDomain | None:
        res = await self._session.execute(select(User).where(User.email == email))
        user = res.scalar_one_or_none()
        return UserDomain.model_validate(user) if user else None

    async def create(self, user_in: CreateUser) -> UserDomain | None:
        user = User(**user_in.model_dump())
        self._session.add(user)
        await self._session.flush()
        await self._session.refresh(user)
        await self._session.commit()
        return UserDomain.model_validate(user) if user else None

    async def get(self, user_id: int) -> UserDomain:
        res = await self._session.execute(select(User).where(User.id == user_id))
        user = res.scalar_one_or_none()
        return UserDomain.model_validate(user) if user else None

    async def delete(self, user_id: int) -> None:
        user = await self._session.get(User, user_id)
        user.is_active = False
        self._session.add(user)

    async def upsert_credentials(self, pandora_cred: PandoraCredIn) -> None:
        cred = await self._session.get(Credential, pandora_cred.user_id)
        cred.pandora_login = pandora_cred.login
        cred.pandora_password = pandora_cred.password
        self._session.add(cred)

    async def get_credentials(self, user_id: int) -> PandoraCredDomain:
        cred = await self._session.get(Credential, user_id)
        return PandoraCredDomain.model_validate(cred) if cred else None
