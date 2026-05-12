"""Document uploading and processing."""

from uuid import UUID

from fastapi import UploadFile
from langchain_core.documents.base import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.settings.vector import vector_settings


class DocHandler:
    """Document uploading and processing."""

    async def create_documents_from_file(
        self,
        file: UploadFile,
        document_id: UUID,
        user_id: UUID,
        collection_id: UUID,
    ) -> list[Document]:
        """Transform the file to list of Documents."""
        context = await file.read()
        text = context.decode("utf-8")
        documents = [
            Document(
                page_content=text,
                metadata={
                    "file_name": file.filename,
                    "user_id": str(user_id),
                    "document_id": str(document_id),
                    "collection_id": str(collection_id),
                },
            ),
        ]

        return documents

    """Document uploading and processing."""

    def split_document(
        self,
        documents: list[Document],
    ) -> list[Document]:
        """
        Split text in document for semantic chunks.
        Use exactly RecursiveCharacterTextSplitter to save context between chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ""],
            chunk_size=vector_settings.CHUNK_SIZE,
            chunk_overlap=vector_settings.CHUNK_OVERLAP,
        )

        chunks = text_splitter.split_documents(documents=documents)

        for i, doc in enumerate(chunks):
            doc.metadata["chunk_index"] = i

        return chunks


doc_handler = DocHandler()
