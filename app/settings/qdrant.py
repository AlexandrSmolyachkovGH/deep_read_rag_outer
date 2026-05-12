"""Qdrant settings."""

from app.settings.base import Base


class QdrantSettings(Base):
    """Qdrant settings."""

    QDRANT_HOST: str
    QDRANT_PORT: int
    TOP_K: int

    @property
    def qdrant_url(self) -> str:
        """Return qdrant url."""
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"


qdrant_settings = QdrantSettings()
