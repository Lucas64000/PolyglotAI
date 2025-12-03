"""
Learning DTOs

Data transfer objects for learning-related operations.
"""


from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class VocabularyDTO:
    """DTO for vocabulary items."""
    id: UUID
    term: str
    definition: str
    language: str
    part_of_speech: str | None = None
    context_example: str | None = None
    mastery_level: str = "new"
    stability: float = 0.1
    review_count: int = 0
    last_reviewed: datetime | None = None
    created_at: datetime | None = None


@dataclass  
class ErrorDTO:
    """DTO for user errors."""
    id: UUID
    wrong_form: str
    correction: str
    error_type: str
    explanation: str | None = None
    occurrence_count: int = 1
    is_recurring: bool = False
    is_resolved: bool = False
    last_occurrence: datetime | None = None


@dataclass
class ProgressStats:
    """DTO for learning progress statistics."""
    user_id: UUID
    total_vocabulary: int = 0
    mastered_count: int = 0
    learning_count: int = 0
    familiar_count: int = 0
    new_count: int = 0
    total_errors: int = 0
    resolved_errors: int = 0
    chronic_errors: int = 0
    streak_days: int = 0
    last_activity: datetime | None = None
    
    # Computed properties
    @property
    def mastery_percentage(self) -> float:
        """Percentage of vocabulary mastered."""
        if self.total_vocabulary == 0:
            return 0.0
        return (self.mastered_count / self.total_vocabulary) * 100
    
    @property
    def error_resolution_rate(self) -> float:
        """Percentage of errors resolved."""
        if self.total_errors == 0:
            return 100.0
        return (self.resolved_errors / self.total_errors) * 100
