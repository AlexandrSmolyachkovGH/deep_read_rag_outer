"""Redis handler."""

import redis.asyncio as aredis
from fastapi import Request

from app.settings.redis import redis_settings


class RedisHandler:
    """Redis handler."""

    def __init__(self) -> None:
        """Handler init."""
        self.client: aredis.Redis | None = None

    def get_client(self) -> aredis.Redis:
        """Get async redis client."""
        if self.client is None:
            self.client = aredis.Redis(
                host=redis_settings.REDIS_HOST,
                port=redis_settings.REDIS_PORT,
                password=redis_settings.REDIS_PASSWORD.get_secret_value(),
                decode_responses=True,
            )

        return self.client

    async def close_client(self) -> None:
        """Close async redis client."""
        if self.client:
            await self.client.aclose()


def get_redis(
    request: Request,
) -> RedisHandler:
    """Retrieve async redis client."""
    redis: RedisHandler = request.app.state.redis

    return redis
