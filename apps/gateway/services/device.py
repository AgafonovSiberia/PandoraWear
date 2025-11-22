import random
import uuid
from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe

from fastapi import HTTPException, Request, status

from apps.common.core.protocols.cache import ICache
from apps.common.core.protocols.repository import IDeviceRepo, IUserRepo
from apps.common.dao.device import DeviceDomain, DeviceIn, DevicePairDataOut, DeviceUpdate
from apps.common.dao.user import ConfirmDeviceIn
from apps.gateway.auth.crypto import check_hashed_value, hash_value

TOKEN_LEN = 32
TOKEN_TTL = timedelta(days=60)
TOKEN_CACHE_TTL_SECONDS = 60 * 60 * 2
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

    async def pair_by_cred(self, confirm_in: ConfirmDeviceIn):
        if not confirm_in.device_name:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UNDEFINED_DEVICE_NAME")

        user = await self.user_repo.get_by_email(email=confirm_in.email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="USER_NOT_FOUND")

        if not check_hashed_value(value=confirm_in.password, hashed_value=user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID_CREDENTIALS")

        return await self._pair_device(device_name=confirm_in.device_name, user_id=user.id)

    async def _pair_device(self, device_name: str, user_id: int) -> DevicePairDataOut:
        raw_token = self._generate_token()
        token_hashed = hash_value(raw_token)
        device_in = DeviceIn(
            name=device_name,
            token_hash=token_hashed,
            user_id=user_id,
            expires_at=datetime.now(UTC) + TOKEN_TTL,
            last_rotated_at=datetime.now(UTC),
        )
        device = await self.device_repo.upsert_device(device_in)
        await self.cache.set(
            key=self.device_key(device.id), value=token_hashed.decode(encoding="utf-8"), ttl=TOKEN_CACHE_TTL_SECONDS
        )
        return DevicePairDataOut(device_id=str(device.id), token=raw_token)

    async def pair_by_code(self, pair_code: str) -> DevicePairDataOut:
        data = await self.cache.get_json(key=self.pair_code_key(code=pair_code))
        if not data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INVALID_CODE")

        user_id, device_name = data.get("user_id"), data.get("device_name")
        return await self._pair_device(device_name=device_name, user_id=user_id)

    async def device_revoke(self, device_id: uuid.UUID | str):
        await self.cache.delete(key=str(device_id))
        await self.device_repo.delete_device(device_id)

    async def process_token(self, device_id: uuid.UUID | str, token: str) -> DeviceDomain:
        from_cache = await self.cache.get(key=self.device_key(device_id))
        if from_cache and check_hashed_value(value=token, hashed_value=from_cache.encode(encoding="utf-8")):
            device = await self.device_repo.get(device_id=device_id)
            device_update = DeviceUpdate(
                id=device.id,
                last_used_at=datetime.now(UTC),
            )
            updated_device = await self.device_repo.update_device(device_update=device_update)
            return updated_device
        
        device = await self.device_repo.get(device_id=device_id)
        if not device:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="TOKEN_EXPIRED")

        if device.token_hash != token:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="TOKEN_EXPIRED")

        # Пока что просто продлеваем токен сами
        await self.cache.set(self.device_key(device.id), str(device.token_hash), ttl=TOKEN_CACHE_TTL_SECONDS)
        device_update = DeviceUpdate(
            id=device.id,
            last_rotated_at=datetime.now(UTC),
            last_used_at=datetime.now(UTC),
        )
        updated_device = await self.device_repo.update_device(device_update=device_update)
        return updated_device

    async def verify_request(self, request: Request) -> DeviceDomain:
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing token")

        cleaned_token = token.removeprefix("Bearer ").strip()
        device_id = request.cookies.get("device_id")
        if not device_id:
            raise HTTPException(status_code=401, detail="Missing device_id")

        return await self.process_token(device_id=device_id, token=cleaned_token)
