"""Document service."""

from pathlib import Path
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.exc import (
    IntegrityError,
    SQLAlchemyError,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.custom_exceptions.exceptions import (
    NotFoundError,
    ServiceError,
)
from app.models import Document
from app.repositories.documents import doc_repo
from app.repositories.users import user_repo
from app.schemes.documents import (
    CreateDocReq,
)

ALLOWED_EXTENSIONS = {
    ".txt",
}


class DocumentService:
    """Document service."""

    def validate_filetype(
        self,
        file: UploadFile,
    ) -> None:
        """Check if type of the provided file is allowed."""
        if not file.filename:
            raise ServiceError("Filename is missing")

        ext = Path(file.filename).suffix.lower()

        if ext not in ALLOWED_EXTENSIONS:
            raise ServiceError(
                "Invalid filetype. "
                "Allowed types for uploading: "
                f"{', '.join(ext for ext in ALLOWED_EXTENSIONS)}.",
            )

    async def upload_doc(
        self,
        file: UploadFile,
        create_data: CreateDocReq,
        session: AsyncSession,
    ) -> Document:
        """Upload new document."""
        user_check = await user_repo.get_user(
            session=session,
            user_id=create_data.uploaded_by,
        )
        if not user_check:
            raise NotFoundError(
                f"User {create_data.uploaded_by} not found.",
            )

        self.validate_filetype(file=file)
        try:
            new_doc = await doc_repo.create_doc(
                session=session,
                file_name=create_data.file_name,
                uploaded_by=create_data.uploaded_by,
            )
        except IntegrityError as err:
            raise ServiceError(
                f"File '{create_data.file_name}' had been uploaded"
                f" previously by {create_data.uploaded_by}.",
            ) from err

        except SQLAlchemyError as err:
            raise SQLAlchemyError(
                "Database operation failed.",
            ) from err

        await session.commit()

        return new_doc

    async def get_doc(
        self,
        document_id: UUID,
        session: AsyncSession,
    ) -> Document:
        """Get document by id."""
        doc = await doc_repo.get_doc(
            session=session,
            document_id=document_id,
        )
        if doc is None:
            raise NotFoundError(
                "Document %s not found",
                document_id,
            )

        return doc

    async def get_docs(
        self,
        session: AsyncSession,
    ) -> list[Document]:
        """Get documents."""
        docs = await doc_repo.get_docs(
            session=session,
        )

        return docs


doc_service = DocumentService()
