"""Document schemes."""

from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
)

from app.schemes.mixins import BaseResponseMixin


class CreateDocReq(BaseModel):
    """Create collection request scheme."""

    file_name: str
    uploaded_by: UUID = Field(
        ...,
        description="Owner unique ID.",
    )


class DocResp(BaseResponseMixin, CreateDocReq):
    """Document response scheme."""
