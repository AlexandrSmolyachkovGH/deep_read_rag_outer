"""Collection service."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.custom_exceptions.exceptions import NotFoundError
from app.models import Collection
from app.repositories.collections import coll_repo
from app.schemes.collections import CreateCollReq


class CollectionService:
    """Collection service."""

    async def create_collection(
        self,
        create_data: CreateCollReq,
        session: AsyncSession,
    ) -> Collection:
        """Create new collection."""
        async with session.begin():
            collection = await coll_repo.create_collection(
                session=session,
                collection_name=create_data.collection_name,
                created_by=create_data.created_by,
            )

        return collection

    async def get_collection(
        self,
        collection_id: UUID,
        session: AsyncSession,
    ) -> Collection:
        """Get collection by id."""
        collection: Collection | None = await coll_repo.get_collection(
            session=session,
            collection_id=collection_id,
        )

        if collection is None:
            raise NotFoundError("Collection %s not found", collection_id)

        return collection

    async def get_collections(
        self,
        session: AsyncSession,
    ) -> list[Collection]:
        """Get collections."""
        collections = await coll_repo.get_collections(
            session=session,
        )
        return collections


coll_service = CollectionService()
