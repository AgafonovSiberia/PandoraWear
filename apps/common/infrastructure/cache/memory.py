import json
from datetime import datetime, timedelta, UTC
from typing import Optional, Any

from apps.common.core.protocols.cache import ICache


class MemoryCache(ICache):
    def __init__(self):
        self._store: dict[str, tuple[str, datetime | None]] = {}

    async def get(self, key: str) -> str | tuple[Any, datetime] | None:
        entry = self._store.get(key)
        if not entry:
            return None
        value, expire_at = entry
        if expire_at and datetime.now(UTC) > expire_at:
            self._store.pop(key, None)
            return None
        return value

    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        expire_at = datetime.now(UTC) + timedelta(seconds=ttl) if ttl else None
        self._store[key] = (str(value), expire_at)

    async def delete(self, key: str) -> None:
        self._store.pop(key, None)

    async def keys(self, pattern: str) -> list[str]:
        return list(self._store.keys())

    async def get_json(self, key: str) -> Optional[dict]:
        raw = await self.get(key)
        return json.loads(raw) if raw else None

    async def set_json(self, key: str, data: dict, ttl: int = None) -> None:
        await self.set(key, json.dumps(data), ttl=ttl)
