"""
These interfaces define how the application layer communicates
with external infrastructure (AI services, databases, etc.).

The application depends on these interfaces.
Infrastructure provides concrete implementations.
"""

from .ai_provider_factory import AIProviderFactory
from .chat_model import ChatModel
from .embedder import Embedder
from .graph_memory import GraphMemory
from .user_repository import UserRepository
from .vocabulary_repository import VocabularyRepository

__all__ = [
    "AIProviderFactory",
    "ChatModel", 
    "Embedder",
    "GraphMemory",
    "UserRepository",
    "VocabularyRepository",
]
