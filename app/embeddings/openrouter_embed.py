"""Embeddings implementation compatible with OpenRouter."""

from langchain_core.embeddings import Embeddings
from openai import (
    AsyncOpenAI,
    OpenAI,
)


class OpenRouterEmbeddings(Embeddings):
    """Embeddings implementation compatible with OpenRouter."""

    def __init__(
        self,
        model: str,
        api_key: str,
        base_url: str,
    ) -> None:
        """OpenRouter embeddings init."""
        self.model = model
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.sync_client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    async def aembed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Create embeddings form docs."""
        response = await self.client.embeddings.create(
            model=self.model,
            input=texts,
        )
        return [item.embedding for item in response.data]

    async def aembed_query(
        self,
        text: str,
    ) -> list[float]:
        """Embed query."""
        response = await self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Sync embed_documents."""
        response = self.sync_client.embeddings.create(
            model=self.model,
            input=texts,
        )

        return [item.embedding for item in response.data]

    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        """Sync embed_query."""
        response = self.sync_client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding
