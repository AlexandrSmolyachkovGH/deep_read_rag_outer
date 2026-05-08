"""Postgres connection setup."""

from collections.abc import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.settings.pg import pg_settings


class PostgresHandler:
    """PG handler."""

    def __init__(
        self,
        pool_size: int,
        max_overflow: int,
        echo: bool = False,
    ) -> None:
        """PostgresHandler initialization."""
        self.async_engine: AsyncEngine = create_async_engine(
            url=pg_settings.get_async_pg_dsn(),
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=30,
            pool_recycle=1800,
            pool_pre_ping=True,
            echo=echo,
        )
        self.async_session_factory = async_sessionmaker(
            bind=self.async_engine,
            class_=AsyncSession,
            autoflush=True,
            expire_on_commit=True,
        )

    async def dispose(self) -> None:
        """Dispose connection pool for async engine."""
        await self.async_engine.dispose()

    async def get_session(
        self,
        request: Request,
    ) -> AsyncGenerator[AsyncSession, None]:
        """Retrieve async session from the factory."""
        pg: PostgresHandler = request.state.pg_handler

        async with pg.async_session_factory as async_session:
            yield async_session
