"""Collection repository."""

from uuid import UUID

from sqlalchemy import (
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.custom_exceptions.decorators import repo_error_decorator
from app.models import Collection


class CollectionRepo:
    """Collection repository."""

    async def create_collection(
        self,
        session: AsyncSession,
        collection_name: str,
        created_by: UUID,
    ) -> Collection:
        """Create new collection."""
        new_coll = Collection(
            collection_name=collection_name,
            created_by=created_by,
        )

        session.add(new_coll)
        await session.flush()

        return new_coll

    @repo_error_decorator
    async def get_collection(
        self,
        session: AsyncSession,
        collection_id: UUID,
    ) -> Collection | None:
        """Get collection by id."""
        stmt = select(Collection).where(Collection.id == collection_id)

        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    @repo_error_decorator
    async def get_collections(
        self,
        session: AsyncSession,
    ) -> list[Collection]:
        """Get collections."""
        stmt = select(Collection)

        res = await session.execute(stmt)
        return list(res.scalars())


coll_repo = CollectionRepo()
