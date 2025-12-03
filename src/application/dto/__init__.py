"""
Data Transfer Objects (DTOs)

DTOs are simple data structures for transferring data
between layers, especially for API requests/responses.
"""

from .chat_dto import ChatRequest, ChatResponse, SessionInfo
from .learning_dto import VocabularyDTO, ErrorDTO, ProgressStats

__all__ = [
    "ChatRequest",
    "ChatResponse", 
    "SessionInfo",
    "VocabularyDTO",
    "ErrorDTO",
    "ProgressStats",
]
