import random
import uuid
from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe

from fastapi import HTTPException, Request, status

from apps.common.core.protocols.cache import ICache
from apps.common.core.protocols.repository import IDeviceRepo, IUserRepo
from apps.common.dao.device import DeviceDomain, DeviceIn, DevicePairDataOut
from apps.gateway.auth.crypto import hash_value

TOKEN_LEN = 32
TOKEN_TTL = timedelta(days=60)
TOKEN_CACHE_TTL_SECONDS = 60 * 30
PAIR_CODE_TTL_SECONDS = 60


class DeviceService:
    def __init__(self, user_repo: IUserRepo, device_repo: IDeviceRepo, cache: ICache):
        self.user_repo = user_repo
        self.device_repo = device_repo
        self.cache = cache

    async def get_all(self, user_id: int) -> list[DeviceDomain]:
        return await self.device_repo.get_all_devices(user_id=user_id)

    @staticmethod
    def _generate_code():
        return f"{random.randint(0, 999999):06d}"

    @staticmethod
    def _generate_token() -> str:
        return token_urlsafe(nbytes=TOKEN_LEN)

    @staticmethod
    def pair_code_key(code: str) -> str:
        return f"pair:{code}"

    @staticmethod
    def device_key(device_id: uuid.UUID | str) -> str:
        return f"device:{str(device_id)}"

    async def generate_pair_code(self, user_id: int, device_name: str) -> str:
        device = await self.device_repo.get_by_name(device_name=device_name)
        if device is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="DEVICE_ALREADY_EXISTS",
            )

        code = self._generate_code()
        data = {"user_id": user_id, "device_name": device_name}
        await self.cache.set_json(key=self.pair_code_key(code=code), data=data, ttl=PAIR_CODE_TTL_SECONDS)
        return code

    async def pair(self, pair_code: str) -> DevicePairDataOut:
        data = await self.cache.get_json(key=self.pair_code_key(code=pair_code))
        if not data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INVALID_CODE")

        raw_token = self._generate_token()
        token_hashed = hash_value(raw_token)
        user_id, device_name = data.get("user_id"), data.get("device_name")

        device_in = DeviceIn(
            name=device_name,
            token_hash=token_hashed,
            user_id=user_id,
            expires_at=datetime.now(UTC) + TOKEN_TTL,
            last_rotated_at=datetime.now(UTC),
        )
        device = await self.device_repo.upsert_device(device_in)
        await self.cache.set(key=self.device_key(device.id), value=str(token_hashed), ttl=TOKEN_CACHE_TTL_SECONDS)
        return DevicePairDataOut(device_id=device.id, token=raw_token)

    async def device_revoke(self, device_id: uuid.UUID | str):
        await self.cache.delete(key=str(device_id))
        await self.device_repo.delete_device(device_id)

    async def process_token(self, device_id: uuid.UUID | str, token: str) -> DeviceDomain:
        from_cache = await self.cache.get(key=self.device_key(device_id))
        if from_cache and from_cache == token:
            return await self.device_repo.get(device_id=device_id)
        device = await self.device_repo.get(device_id=device_id)
        if not device:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="TOKEN_EXPIRED")

        if device.token_hash != token:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="TOKEN_EXPIRED")

        # Пока что просто продлеваем токен сами
        await self.cache.set(self.device_key(device.id), str(device.token_hash), ttl=TOKEN_CACHE_TTL_SECONDS)
        return device

    async def verify_request(self, request: Request) -> DeviceDomain:
        device_id, token = request.cookies.get("device_id"), request.cookies.get("token")
        return await self.process_token(device_id=device_id, token=token)
