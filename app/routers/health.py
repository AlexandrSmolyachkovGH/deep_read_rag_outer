"""Health check router."""

from fastapi import (
    APIRouter,
    status,
)

from app.schemes.general import HealthResp

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get(
    path="/",
    response_model=HealthResp,
    status_code=status.HTTP_200_OK,
    description="Check health status of the service.",
)
async def check_healthy_status() -> HealthResp:
    """Check health status of the service."""
    return HealthResp(
        healthy_status="Healthy",
    )
