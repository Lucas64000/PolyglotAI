"""
Application Ports Package 

Interfaces for read-only query operations.
These interfaces are implemented by infrastructure adapters that provide optimized read operations.
"""

from .conversations import ConversationReader
from .students import StudentReader

__all__ = [
    "ConversationReader",
    "StudentReader",
]