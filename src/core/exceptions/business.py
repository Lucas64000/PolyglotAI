"""
Business Rule Violation Exceptions

Exceptions raised when business rules or domain invariants are violated.
These typically indicate invalid user actions or invalid entity states.
"""

from uuid import UUID

from .base import DomainException

class BusinessRuleViolation(DomainException):
    """Base class for invalid user actions violating domain invariants."""

# Conversations errors 

class InvalidConversationStateError(BusinessRuleViolation):
    """Raised when a conversation is in an invalid state and cannot be instanciated or restored."""
    def __init__(self, conversation_id: UUID, status: str) -> None:
        super().__init__(
            f"Conversation '{conversation_id}' cannot be instantiated with status '{status}'."
        )


class ConversationNotWritableError(BusinessRuleViolation):
    """Raised when attempting to add a message to a conversation that is not writable."""
    def __init__(self, conversation_id: UUID, status: str) -> None:
        super().__init__(
            f"Operation denied. Conversation '{conversation_id}' is currently '{status}'."
        )


class EmptyConversationTitleError(BusinessRuleViolation):
    """Raised when trying to set an empty conversation title."""
    def __init__(self, conversation_id: UUID) -> None:
        super().__init__(
            f"Conversation '{conversation_id}' title cannot be empty."
        )


class ConversationTitleTooLongError(BusinessRuleViolation):
    """Raised when trying to set a conversation title that is too long."""
    def __init__(self, conversation_id: UUID, title_length: int, max_length: int) -> None:
        super().__init__(
            f"Conversation '{conversation_id}' title is too long ({title_length} chars, max {max_length})."
        )

# User errors

class InvalidLanguagePairError(BusinessRuleViolation):
    """Raised when the native and target languages are incompatible."""
    def __init__(self, native: str, target: str) -> None:
        super().__init__(
            f"Invalid language pair. Native: '{native}', Target: '{target}'."
        )


class InvalidLevelChangeError(BusinessRuleViolation):
    """Raised when trying to change level to an invalid value."""
    def __init__(self, current_level: str, new_level: str) -> None:
        super().__init__(
            f"Cannot change level from '{current_level}' to '{new_level}': level changes must be to adjacent levels only."
        )
        
# Language errors

class InvalidLanguageIsoCodeError(BusinessRuleViolation):
    """Raised when a language code does not respect the ISO 639-1 format (2 chars)."""
    def __init__(self, invalid_code: str) -> None:
        super().__init__(
            f"Invalid Language Code: '{invalid_code}'. Must be 2-char ISO 639-1 format."
        )

# ChatMessage errors

class InvalidChatMessageContentError(BusinessRuleViolation):
    """Raised when a chat message violates content rules based on its role."""
    def __init__(self, message_id: UUID, role: str) -> None:
        super().__init__(
            f"Message '{message_id}' with role '{role}' must have non-empty content."
        )


class InvalidChatMessageEditError(BusinessRuleViolation):
    """Raised when trying to edit a message that is not from a user."""
    def __init__(self, message_id: UUID, role: str) -> None:
        super().__init__(
            f"Cannot edit message '{message_id}' with role '{role}'. Only USER messages can be edited."
        )

