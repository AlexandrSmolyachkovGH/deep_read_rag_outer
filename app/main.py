"""Main app file."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.connections.pg import PostgresHandler
from app.custom_exceptions.exceptions import (
    NotFoundError,
    RepositoryError,
    ServiceError,
)
from app.custom_exceptions.handlers import (
    handle_not_found_errors,
    handle_repo_errors,
    handle_service_errors,
)
from app.routers.collections import router as collection_router
from app.routers.health import router as health_router
from app.routers.root import router as root_router
from app.routers.users import router as user_router


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

# Routers
app.include_router(root_router)
app.include_router(health_router)
app.include_router(user_router)
app.include_router(collection_router)

# Exception handlers
app.add_exception_handler(RepositoryError, handle_repo_errors)
app.add_exception_handler(ServiceError, handle_service_errors)
app.add_exception_handler(NotFoundError, handle_not_found_errors)

if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        host="127.0.0.1",
        port=8000,
    )
