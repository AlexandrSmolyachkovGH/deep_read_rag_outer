"""User schemes."""

from pydantic import (
    BaseModel,
    EmailStr,
)

from app.schemes.mixins import BaseResponseMixin


class CreateUserReq(BaseModel):
    """Create user request scheme."""

    user_name: str
    email: EmailStr


class UserResp(BaseResponseMixin, CreateUserReq):
    """User response scheme."""
