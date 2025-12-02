"""
Domain Exceptions

Custom exceptions for the domain layer.
These represent business rule violations and domain errors.
"""

from .domain_exceptions import (
    DomainException,
    ValidationError,
    EntityNotFoundError,
    InvalidLanguagePairError,
    InvalidCEFRLevelError,
    SessionNotActiveError,
)

__all__ = [
    "DomainException",
    "ValidationError",
    "EntityNotFoundError",
    "InvalidLanguagePairError",
    "InvalidCEFRLevelError",
    "SessionNotActiveError",
]
