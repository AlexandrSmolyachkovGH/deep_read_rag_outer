"""Qdrant handler."""

import asyncio
from uuid import (
    UUID,
    uuid4,
)

import redis.asyncio as aredis
from langchain_core.documents.base import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores.base import VectorStoreRetriever
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from app.embeddings.embedding_factory import EmbCliFactory
from app.settings.ai import ai_settings
from app.settings.qdrant import qdrant_settings
from app.settings.vector import vector_settings


class QdrantHandler:
    """Qdrant handler."""

    def __init__(self) -> None:
        """Handler init."""
        self.client: QdrantClient | None = None
        self.embedding_client: Embeddings | None = None

    def _set_client(self) -> QdrantClient:
        """Set QdrantClient."""
        self.client = QdrantClient(
            url=qdrant_settings.qdrant_url,
        )

        return self.client

    def _set_embedding_client(self) -> Embeddings:
        """Set Embedding client."""
        factory = EmbCliFactory()
        embedding_client = factory.set_embedding_model(
            api_key=ai_settings.OPENROUTER_API_KEY,
            model=ai_settings.EMBEDDING_MODEL,
            base_url=ai_settings.OPENROUTER_BASE_URL,
            emb_client=ai_settings.OPENROUTER_CLIENT,
        )

        self.embedding_client = embedding_client
        return embedding_client

    def get_client(self) -> QdrantClient:
        """Get QdrantClient. If client is None - set it lazy."""
        if self.client is None:
            self._set_client()

        return self.client

    def get_embedding_client(self) -> Embeddings:
        """Get Embedding client."""
        if self.embedding_client is None:
            self._set_embedding_client()

        return self.embedding_client

    async def ensure_collection(
        self,
        collection_name: str,
    ) -> None:
        """Check collection."""
        client: QdrantClient = self.get_client()

        collections = client.get_collections().collections
        names = {col.name for col in collections}

        if collection_name not in names:
            raise ValueError(
                f"Collection {collection_name} doesn't exits.",
            )

    async def async_ensure_collection(
        self,
        redis: aredis.Redis,
        collection_name: str | UUID,
    ) -> None:
        """Async wrapper for collection_ensure."""
        if isinstance(collection_name, UUID):
            collection_name = str(collection_name)

        check_cache = await redis.sismember(
            name=vector_settings.COLLECTION_CACHE,
            value=collection_name,
        )

        if not check_cache:
            await self.ensure_collection(
                collection_name=collection_name,
            )
            await redis.sadd(
                vector_settings.COLLECTION_CACHE,
                collection_name,
            )
            await redis.expire(
                vector_settings.COLLECTION_CACHE,
                time=3600,
            )

    async def _embed_documents_batch(
        self,
        documents: list[Document],
    ) -> tuple[list[list[float]], list[dict]]:
        """Batch embedding for documents."""
        texts = [doc.page_content for doc in documents]
        metadata = [doc.metadata for doc in documents]

        embedding_client = self.get_embedding_client()

        vectors = await embedding_client.aembed_documents(
            texts=texts,
        )

        return vectors, metadata

    async def vectorize_documents_batch(
        self,
        collection_name: str | UUID,
        documents: list[Document],
        redis: aredis.Redis,
    ) -> None:
        """Vectorize batch of documents."""
        if isinstance(collection_name, UUID):
            collection_name = str(collection_name)

        client: QdrantClient = self.get_client()

        await self.async_ensure_collection(
            redis=redis,
            collection_name=collection_name,
        )

        BATCH_SIZE = 32

        for doc_n in range(0, len(documents), BATCH_SIZE):
            doc_batch = documents[doc_n : doc_n + BATCH_SIZE]
            vectors, _ = await self._embed_documents_batch(
                documents=doc_batch,
            )
            points = [
                PointStruct(
                    id=uuid4(),
                    vector=vector,
                    payload={
                        "page_content": doc.page_content,
                        "metadata": doc.metadata,
                    },
                )
                for vector, doc in zip(vectors, doc_batch, strict=True)
            ]

            await asyncio.to_thread(
                client.upsert,
                collection_name=collection_name,
                points=points,
            )

    async def create_collection(
        self,
        collection_name: str,
    ) -> None:
        """Create new collection."""
        client: QdrantClient = self.get_client()

        await asyncio.to_thread(
            client.create_collection,
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=ai_settings.VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

    async def retrieve_documents(
        self,
        collection_name: str,
        question: str,
        redis: aredis.Redis,
        search_type: str = "similarity",
    ) -> list[Document]:
        """Retrieve similar documents."""
        await self.async_ensure_collection(
            redis=redis,
            collection_name=collection_name,
        )
        vector_store: QdrantVectorStore = QdrantVectorStore(
            client=self.get_client(),
            collection_name=collection_name,
            embedding=self.get_embedding_client(),
        )
        retriever: VectorStoreRetriever = vector_store.as_retriever(
            search_type=search_type,
            search_kwargs={
                "k": qdrant_settings.TOP_K,
            },
        )

        docs: list[Document] = await retriever.ainvoke(question)

        return docs


qdrant_handler = QdrantHandler()
