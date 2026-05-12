"""AI settings."""

from app.settings.base import Base


class AiSettings(Base):
    """AI settings."""

    OPENROUTER_CLIENT: str
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str
    LLM_MODEL: str
    EMBEDDING_MODEL: str
    VECTOR_SIZE: int


ai_settings = AiSettings()
