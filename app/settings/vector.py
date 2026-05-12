"""Vector settings."""

from app.settings.base import Base


class VectorSettings(Base):
    """Vector settings."""

    VECTOR_SIZE: int
    EMBEDDING_MODEL: str
    CHUNK_SIZE: int
    CHUNK_OVERLAP: int
    COLLECTION_CACHE: str


vector_settings = VectorSettings()
