"""Main app file."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.connections.pg import PostgresHandler
from app.routers.health import router as health_router
from app.routers.root import router as root_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan."""
    pg_handler = PostgresHandler(
        pool_size=5,
        max_overflow=5,
        echo=True,
    )
    _app.state.pg_handler = pg_handler

    yield

    await pg_handler.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(root_router)
app.include_router(health_router)

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=8000,
    )
