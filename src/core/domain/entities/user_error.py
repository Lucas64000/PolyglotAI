"""
UserError Entity

Represents a specific linguistic error made by a user.
Tracks error patterns for personalized feedback and targeted practice.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from ..value_objects import ErrorType, Language


@dataclass
class UserError:
    """
    Represents a linguistic error made by a learner.
    
    This entity tracks:
    - The exact incorrect form used
    - The correct form
    - Why it was wrong (explanation)
    - Error category for pattern analysis
    - Frequency of occurrence
    
    Corresponds to the Mistake node in the graph ontology,
    with additional domain logic for error analysis.
    
    Attributes:
        id: Unique identifier
        user_id: Reference to the user who made the error
        wrong_form: The exact incorrect text segment
        correction: The correct form
        error_type: Category of error (GRAMMAR, SPELLING, etc.)
        explanation: Why it's wrong (pedagogical)
        language: Language where the error occurred
        occurrence_count: How many times this error was made
        first_occurrence: When error was first made
        last_occurrence: Most recent occurrence
        is_resolved: Whether user has stopped making this error
    
    Examples:
        >>> from polyglot_ai.core.domain.value_objects import ErrorType, Language
        >>> error = UserError(
        ...     user_id=user.id,
        ...     wrong_form="I goed to the store",
        ...     correction="I went to the store",
        ...     error_type=ErrorType.CONJUGATION,
        ...     explanation="'Go' is an irregular verb. Past tense is 'went', not 'goed'.",
        ...     language=Language.english()
        ... )
    """
    
    user_id: UUID
    wrong_form: str
    correction: str
    error_type: ErrorType
    language: Language
    id: UUID = field(default_factory=uuid4)
    explanation: str | None = None
    related_rule: str | None = None  # Link to GrammarRule name
    occurrence_count: int = 1
    first_occurrence: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_occurrence: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_resolved: bool = False
    
    def __post_init__(self) -> None:
        """Validate the error."""
        if not self.wrong_form or not self.wrong_form.strip():
            raise ValueError("Wrong form cannot be empty")
        if not self.correction or not self.correction.strip():
            raise ValueError("Correction cannot be empty")
        if self.wrong_form.strip().lower() == self.correction.strip().lower():
            raise ValueError("Wrong form and correction cannot be identical")
        
        self.wrong_form = self.wrong_form.strip()
        self.correction = self.correction.strip()
    
    def record_occurrence(self) -> None:
        """
        Record another occurrence of this error.
        
        Increments the count and updates last_occurrence timestamp.
        Also marks as unresolved if it was previously resolved.
        """
        self.occurrence_count += 1
        self.last_occurrence = datetime.now(timezone.utc)
        self.is_resolved = False
    
    def mark_resolved(self) -> None:
        """
        Mark this error as resolved.
        
        Called when the user consistently uses the correct form.
        """
        self.is_resolved = True
    
    @property
    def is_recurring(self) -> bool:
        """
        Check if this is a recurring error (made more than once).
        
        Recurring errors may need special attention in lessons.
        """
        return self.occurrence_count > 1
    
    @property
    def is_chronic(self) -> bool:
        """
        Check if this is a chronic error (made many times).
        
        Chronic errors (5+ occurrences) indicate a fundamental
        misunderstanding that needs explicit instruction.
        """
        return self.occurrence_count >= 5
    
    @property
    def days_since_last_occurrence(self) -> int:
        """Get days since the last time this error was made."""
        now = datetime.now(timezone.utc)
        return (now - self.last_occurrence).days
    
    @property
    def might_be_resolved(self) -> bool:
        """
        Heuristic to check if error might be resolved.
        
        If the user hasn't made this error in 14+ days,
        they might have learned the correct form.
        """
        return self.days_since_last_occurrence >= 14 and not self.is_resolved
    
    def __eq__(self, other: object) -> bool:
        """Two errors are equal if they have the same ID."""
        if not isinstance(other, UserError):
            return NotImplemented
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash based on ID."""
        return hash(self.id)
    
    def __repr__(self) -> str:
        return (
            f"UserError({self.wrong_form!r} -> {self.correction!r}, "
            f"type={self.error_type.value}, count={self.occurrence_count})"
        )
