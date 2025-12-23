"""
Application Ports Package 

Interfaces for read-only query operations.
These interfaces are implemented by infrastructure adapters that provide optimized read operations.
"""

from .conversation_reader import ConversationReader
from .student_reader import StudentReader

__all__ = [
    "ConversationReader",
    "StudentReader",
]