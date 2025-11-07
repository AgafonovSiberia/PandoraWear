from fastapi import HTTPException, status

from apps.common.config import SecureSettings
from apps.common.core.protocols.cache import ICache
from apps.common.core.protocols.repository import IUserRepo
from apps.common.dao.user import CreateUser, UserDomain, UserInLogin, UserInRegister
from apps.gateway.auth.crypto import check_hashed_value, hash_value
from apps.gateway.auth.token import generate_jwt


class UserService:
    def __init__(self, user_repo: IUserRepo, cache: ICache, auth_settings: SecureSettings) -> None:
        self.user_repo = user_repo
        self.cache = cache
        self.auth_settings = auth_settings

    async def register(self, user_in: UserInRegister) -> UserDomain:
        user = await self.user_repo.get_by_email(email=user_in.email)
        if user is not None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="USER_ALREADY_EXISTS")

        new_user = CreateUser(
            username=user_in.username,
            email=user_in.email,
            password_hash=hash_value(user_in.password),
        )
        user = await self.user_repo.create(user_in=new_user)
        return user

    async def login(self, user_in: UserInLogin) -> str:
        user = await self.user_repo.get_by_email(email=user_in.email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="USER_NOT_FOUND")

        if not check_hashed_value(password=user_in.password, hash_password=user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID_CREDENTIALS")

        token = generate_jwt(payload={"user_id": user.id}, secret=self.auth_settings.SECRET_KEY)
        await self.cache.set_json(key=str(token), data={"user_id": user.id}, ttl=self.auth_settings.JWT_TTL)
        return token

    async def logout(self, user_id: int, token: str):
        user = await self.user_repo.get(user_id=user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="USER_NOT_FOUND")

        await self.cache.delete(token)


    async def set_pandora_credentials(self, user_id: int, login: str, password: str) -> None: ...

    async def get_user(self, email: str) -> UserDomain | None:
        return await self.user_repo.get_by_email(email=email)
