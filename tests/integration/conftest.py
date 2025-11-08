import os
import socket
import time
from typing import Iterator
from urllib.parse import urlparse

import httpx
import pytest
import pytest_asyncio
from fastapi import FastAPI
from sqlalchemy import create_engine, text
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

from apps.gateway.main import create_app

# ВАЖНО: отключаем Ryuk до любого использования testcontainers
os.environ.setdefault("TESTCONTAINERS_RYUK_DISABLED", "true")

API_BASE_URL = "http://test"


def _wait_for_port(host: str, port: int, timeout: float = 60.0) -> None:
    deadline = time.time() + timeout
    last_err: Exception | None = None

    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=2.0):
                return
        except OSError as exc:
            last_err = exc
            time.sleep(0.5)

    raise RuntimeError(f"Service on {host}:{port} not ready: {last_err!r}")


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
        # Postgres
        pg_host = pg.get_container_host_ip()
        pg_port = int(pg.get_exposed_port(5432))
        _wait_for_port(pg_host, pg_port)

        pg_sync_url = f"postgresql+psycopg://{pg.username}:{pg.password}@{pg_host}:{pg_port}/{pg.dbname}"
        async_url = _make_asyncpg_url(pg_sync_url)

        parsed = urlparse(pg_sync_url)
        db_name = parsed.path.lstrip("/") or pg.dbname

        os.environ["DB_URL"] = async_url
        os.environ["POSTGRES_HOST"] = parsed.hostname or "localhost"
        os.environ["POSTGRES_PORT"] = str(parsed.port or 5432)
        os.environ["POSTGRES_USER"] = parsed.username or pg.username
        os.environ["POSTGRES_PASSWORD"] = parsed.password or pg.password
        os.environ["POSTGRES_DB"] = db_name

        # Redis
        redis_host = redis.get_container_host_ip()
        redis_port = int(redis.get_exposed_port(6379))
        _wait_for_port(redis_host, redis_port)

        redis_url = f"redis://{redis_host}:{redis_port}/0"
        os.environ["REDIS_URL"] = redis_url

        # Secure / ENV
        os.environ.setdefault("SECURE_SECRET_KEY", "integration-secret-key")
        os.environ.setdefault("SECURE_JWT_TTL", "3600")
        os.environ.setdefault("ENV", "test")

        # Миграции
        _run_migrations(pg_sync_url)

        yield {
            "pg_sync_url": pg_sync_url,
            "redis_url": redis_url,
        }


@pytest.fixture(scope="session")
def app(_infrastructure: dict) -> FastAPI:  # noqa: ARG001
    return create_app()


@pytest_asyncio.fixture
async def client(app: FastAPI):
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
