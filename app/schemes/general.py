"""General schemes."""

from pydantic import BaseModel


class RootResp(BaseModel):
    """Response scheme for root."""

    service_name: str
    service_description: str
    useful_paths: dict[str, str]


class HealthResp(BaseModel):
    """Response scheme for health-check."""

    healthy_status: str
