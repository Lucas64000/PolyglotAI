"""
VocabularyItem Entity

Represents the link between a Student and a learned word (Lexeme).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.core.domain.entities.base import Entity
from src.core.domain.value_objects import Lexeme


@dataclass(eq=False, kw_only=True, slots=True)
class VocabularyItem(Entity):
    """
    Represents the link between a Student and a Word.
    Tracks progress, mastery, and last review.
    
    Each vocabulary item tracks how many times a word has been reviewed
    and when it was last encountered in a conversation.
    
    Attributes:
        _student_id: Identifier of the student who learned this word
        _lexeme: The word concept being tracked
        _last_reviewed_at: Timestamp of the last review/usage
        _review_count: Number of times the word has been reviewed
    """
    
    _student_id: UUID
    _lexeme: Lexeme
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