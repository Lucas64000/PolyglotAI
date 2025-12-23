"""
Test Doubles - Fake, Stub, Mock implementations for testing.

This package contains test doubles organized by type:
- fakes/: Simplified working implementations (e.g., in-memory repositories)
- stubs/: Fixed response providers (e.g., time provider)

Mocks are created directly with unittest.mock in test fixtures.
"""

from .fakes import InMemoryConversationRepository
from .stubs import StubTimeProvider

__all__ = [
    "InMemoryConversationRepository",
    "StubTimeProvider",
]
