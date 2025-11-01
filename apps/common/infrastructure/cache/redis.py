import json

import redis.asyncio as redis

from apps.common.core.protocols.cache import ICache


class RedisCache(ICache):
    def __init__(self, url: str, prefix: str):
        self._redis = redis.from_url(url, decode_responses=True)
        self._prefix = prefix

    def get_key(self, key: str) -> str:
        return f"{self._prefix}:{key}"

    async def get(self, key: str):
        return await self._redis.get(self.get_key(key))

    async def set(self, key: str, value, ttl: int | None = None):
        await self._redis.set(self.get_key(key), value, ex=ttl)

    async def delete(self, key: str):
        await self._redis.delete(self.get_key(key))

    async def keys(self, pattern: str):
        return await self._redis.keys(pattern)

    async def get_json(self, key: str):
        if raw := await self._redis.get(self.get_key(key)):
            try:
                return json.loads(raw)
            except Exception:
                return None
        return None

    async def set_json(self, key: str, data, ttl: int | None = None):
        await self._redis.set(self.get_key(key), json.dumps(data), ex=ttl)
