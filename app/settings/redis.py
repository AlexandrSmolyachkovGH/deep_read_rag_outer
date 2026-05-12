"""Redis settings."""

from pydantic import SecretStr

from app.settings.base import Base


class RedisSettings(Base):
    """Redis settings."""

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: SecretStr


redis_settings = RedisSettings()
