"""
Domain Exceptions

Custom exceptions for the domain layer.
These represent business rule violations and domain errors.
"""

from .base import DomainException
from .business import (
    BusinessRuleViolation,
    InvalidConversationStateError,
    ConversationNotWritableError,
    EmptyConversationTitleError,
    ConversationTitleTooLongError,
    InvalidLanguagePairError,
    InvalidLanguageIsoCodeError,
    InvalidChatMessageContentError,
    InvalidChatMessageEditError,
    InvalidLevelChangeError,
)
from .resources import ResourceNotFoundError, ResourceAlreadyExistsError

__all__ = [
    "DomainException",
    # Business
    "BusinessRuleViolation",
    "InvalidConversationStateError",
    "ConversationNotWritableError",
    "EmptyConversationTitleError",
    "ConversationTitleTooLongError",
    "InvalidLanguagePairError",
    "InvalidLanguageIsoCodeError",
    "InvalidChatMessageContentError",
    "InvalidChatMessageEditError",
    "InvalidLevelChangeError",
    # Resources
    "ResourceNotFoundError", 
    "ResourceAlreadyExistsError",
]
