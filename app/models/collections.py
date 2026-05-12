"""Collection model."""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    UUID as UUID_A,
)
from sqlalchemy import (
    ForeignKey,
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
        Document,
        User,
    )


class Collection(UuidPkMixin, CreatedAtMixin, Base):
    """Collection model."""

    __tablename__ = "collections"

    collection_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )
    created_by: Mapped[UUID] = mapped_column(
        UUID_A(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="collections",
    )
    documents: Mapped[list["Document"]] = relationship(
        "Document",
        back_populates="collection",
    )

    def __str__(self) -> str:
        """Return string representation of the object."""
        return (
            f"{self.__class__.__name__}("
            f"id: {self.id}, "
            f"collection_name: {self.collection_name}, "
            f"created_by: {self.created_by}, "
            f"created_at: {self.created_at})"
        )

    def __repr__(self) -> str:
        """Represented value of the model."""
        return str(self)
