"""Collection service."""

from uuid import UUID

from sqlalchemy.exc import (
    IntegrityError,
    SQLAlchemyError,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.connections.qdrant import qdrant_handler
from app.custom_exceptions.exceptions import (
    NotFoundError,
    ServiceError,
)
from app.models import Collection
from app.repositories.collections import coll_repo
from app.repositories.users import user_repo
from app.schemes.collections import CreateCollReq


class CollectionService:
    """Collection service."""

    async def create_collection(
        self,
        create_data: CreateCollReq,
        session: AsyncSession,
    ) -> Collection:
        """Create new collection."""
        check_user = await user_repo.get_user(
            session=session,
            user_id=create_data.created_by,
        )
        if not check_user:
            raise NotFoundError(
                f"User '{create_data.created_by}' not found.",
            )

        try:
            collection = await coll_repo.create_collection(
                session=session,
                collection_name=create_data.collection_name,
                created_by=create_data.created_by,
            )

        except IntegrityError as err:
            raise ServiceError(
                "Collection already exists.",
            ) from err

        except SQLAlchemyError as err:
            raise ServiceError(
                "Database operation failed.",
            ) from err

        try:
            await qdrant_handler.create_collection(
                collection_name=collection.id,
            )

        except Exception as exc:
            await session.rollback()
            raise ServiceError("Collection creation failed in qdrant") from exc

        await session.commit()

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
