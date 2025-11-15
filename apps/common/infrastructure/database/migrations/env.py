import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool

from apps.common.config import DatabaseSettings
from apps.common.infrastructure.database.models import Credential, Device, User  # noqa
from apps.common.infrastructure.database.models.base import Base

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_db_url() -> str:
    db_settings = DatabaseSettings()
    print(db_settings.DB_URL)
    url = str(db_settings.DB_URL)
    if not url:
        raise RuntimeError("DB_URL env is empty for Alembic")
    return url

def run_migrations_offline() -> None:
    context.configure(
        url=get_db_url(),
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    connectable = create_async_engine(get_db_url(), poolclass=pool.NullPool)

    async with connectable.connect() as async_conn:
        await async_conn.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())