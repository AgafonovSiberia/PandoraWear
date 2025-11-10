from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.core.protocols.repository import IUserRepo
from apps.common.dao.user import CreateUser, UserDomain
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
        return UserDomain.model_validate(user) if user else None

    async def get(self, user_id: int) -> UserDomain:
        res = await self._session.execute(select(User).where(User.id == user_id))
        user = res.scalar_one_or_none()
        return UserDomain.model_validate(user) if user else None

    async def delete(self, user_id: int) -> None:
        user = await self._session.get(User, user_id)
        if not user:
            return
        user.active = False
        self._session.add(user)


