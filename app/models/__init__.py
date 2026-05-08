"""Model init file."""

from app.models.collections import Collection
from app.models.documents import Document
from app.models.users import User

__all__ = [
    "Collection",
    "Document",
    "User",
]
