"""Document repository."""

from uuid import UUID

from sqlalchemy import (
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.custom_exceptions.decorators import repo_error_decorator
from app.models import Document


class DocumentRepository:
    """Document repository."""

    async def create_doc(
        self,
        session: AsyncSession,
        file_name: str,
        uploaded_by: UUID,
        collection_id: UUID,
    ) -> Document:
        """Create new document."""
        doc = Document(
            file_name=file_name,
            uploaded_by=uploaded_by,
            collection_id=collection_id,
        )
        session.add(doc)
        await session.flush()

        return doc

    @repo_error_decorator
    async def get_doc(
        self,
        session: AsyncSession,
        document_id: UUID,
    ) -> Document | None:
        """Get document by id."""
        stmt = select(Document).where(
            Document.id == document_id,
        )
        doc = await session.execute(stmt)

        return doc.scalar_one_or_none()

    @repo_error_decorator
    async def get_docs(
        self,
        session: AsyncSession,
    ) -> list[Document]:
        """Get documents."""
        stmt = select(Document)
        doc = await session.execute(stmt)

        return list(doc.scalars())


doc_repo = DocumentRepository()
