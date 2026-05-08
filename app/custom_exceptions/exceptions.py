"""Custom exceptions."""


class RepositoryError(Exception):
    """Repository layer errors."""


class NotFoundError(Exception):
    """Record not found exception."""


class ServiceError(Exception):
    """Service layer errors."""
