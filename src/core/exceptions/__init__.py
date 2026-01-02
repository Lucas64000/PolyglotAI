"""
Core Exceptions

Custom exceptions for the core layer.
These represent business rule violations and domain errors.
"""

from .base import (
    PolyglotException,
    DomainException, 
    InfrastructureError,
)
from .business import (
    BusinessRuleViolation,
    InvalidConversationStateError,
    ConversationNotWritableError,
    EmptyConversationTitleError,
    ConversationTitleTooLongError,
    InvalidLanguagePairError,
    InvalidLanguageIsoCodeError,
    InvalidChatMessageContentError,
    InvalidLevelChangeError,
)
from .resources import (
    ResourceNotFoundError, 
    ResourceAlreadyExistsError
)
from .infrastructure import (
    ExternalServiceError,
    ChatProviderError,
    TeacherResponseError,
    PersistenceError,
)

__all__ = [
    # Base
    "PolyglotException",
    "DomainException",
    "InfrastructureError",
    # Business Rules
    "BusinessRuleViolation",
    "InvalidConversationStateError",
    "ConversationNotWritableError",
    "EmptyConversationTitleError",
    "ConversationTitleTooLongError",
    "InvalidLanguagePairError",
    "InvalidLanguageIsoCodeError",
    "InvalidLevelChangeError",
    "InvalidChatMessageContentError",
    "ResourceNotFoundError",
    "ResourceAlreadyExistsError",
    "InvalidLevelChangeError",
    # Ports rules
    "ExternalServiceError",
    "ChatProviderError",
    "TeacherResponseError",
    "PersistenceError",
]
