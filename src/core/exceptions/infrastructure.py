"""
Infrastructure Exceptions

Exceptions defining contracts for infrastructure layer failures.
The Core defines contracts for what can go wrong (e.g. "Teacher response unavailable"),
while Adapters map specific library errors (e.g. OpenAI RateLimitError) to these exception classes.
"""

from .base import InfrastructureError

class ExternalServiceError(InfrastructureError):
    """Raised when an external API or service fails."""


class ChatProviderError(ExternalServiceError):
    """Base error for chat provider failures."""


class TeacherResponseError(ChatProviderError):
    """
    Raised when the teacher fails to provide a response.
    """
    def __init__(self, cause: str) -> None:
        super().__init__(f"Unable to provide the teacher's response: {cause}")


class PersistenceError(InfrastructureError):
    """Raised when data cannot be persisted to the storage mechanism."""
    pass