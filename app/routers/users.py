"""User router."""

from typing import Annotated
from uuid import UUID

from fastapi import (
    APIRouter,
    Body,
    Depends,
    Path,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.connections.pg import get_session
from app.schemes.users import (
    CreateUserReq,
    UserResp,
)
from app.services.users import user_service

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    path="/",
    response_model=UserResp,
    status_code=status.HTTP_201_CREATED,
    description="Create new user.",
)
async def create_user(
    create_data: Annotated[CreateUserReq, Body()],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserResp:
    """Create new user."""
    user = await user_service.create_user(
        create_data=create_data,
        session=session,
    )

    return UserResp.model_validate(user)


@router.get(
    path="/{user_id}",
    response_model=UserResp,
    status_code=status.HTTP_200_OK,
    description="Get user.",
)
async def get_user(
    user_id: Annotated[UUID, Path(...)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserResp:
    """Get user by user_id."""
    user = await user_service.get_user(
        user_id=user_id,
        session=session,
    )

    return UserResp.model_validate(user)


@router.get(
    path="/",
    response_model=list[UserResp],
    status_code=status.HTTP_200_OK,
    description="Get users.",
)
async def get_users(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[UserResp]:
    """Get users."""
    users = await user_service.get_users(
        session=session,
    )

    return [UserResp.model_validate(user) for user in users]
