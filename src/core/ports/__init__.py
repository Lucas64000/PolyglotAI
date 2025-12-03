"""
Ports Module

Ports define the boundaries of the application.
They are interfaces (protocols) that specify contracts between layers.

Types of Ports:
- Driven (Secondary): How the application talks to infrastructure
  (databases, AI providers, external services)
- Driving (Primary): How the outside world talks to the application
  (API endpoints, CLI commands, event handlers)
"""

from .driven import (
    # AI Interfaces
    AIProviderFactory,
    ChatModel,
    Embedder,
    # Storage Interfaces
    GraphMemory,
    UserRepository,
    VocabularyRepository,
)
from .driver import (
    ChatService,
    LearningService,
)

__all__ = [
    # Driven (Infrastructure)
    "AIProviderFactory",
    "ChatModel",
    "Embedder",
    "GraphMemory",
    "UserRepository",
    "VocabularyRepository",
    # Driving (API)
    "ChatService",
    "LearningService",
]
