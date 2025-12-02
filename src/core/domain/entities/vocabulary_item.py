"""
VocabularyItem Entity

Represents a vocabulary word/phrase that a user is learning.
Tracks the term, its definition, and the user's mastery progress.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from ..value_objects import Language, MasteryLevel, PartOfSpeech


@dataclass
class VocabularyItem:
    """
    Represents a vocabulary item being learned.
    
    This entity combines:
    - The term itself (in target language)
    - Its translation/definition (in native language)  
    - Learning metadata (mastery, review schedule)
    - Contextual information (usage, examples)
    
    Corresponds to Vocabulary + Definition nodes in the graph ontology,
    but provides a richer domain model for application logic.
    
    Attributes:
        id: Unique identifier
        term: The word/phrase in the target language (lemma form)
        definition: Translation or definition in native language
        language: Language of the term (ISO code)
        part_of_speech: Grammatical category (NOUN, VERB, etc.)
        context_example: Example sentence showing usage
        mastery_level: Current learning progress
        stability: SRS stability value (0.0-1.0)
        last_reviewed: When the item was last reviewed
        review_count: Number of times reviewed
        created_at: When first learned
    
    Examples:
        >>> from polyglot_ai.core.domain.value_objects import (
        ...     Language, MasteryLevel, PartOfSpeech
        ... )
        >>> vocab = VocabularyItem(
        ...     term="ubiquitous",
        ...     definition="omniprésent, que l'on trouve partout",
        ...     language=Language.english(),
        ...     part_of_speech=PartOfSpeech.ADJ,
        ...     context_example="Smartphones have become ubiquitous."
        ... )
    """
    
    term: str
    definition: str
    language: Language
    id: UUID = field(default_factory=uuid4)
    part_of_speech: PartOfSpeech | None = None
    context_example: str | None = None
    context_usage: str | None = None  # e.g., "Formal", "Slang", "Technical"
    stability: float = field(default=0.1)  # SRS stability (0.0-1.0)
    last_reviewed: datetime | None = None
    review_count: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def __post_init__(self) -> None:
        """Validate the vocabulary item."""
        if not self.term or not self.term.strip():
            raise ValueError("Term cannot be empty")
        if not self.definition or not self.definition.strip():
            raise ValueError("Definition cannot be empty")
        if not 0.0 <= self.stability <= 1.0:
            raise ValueError(f"Stability must be between 0.0 and 1.0, got {self.stability}")
        
        self.term = self.term.strip().lower()
        self.definition = self.definition.strip()
    
    @property
    def mastery_level(self) -> MasteryLevel:
        """
        Get the mastery level based on stability.
        
        Returns:
            MasteryLevel derived from the stability value
        """
        from ..value_objects import MasteryLevel
        return MasteryLevel.from_stability(self.stability)
    
    @property
    def needs_review(self) -> bool:
        """
        Check if this item needs to be reviewed.
        
        Simple heuristic: needs review if not mastered or 
        hasn't been reviewed recently.
        """
        from ..value_objects import MasteryLevel
        
        if self.mastery_level == MasteryLevel.NEW:
            return True
        if self.last_reviewed is None:
            return True
        
        # Calculate days since last review
        now = datetime.now(timezone.utc)
        days_since_review = (now - self.last_reviewed).days
        
        # Review intervals based on mastery
        intervals = {
            MasteryLevel.NEW: 0,
            MasteryLevel.LEARNING: 1,
            MasteryLevel.FAMILIAR: 7,
            MasteryLevel.MASTERED: 30,
        }
        
        return days_since_review >= intervals[self.mastery_level]
    
    def record_review(self, correct: bool) -> None:
        """
        Record a review of this vocabulary item.
        
        Updates stability based on whether the review was correct.
        Uses a simplified SRS algorithm.
        
        Args:
            correct: Whether the user recalled the item correctly
        """
        self.review_count += 1
        self.last_reviewed = datetime.now(timezone.utc)
        
        if correct:
            # Increase stability (but cap at 1.0)
            self.stability = min(1.0, self.stability + 0.15)
        else:
            # Decrease stability (but keep above 0.1)
            self.stability = max(0.1, self.stability - 0.2)
    
    def __eq__(self, other: object) -> bool:
        """Two vocabulary items are equal if they have the same ID."""
        if not isinstance(other, VocabularyItem):
            return NotImplemented
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash based on ID."""
        return hash(self.id)
    
    def __repr__(self) -> str:
        return (
            f"VocabularyItem(term={self.term!r}, "
            f"mastery={self.mastery_level.value})"
        )
