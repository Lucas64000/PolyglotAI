"""
Domain Module

Contains all domain entities and value objects that represent
the core business concepts of a language learning application.
"""

from .entities import (
    UserProfile,
    VocabularyItem,
    UserError,
    GrammarRule,
    LearningSession,
    ChatMessage,
)
from .value_objects import (
    Language,
    LanguagePair,
    CEFRLevel,
    Role,
    ErrorType,
    MasteryLevel,
    PartOfSpeech,
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
]
