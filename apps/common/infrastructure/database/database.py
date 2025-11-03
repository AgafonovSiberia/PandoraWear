from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from apps.common.config import DatabaseSettings


class DatabaseCore:
    def __init__(self, settings: DatabaseSettings):
        self._settings = settings
        self._engine = create_async_engine(
            str(settings.DB_URL),
            echo=False,
            pool_pre_ping=True,
        )
        self._session_factory = async_sessionmaker(
            self._engine, autoflush=True, expire_on_commit=False, class_=AsyncSession
        )

    @property
    def engine(self):
        return self._engine

    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory
