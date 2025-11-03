import jwt
from fastapi import HTTPException, Request, status

from apps.common.config import AuthSettings
from apps.common.core.protocols.cache import ICache
from apps.common.core.protocols.repository import IUserRepo
from apps.common.dao.user import UserDomain
from apps.gateway.auth.token import decode_jwt


class AuthService:
    def __init__(self, user_repo: IUserRepo, cache: ICache, auth_settings: AuthSettings):
        self.user_repo = user_repo
        self.cache = cache
        self.settings = auth_settings

    async def verify_request(self, request: Request) -> UserDomain:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="NO_TOKEN")

        try:
            payload = decode_jwt(token=token, secret=self.settings.secret_key)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="TOKEN_EXPIRED")
        except jwt.InvalidTokenError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="INVALID_TOKEN")

        iss = payload.get("iss")
        if not iss:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="INVALID_PAYLOAD")

        user = await self.user_repo.get(user_id=payload.get("user_id"))
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="USER_NOT_FOUND")

        return user