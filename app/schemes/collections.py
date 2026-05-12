"""Collection schemes."""

from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
)

from app.schemes.mixins import BaseResponseMixin, ResponseMixin


class CreateCollReq(BaseModel):
    """Create collection request scheme."""

    collection_name: str
    created_by: UUID = Field(
        ...,
        description="Owner unique ID.",
    )


class CollResp(BaseResponseMixin, CreateCollReq):
    """Collection response scheme."""


class AskAIResp(ResponseMixin):
    """Ask AI response scheme."""

    context: str
    meta: list[str]
