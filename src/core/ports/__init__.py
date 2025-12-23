"""
Ports Module

Interfaces that the application uses to communicate
with external infrastructure (AI services, databases, etc.).

The application depends on these interfaces.
Infrastructure provides concrete implementations.
"""

from .chat_provider import ChatProvider
from .repositories import (
    ConversationRepository,
    StudentRepository,
)
from .time_provider import TimeProvider

__all__ = [
    "ChatProvider",
    "ConversationRepository",
    "StudentRepository",
    "TimeProvider",
]
