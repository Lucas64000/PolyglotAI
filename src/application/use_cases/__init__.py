"""
Use Cases

Atomic application operations representing single user intentions.
Each use case has one responsibility and returns a specific result.
"""

from .process_message import (
    ProcessMessageUseCase,
    ProcessMessageInput,
    ProcessMessageOutput,
)
from .record_vocabulary import RecordVocabularyUseCase
from .retrieve_learning_context import GetLearningContextUseCase
from .track_error import TrackErrorUseCase

__all__ = [
    "ProcessMessageUseCase",
    "ProcessMessageInput",
    "ProcessMessageOutput",
    "RecordVocabularyUseCase",
    "GetLearningContextUseCase",
    "TrackErrorUseCase",
]
