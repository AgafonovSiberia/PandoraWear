import os
from typing import Any, AsyncGenerator, Iterator
from urllib.parse import urlparse

import httpx
import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import create_engine, text
from testcontainers.core.wait_strategies import LogMessageWaitStrategy
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from apps.gateway.main import create_app

os.environ.setdefault("TESTCONTAINERS_RYUK_DISABLED", "true")
API_BASE_URL = "http://test"
POSTGRES_PORT = 5432
REDIS_PORT = 6379


# @pytest.fixture(scope="session")
# def event_loop():
#     loop = asyncio.new_event_loop()
#     yield loop
#     loop.close()

def _make_asyncpg_url(sync_url: str) -> str:
    parsed = urlparse(sync_url)
    return f"postgresql+asyncpg://{parsed.username}:{parsed.password}@{parsed.hostname}:{parsed.port}{parsed.path}"


def _run_migrations(sync_url: str) -> None:
    from alembic import command
    from alembic.config import Config

    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", sync_url)
    command.upgrade(cfg, "head")


@pytest.fixture(scope="session")
def _infrastructure() -> Iterator[dict]:
    with PostgresContainer("postgres:16") as pg, RedisContainer("redis:7") as redis:
        pg_host, pg_port = pg.get_container_host_ip(), int(pg.get_exposed_port(POSTGRES_PORT))
        pg.waiting_for(LogMessageWaitStrategy('ready to accept connections'))

        pg_sync_url = f"postgresql+psycopg://{pg.username}:{pg.password}@{pg_host}:{pg_port}/{pg.dbname}"
        async_url = _make_asyncpg_url(pg_sync_url)

        parsed = urlparse(pg_sync_url)
        db_name = parsed.path.lstrip("/") or pg.dbname

        os.environ["DB_URL"] = async_url
        os.environ["POSTGRES_HOST"] = parsed.hostname or "localhost"
        os.environ["POSTGRES_PORT"] = str(parsed.port or POSTGRES_PORT)
        os.environ["POSTGRES_USER"] = parsed.username or pg.username
        os.environ["POSTGRES_PASSWORD"] = parsed.password or pg.password
        os.environ["POSTGRES_DB"] = db_name

        redis_host, redis_port = redis.get_container_host_ip(), int(redis.get_exposed_port(REDIS_PORT))
        pg.waiting_for(LogMessageWaitStrategy('ready'))

        redis_url = f"redis://{redis_host}:{redis_port}/0"
        os.environ["REDIS_URL"] = redis_url

        os.environ.setdefault("SECURE_SECRET_KEY", "integration-secret-key")
        os.environ.setdefault("SECURE_JWT_TTL", "3600")
        os.environ.setdefault("ENV", "test")

        _run_migrations(pg_sync_url)

        yield {
            "pg_sync_url": pg_sync_url,
            "redis_url": redis_url,
        }


@pytest.fixture(scope="function")
def app(_infrastructure: dict) -> FastAPI:  # noqa: ARG001
    return create_app()


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, Any]:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport,
        base_url=API_BASE_URL,
        timeout=10.0,
    ) as client:
        yield client


@pytest.fixture(autouse=True)
def clean_users(_infrastructure: dict):
    engine = create_engine(_infrastructure["pg_sync_url"])
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
    yield
