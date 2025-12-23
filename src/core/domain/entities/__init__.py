"""
Domain Entities

Entities are objects with a distinct identity that persists over time.
"""

from .base import Entity, AggregateRoot
from .conversation import ChatMessage, Conversation
from .student import Student
from .learning import VocabularyItem, VocabularySource

__all__ = [
    "Entity",
    "AggregateRoot",
    "ChatMessage",
    "Conversation",
    "Student",
    "VocabularyItem",
    "VocabularySource",
]