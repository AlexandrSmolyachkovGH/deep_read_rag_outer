"""Embedding factory."""

from collections.abc import Callable
from enum import StrEnum

from langchain_core.embeddings import Embeddings

from app.embeddings.openrouter_embed import OpenRouterEmbeddings


class EmbClients(StrEnum):
    """Allowed clients implemented for the service."""

    open_router = "open_router"


def create_openrouter_embeddings(
    api_key: str,
    model: str,
    base_url: str,
) -> OpenRouterEmbeddings:
    """Create embedding client based on OpenRouter."""
    return OpenRouterEmbeddings(
        api_key=api_key,
        model=model,
        base_url=base_url,
    )


embedding_clients: dict[str, Callable[..., Embeddings]] = {
    "open_router": create_openrouter_embeddings,
}


class EmbCliFactory:
    """Embedding client factory."""

    allowed_models = EmbClients

    def set_embedding_model(
        self,
        api_key: str,
        model: str,
        base_url: str,
        emb_client: EmbClients | str,
    ) -> Embeddings:
        """Create embedding client. Set embedding model."""
        factory = embedding_clients.get(emb_client)
        if not factory:
            raise ValueError("Wrong embedding client.")

        return factory(
            api_key=api_key,
            model=model,
            base_url=base_url,
        )
