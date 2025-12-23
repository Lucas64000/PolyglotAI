"""
Fakes - Simplified working implementations for testing.

Fakes have real logic but use simplified storage (in-memory instead of database).
They respect the same contracts as real implementations.
"""

from .in_memory_conversation_repository import InMemoryConversationRepository

__all__ = ["InMemoryConversationRepository"]
