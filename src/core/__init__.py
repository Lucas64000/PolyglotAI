"""
Core Layer (Domain)

This layer contains:
- Domain entities (business objects with behavior)
- Value objects (immutable domain concepts)
- Port interfaces (contracts for infrastructure)
- Domain exceptions

RULES:
- ZERO external dependencies (only stdlib + typing)
- NO framework imports (no pydantic, no fastapi, etc.)
- NO infrastructure concerns
- All dependencies point INWARD (nothing here imports from application/infrastructure)
"""

from .domain import (
    # Entities
    UserProfile,
    VocabularyItem,
    UserError,
    GrammarRule,
    LearningSession,
    ChatMessage,
    # Value Objects
    Language,
    LanguagePair,
    CEFRLevel,
    Role,
    ErrorType,
    MasteryLevel,
    PartOfSpeech,
)
from .exceptions import (
    DomainException,
    ValidationError,
    EntityNotFoundError,
    InvalidLanguagePairError,
)

__all__ = [
    # Entities
    "UserProfile",
    "VocabularyItem",
    "UserError",
    "GrammarRule",
    "LearningSession",
    "ChatMessage",
    # Value Objects
    "Language",
    "LanguagePair",
    "CEFRLevel",
    "Role",
    "ErrorType",
    "MasteryLevel",
    "PartOfSpeech",
    # Exceptions
    "DomainException",
    "ValidationError",
    "EntityNotFoundError",
    "InvalidLanguagePairError",
]
