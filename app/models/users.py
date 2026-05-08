"""User model."""

from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import Base
from app.models.mixins.general_mixins import (
    CreatedAtMixin,
    UuidPkMixin,
)

if TYPE_CHECKING:
    from app.models import (
        Collection,
        Document,
    )


class User(CreatedAtMixin, UuidPkMixin, Base):
    """User model."""

    __tablename__ = "users"

    user_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    collections: Mapped[list["Collection"]] = relationship(
        "Collection",
        back_populates="user",
    )
    documents: Mapped[list["Document"]] = relationship(
        "Document",
        back_populates="user",
    )

    def __str__(self) -> str:
        """Return string representation of the object."""
        return (
            f"{self.__class__.__name__}("
            f"id: {self.id}, "
            f"user_name: {self.user_name}, "
            f"email: {self.email}, "
            f"created_at: {self.created_at})"
        )

    def __repr__(self) -> str:
        """Represented value of the model."""
        return str(self)
