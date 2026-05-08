"""Root router."""

from fastapi import (
    APIRouter,
    status,
)

from app.schemes.general import RootResp

router = APIRouter(
    tags=["root"],
)


@router.get(
    path="/",
    response_model=RootResp,
    status_code=status.HTTP_200_OK,
    description="Return general service info.",
)
async def get_root() -> RootResp:
    """Return general service info."""
    return RootResp(
        service_name="DeepReadOuter",
        service_description="RAG service using non-local AI models for interaction.",
        useful_paths={
            "/health": "Check health status of the service.",
            "/docs": "Swagger UI.",
        },
    )
