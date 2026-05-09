"""Document routers."""

from typing import Annotated
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Path,
    UploadFile,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.connections.pg import get_session
from app.schemes.documents import (
    CreateDocReq,
    DocResp,
)
from app.services.documents import doc_service

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=DocResp,
    description="Upload new document.",
)
async def upload_doc(
    file: Annotated[UploadFile, File(...)],
    user_id: Annotated[UUID, Form(...)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DocResp:
    """Upload new document."""
    doc = await doc_service.upload_doc(
        file=file,
        create_data=CreateDocReq(
            file_name=file.filename,
            uploaded_by=user_id,
        ),
        session=session,
    )

    return DocResp.model_validate(doc)


@router.get(
    path="/{document_id}",
    status_code=status.HTTP_200_OK,
    response_model=DocResp,
    description="Get document by id.",
)
async def get_doc(
    document_id: Annotated[UUID, Path(...)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DocResp:
    """Get document by id."""
    doc = await doc_service.get_doc(
        document_id=document_id,
        session=session,
    )

    return DocResp.model_validate(doc)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[DocResp],
    description="Get documents.",
)
async def get_docs(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[DocResp]:
    """Get documents."""
    docs = await doc_service.get_docs(
        session=session,
    )

    return [DocResp.model_validate(doc) for doc in docs]
