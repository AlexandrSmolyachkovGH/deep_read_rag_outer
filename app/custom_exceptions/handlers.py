"""Exception handlers."""

from fastapi import (
    Request,
    status,
)
from fastapi.responses import (
    JSONResponse,
)

from app.custom_exceptions.exceptions import (
    NotFoundError,
    RepositoryError,
    ServiceError,
)


async def handle_repo_errors(
    request: Request,
    err: RepositoryError,
) -> JSONResponse:
    """Handle repository errors."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "details": f"RepositoryError: {err!s}",
        },
    )


async def handle_service_errors(
    request: Request,
    err: ServiceError,
) -> JSONResponse:
    """Handle service errors."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "details": f"ServiceError: {err!s}",
        },
    )


async def handle_not_found_errors(
    request: Request,
    err: NotFoundError,
) -> JSONResponse:
    """Handle not found errors."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "details": f"NotFoundError: {err!s}",
        },
    )
