"""LLM Chat factory."""

from collections.abc import Callable
from enum import StrEnum

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

from app.settings.ai import ai_settings


class ChatClient(StrEnum):
    """Allowed chat providers."""

    open_router = "open_router"


def create_openrouter_chat() -> ChatOpenAI:
    """Create OpenRouter chat client."""
    return ChatOpenAI(
        model=ai_settings.LLM_MODEL,
        api_key=ai_settings.OPENROUTER_API_KEY,
        base_url=ai_settings.OPENROUTER_BASE_URL,
        temperature=0,
    )


chat_clients: dict[str, Callable[..., BaseChatModel]] = {
    "open_router": create_openrouter_chat,
}


class ChatFactory:
    """AI-chat client factory."""

    def set_chat_model(
        self,
        chat_client: ChatClient | str,
    ) -> BaseChatModel:
        """Create chat client."""
        factory = chat_clients.get(chat_client)

        if not factory:
            raise ValueError("Wrong chat client.")

        return factory()
