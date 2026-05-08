"""User service."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.custom_exceptions.exceptions import (
    NotFoundError,
)
from app.models import User
from app.repositories.users import user_repo
from app.schemes.users import CreateUserReq


class UserService:
    """User service."""

    async def create_user(
        self,
        create_data: CreateUserReq,
        session: AsyncSession,
    ) -> User:
        """Create new user."""
        async with session.begin():
            user = await user_repo.create_user(
                session=session,
                user_name=create_data.user_name,
                email=create_data.email,
            )

        return user

    async def get_user(
        self,
        user_id: UUID,
        session: AsyncSession,
    ) -> User:
        """Get user."""
        user = await user_repo.get_user(
            session=session,
            user_id=user_id,
        )

        if user is None:
            raise NotFoundError(
                "User %s not found.",
                user_id,
            )

        return user

    async def get_users(
        self,
        session: AsyncSession,
    ) -> list[User]:
        """Get users."""
        users = await user_repo.get_users(
            session=session,
        )

        return users


user_service = UserService()
