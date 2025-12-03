"""
These interfaces define how the outside world 
interacts with the application layer.

External systems call these interfaces.
Application layer provides implementations.
"""

from .chat_service import ChatService
from .learning_service import LearningService

__all__ = [
    "ChatService",
    "LearningService",
]
