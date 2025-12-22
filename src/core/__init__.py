"""
Core Package

The heart of the application containing the business logic and domain model.
This package is framework-independent and has no external dependencies.

Structure:
- domain: Entities, value objects, and read models
- ports: Interfaces (abstractions) for external systems
- exceptions: Domain-specific errors and invariant violations

This follows the Hexagonal Architecture pattern, keeping business logic
completely isolated from technical concerns.
"""

from .domain import (
    ChatMessage, 
    Role, 
    PartOfSpeech,
    GrammaticalNumber,
    Gender,
    Tense,
    Person,
    CEFRLevel,
    Language,
)
from .exceptions import (
    DomainException,
)

__all__ = [
    # Domain
    "ChatMessage",
    "Role",
    "PartOfSpeech",
    "GrammaticalNumber",
    "Gender",
    "Tense",
    "Person",
    "CEFRLevel",
    "Language",
    # Exceptions
    "DomainException",
]
