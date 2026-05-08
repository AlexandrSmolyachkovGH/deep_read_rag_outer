"""Postgres settings."""

from pydantic import SecretStr

from app.settings.base import Base


class PGSettings(Base):
    """Postgres settings."""

    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_PORT_INNER: int
    POSTGRES_PORT_OUTER: int
    POSTGRES_ASYNC_DRIVER: str = "asyncpg"

    def _get_general_dsn_part(self) -> str:
        """Get general part of PG DSN."""
        return (
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD.get_secret_value()}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT_OUTER}/"
            f"{self.POSTGRES_DB}"
        )

    def get_async_pg_dsn(self) -> str:
        """Get async PG DSN."""
        return (
            f"postgresql+{self.POSTGRES_ASYNC_DRIVER}://"
            f"{self._get_general_dsn_part()}"
        )


pg_settings = PGSettings()
