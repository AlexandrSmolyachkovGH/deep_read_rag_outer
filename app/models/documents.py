"""Document model."""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    UUID as UUID_A,
)
from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint,
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
        User,
    )


class Document(UuidPkMixin, CreatedAtMixin, Base):
    """Document model."""

    __tablename__ = "documents"

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    uploaded_by: Mapped[UUID] = mapped_column(
        UUID_A(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    collection_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "collections.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="documents",
    )
    collection: Mapped["Collection"] = relationship(
        "Collection",
        back_populates="documents",
    )

    __table_args__ = (
        UniqueConstraint(
            "file_name",
            "uploaded_by",
            name="unique_file_user",
        ),
    )

    def __str__(self) -> str:
        """Return string representation of the object."""
        return (
            f"{self.__class__.__name__}("
            f"id: {self.id}, "
            f"file_name: {self.file_name}, "
            f"uploaded_by: {self.uploaded_by}, "
            f"collection_id: {self.collection_id}, "
            f"created_at: {self.created_at})"
        )

    def __repr__(self) -> str:
        """Represented value of the model."""
        return str(self)
