"""
Domain Entities

Entities are objects with a distinct identity that persists over time.
They have a lifecycle and can change state while maintaining their identity.
"""

from .user_profile import UserProfile
from .vocabulary_item import VocabularyItem
from .user_error import UserError
from .grammar_rule import GrammarRule
from .learning_session import LearningSession
from .chat_message import ChatMessage

__all__ = [
    "UserProfile",
    "VocabularyItem",
    "UserError",
    "GrammarRule",
    "LearningSession",
    "ChatMessage",
]
