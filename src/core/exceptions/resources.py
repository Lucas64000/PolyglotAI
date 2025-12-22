"""
Resource Exception Classes

Defines exceptions for missing or duplicate entities.
"""

from uuid import UUID
from typing import Union

from .base import DomainException


class ResourceNotFoundError(DomainException):
    """Raised when a requested entity does not exist."""
    def __init__(self, resource_type: str, resource_id: Union[str, UUID]) -> None:
        super().__init__(f"{resource_type} not found with ID: {resource_id}")


class ResourceAlreadyExistsError(DomainException):
    """
    Raised when attempting to create an entity that already exists.
    Indicates a uniqueness constraint violation.
    """
    def __init__(self, resource_type: str, field: str, value: str) -> None:
        super().__init__(f"{resource_type} with {field} '{value}' already exists.")