"""LLM handler for interactions with model."""

from uuid import UUID

import redis.asyncio as aredis
from langchain_core.language_models.chat_models import BaseChatModel

from app.connections.qdrant import qdrant_handler
from app.llm.chat_factory import ChatFactory
from app.llm.prompt import prompt_builder
from app.settings.ai import ai_settings


class LLMHandler:
    """LLM handler for interactions with model."""

    def __init__(self) -> None:
        """Handler init."""
        self.chat_client: BaseChatModel | None = None

    def get_chat_client(self) -> BaseChatModel:
        """Get llm chat client."""
        if self.chat_client is None:
            factory = ChatFactory()
            self.chat_client = factory.set_chat_model(
                chat_client=ai_settings.OPENROUTER_CLIENT,
            )

        return self.chat_client

    async def create_llm_request(
        self,
        question: str,
        collection_name: str,
        redis: aredis.Redis,
    ) -> tuple[str, list[str]]:
        """
        Build prompt for LLM model.
        Initially retrieve context from vector db.
        """
        context = await qdrant_handler.retrieve_documents(
            collection_name=collection_name,
            question=question,
            redis=redis,
        )
        sources = list(
            {doc.metadata.get("file_name", "unknown") for doc in context},
        )
        prompt = prompt_builder.create_new_prompt(
            context=context,
            question=question,
        )

        return prompt, sources

    async def invoke_llm(
        self,
        question: str,
        collection_name: str | UUID,
        redis: aredis.Redis,
    ) -> tuple[str, list[str]]:
        """Send prompt to LLM and receive result."""
        if isinstance(collection_name, UUID):
            collection_name = str(collection_name)

        prompt, sources = await self.create_llm_request(
            question=question,
            collection_name=collection_name,
            redis=redis,
        )

        llm_client = self.get_chat_client()

        invoke_res = await llm_client.ainvoke(
            input=prompt,
        )

        return invoke_res.content, sources


llm_handler = LLMHandler()
