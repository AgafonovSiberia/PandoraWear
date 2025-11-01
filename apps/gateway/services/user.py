from fastapi import HTTPException

from apps.common.config import AuthSettings
from apps.common.core.protocols.cache import ICache
from apps.common.core.protocols.repository import IUserRepo
from apps.common.dao.user import UserIn, UserDomain, CreateUser
from apps.gateway.auth.crypto import crypt_password
from apps.gateway.auth.token import generate_jwt


class UserService:
    def __init__(
        self, user_repo: IUserRepo, cache: ICache, auth_settings: AuthSettings
    ) -> None:
        self.user_repo = user_repo
        self.cache = cache
        self.auth_settings = auth_settings

    async def register(self, user_in: UserIn) -> str:
        new_user = CreateUser(
            username=user_in.username,
            email=user_in.email,
            password_hash=crypt_password(user_in.password),
        )
        user = await self.user_repo.create(user_in=new_user)
        if user is None:
            raise HTTPException(status_code=400, detail="Registration error")

        return generate_jwt(
            payload={"user_id": user.id}, secret=self.auth_settings.secret_key
        )

    async def login(self, user_in: UserIn) -> str:
        user = await self.user_repo.get_by_email(email=user_in.email)
        if user is None:
            raise HTTPException(status_code=400, detail="Login error")
        password_hash_in = crypt_password(user_in.password)

        if user.password_hash != password_hash_in:
            raise HTTPException(status_code=400, detail="Login error")

        return generate_jwt(
            payload={"user_id": user.id}, secret=self.auth_settings.secret_key
        )

    async def set_pandora_credentials(
        self, user_id: int, login: str, password: str
    ) -> None: ...

    async def get_user(self, email: str) -> UserDomain | None:
        return await self.user_repo.get_by_email(email=email)
