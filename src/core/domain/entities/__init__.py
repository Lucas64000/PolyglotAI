"""
Domain Entities

Entities are objects with a distinct identity that persists over time.
"""

from .base import Entity
from .chat_message import ChatMessage
from .student import Student
from .conversation import Conversation
from .vocabulary_item import VocabularyItem

__all__ = [
    "Entity",
    "ChatMessage",
    "Student",
    "Conversation",
    "VocabularyItem",
]