"""
Persistence Module

Contains repository implementations:
- In-memory repositories for testing
- Future: SQL repositories
"""

from .in_memory import InMemoryUserRepository, InMemoryVocabularyRepository

__all__ = [
    "InMemoryUserRepository",
    "InMemoryVocabularyRepository",
]
