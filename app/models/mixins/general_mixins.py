"""General mixins for models."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    UUID as UUID_A,
)
from sqlalchemy import (
    DateTime,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class UuidPkMixin:
    """Mixin UUID primary_key."""

    id: Mapped[UUID] = mapped_column(
        UUID_A(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )


class CreatedAtMixin:
    """Mixin DateTime with timezone == True."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
