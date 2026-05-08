"""Decorators for catching exceptions."""

from collections.abc import Callable, Coroutine
from functools import wraps
from typing import (
    ParamSpec,
)

from sqlalchemy.exc import (
    IntegrityError,
    SQLAlchemyError,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.custom_exceptions.exceptions import RepositoryError

P = ParamSpec("P")


def repo_error_decorator[**P, RES](
    repo_func: Callable[P, Coroutine[None, None, RES]],
) -> Callable[P, Coroutine[None, None, RES]]:
    """Take repo function and handle exceptions."""

    @wraps(repo_func)
    async def wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> RES:
        """Add extra logic to catch exception properly."""
        session: None | AsyncSession = kwargs.get("session")

        if session is None:
            for arg in args:
                if isinstance(arg, AsyncSession):
                    session = arg
                    break
        try:

            res = await repo_func(*args, **kwargs)

        except IntegrityError as err:

            if session is not None:
                await session.rollback()

            msg = f"Integrity error in {repo_func.__name__}"
            raise RepositoryError(msg) from err

        except SQLAlchemyError as err:

            if session is not None:
                await session.rollback()

            msg = f"DB error in {repo_func.__name__}"
            raise RepositoryError(msg) from err

        return res

    return wrapper
