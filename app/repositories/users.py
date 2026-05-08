"""User repository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.custom_exceptions.decorators import repo_error_decorator
from app.models import User


class UserRepo:
    """User repository."""

    @repo_error_decorator
    async def create_user(
        self,
        session: AsyncSession,
        user_name: str,
        email: str,
    ) -> User:
        """Create new user."""
        new_user = User(
            user_name=user_name,
            email=email,
        )

        session.add(new_user)
        await session.flush()

        return new_user

    @repo_error_decorator
    async def get_user(
        self,
        session: AsyncSession,
        user_id: UUID,
    ) -> User | None:
        """Get user."""
        stmt = select(User).where(User.id == user_id)
        res = await session.execute(stmt)
        user: User | None = res.scalar_one_or_none()

        return user

    @repo_error_decorator
    async def get_users(
        self,
        session: AsyncSession,
    ) -> list[User]:
        """Get users."""
        stmt = select(User)

        res = await session.execute(stmt)
        users = res.scalars()
        return list(users)


user_repo = UserRepo()
