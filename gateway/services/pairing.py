import random
import string
from datetime import datetime, timedelta, UTC
from uuid import uuid4, UUID

from gateway.core.models import CreatedCode, BindedDevice
from gateway.core.protocols import PairingServicePort, ErrInvalidCode
from gateway.infrastructure.redis import RedisCache

PAIR_CODE_LENGTH = 6
PAIR_CODE_TTL = 300
DEVICE_TOKEN_TTL = 60 * 60 * 24 * 365


class PairingService(PairingServicePort):
    """Создание и активация кодов привязки устройств."""

    def __init__(self, cache: RedisCache):
        self._cache = cache

    @staticmethod
    def _get_cache_key(code: str) -> str:
        return f"pair_{code}"

    @staticmethod
    def _generate_random_code() -> str:
        return "".join(random.choices(string.digits, k=PAIR_CODE_LENGTH))

    @staticmethod
    def _generate_random_token() -> str:
        return str(uuid4().hex)

    async def create_code(self, user_id: UUID) -> CreatedCode:
        code = self._generate_random_code()
        await self._cache.set(
            self._get_cache_key(code=code), str(user_id), expire_ttl=PAIR_CODE_TTL
        )
        return CreatedCode(
            code=code, expire_dt=datetime.now(UTC) + timedelta(seconds=PAIR_CODE_TTL)
        )

    async def bind_device(self, code: str, device_name: str) -> BindedDevice:
        key = self._get_cache_key(code=code)
        if not (user_id := await self._cache.get(key)):
            raise ErrInvalidCode()

        await self._cache.delete(key)

        device_id, token = uuid4(), self._generate_random_token()

        await self._cache.set_json(
            f"device:{device_id}",
            {"user": user_id, "name": device_name, "token": token},
            expire_ttl=DEVICE_TOKEN_TTL,
        )

        return BindedDevice(
            device_id=device_id,
            user_id=user_id,
            token=token,
            expire_dt=datetime.now(UTC) + timedelta(seconds=DEVICE_TOKEN_TTL),
        )
