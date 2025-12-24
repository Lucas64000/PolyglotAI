"""
Application DTOs Package

Data Transfer Objects for application layer.
Groups commands (write operations) and read models (query operations) by aggregate.
"""

from .conversations import (
    SendMessageCommand,
    SendMessageResult,
    ConversationSummary,
    ListConversationsQuery,
)
from .students import StudentSummary

__all__ = [
    # Conversation DTOs
    "SendMessageCommand",
    "SendMessageResult",
    "ConversationSummary",
    "ListConversationsQuery",
    # Student DTOs
    "StudentSummary",
]