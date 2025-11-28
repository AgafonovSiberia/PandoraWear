import jwt
from fastapi import HTTPException, Request, status

from apps.common.config import SecureSettings
from apps.common.core.protocols.cache import ICache
from apps.common.core.protocols.repository import IUserRepo
from apps.gateway.auth.token import decode_jwt


class AuthService:
    def __init__(self, user_repo: IUserRepo, cache: ICache, auth_settings: SecureSettings):
        self.user_repo = user_repo
        self.cache = cache
        self.settings = auth_settings

    async def verify_request(self, request: Request) -> tuple[str, int]:
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="MISSING_TOKEN")

        cleaned_token = token.removeprefix("Bearer ").strip()
        if not cleaned_token:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="NO_TOKEN")

        if not await self.cache.get(cleaned_token):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="TOKEN_EXPIRED")

        try:
            payload = decode_jwt(token=cleaned_token, secret=self.settings.SECRET_KEY)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="TOKEN_EXPIRED")
        except jwt.InvalidTokenError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="INVALID_TOKEN")

        iss = payload.get("iss")
        if not iss:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="INVALID_PAYLOAD")

        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="INVALID_PAYLOAD")

        return token, user_id
