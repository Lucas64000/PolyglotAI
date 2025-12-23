"""
VocabularyItem AggregateRoot

Represents the link between a Student and a learned word (Lexeme).
"""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.core.domain.entities.base import AggregateRoot
from src.core.domain.value_objects import Lexeme


# VO grouped with VocabItem to avoid multiple files 
class VocabularySource(Enum):
    """
    Source classification for vocabulary learning.
    
    Helps track where students encounter and produce vocabulary:
    - STUDENT: New words produced or used by the student in conversation
    - TEACHER: New words introduced by the teacher in explanations or responses
    
    This distinction is useful for adapting teaching strategy and understanding
    which words the student is actively producing versus passively receiving.
    """
    STUDENT = "student"
    TEACHER = "teacher"


@dataclass(eq=False, kw_only=True, slots=True)
class VocabularyItem(AggregateRoot):
    """
    Represents the link between a Student and a Word.
    Tracks progress, mastery, and last review.
    
    Each vocabulary item tracks how many times a word has been reviewed
    and when it was last encountered in a conversation.
    
    Attributes:
        _student_id: Identifier of the student who learned this word
        _lexeme: The word concept being tracked
        _source: Where this vocabulary item was first encountered (STUDENT or TEACHER)
        _last_reviewed_at: Timestamp of the last review/usage
        _review_count: Number of times the word has been reviewed
    """
    
    _student_id: UUID
    _lexeme: Lexeme
    _source: VocabularySource
    _last_reviewed_at: datetime
    _review_count: int = field(default=1)

    @property
    def student_id(self) -> UUID:
        """Return the student ID who owns this vocabulary item."""
        return self._student_id

    @property
    def lexeme(self) -> Lexeme:
        """Return the lexeme being tracked."""
        return self._lexeme
    
    @property
    def source(self) -> VocabularySource:
        """Return who introduced this vocabulary item"""
        return self._source

    @property
    def last_reviewed_at(self) -> datetime:
        """Return the timestamp of the last review."""
        return self._last_reviewed_at

    @property
    def review_count(self) -> int:
        """Return the number of times this item has been reviewed."""
        return self._review_count

    @classmethod
    def create_new(
        cls,
        id: UUID,
        now: datetime,
        student_id: UUID,
        lexeme: Lexeme,
        source: VocabularySource,
    ) -> VocabularyItem:
        """
        Factory method for creating a new vocabulary item.
        
        Returns:
            VocabularyItem: a new vocabulary item with initial review count of 1
        """
        return cls(
            _id=id,
            _created_at=now,
            _student_id=student_id,
            _lexeme=lexeme,
            _source=source,
            _last_reviewed_at=now,
            _review_count=1,
        )

    def mark_as_reviewed(self, now: datetime) -> None:
        """
        Mark the item as reviewed.
        
        Increments review count and updates the last_reviewed_at timestamp.
        """
        self._review_count += 1
        self._last_reviewed_at = now