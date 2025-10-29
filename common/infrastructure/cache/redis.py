import json

import redis.asyncio as redis

from common.core.protocols.icache import ICache


class RedisCache(ICache):
    def __init__(self, url: str, prefix: str):
        self._redis = redis.from_url(url, decode_responses=True)
        self._prefix = prefix

    async def get(self, key: str):
        return await self._redis.get(key)

    async def set(self, key: str, value, expire_ms: int | None = None):
        await self._redis.set(key, value, ex=expire_ms)

    async def delete(self, key: str):
        await self._redis.delete(key)

    async def keys(self, pattern: str):
        return await self._redis.keys(pattern)

    async def get_json(self, key: str):
        if raw := await self._redis.get(key):
            try:
                return json.loads(raw)
            except Exception:
                return None
        return None

    async def set_json(self, key: str, data, expire_ms: int | None = None):
        await self._redis.set(key, json.dumps(data), ex=expire_ms)
