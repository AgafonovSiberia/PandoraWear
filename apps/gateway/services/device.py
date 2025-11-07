import random
import uuid
from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe

from fastapi import HTTPException, status

from apps.common.core.protocols.cache import ICache
from apps.common.core.protocols.repository import IDeviceRepo, IUserRepo
from apps.common.dao.device import DeviceDomain, DeviceIn, DevicePairDataIn, DevicePairDataOut
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

    async def generate_pair_code(self, user_id: int, device_name: str) -> str:
        device = await self.device_repo.get_by_name(device_name=device_name)
        if device is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="DEVICE_ALREADY_EXISTS",
            )

        code = self._generate_code()
        data = {"user_id": user_id, "device_name": device_name}
        await self.cache.set_json(key=code, data=data, ttl=PAIR_CODE_TTL_SECONDS)
        return code

    async def pair(self, device_pair: DevicePairDataIn) -> DevicePairDataOut:
        data = await self.cache.get_json(key=device_pair.code)
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
        await self.cache.set(key=str(device.id), value=str(token_hashed), ttl=TOKEN_CACHE_TTL_SECONDS)
        return DevicePairDataOut(device_id=device.id, token=raw_token)


    async def device_revoke(self, device_id: uuid.UUID | str):
        await self.cache.delete(key=str(device_id))
        await self.device_repo.delete_device(device_id)
