"""
UserProfile Entity

Represents a learner in the system with their learning preferences and progress.
This is the aggregate root for user-related operations.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from ..value_objects import CEFRLevel, Language, LanguagePair

@dataclass
class UserProfile:
    """
    Represents a language learner's profile.
    
    This entity tracks:
    - User identity
    - Language learning direction (native -> target)
    - Current proficiency level
    - Learning preferences
    
    Attributes:
        id: Unique identifier
        language_pair: The learning direction (source=native, target=learning)
        current_level: Current CEFR proficiency level
        display_name: Optional display name
        created_at: When the profile was created
        updated_at: When the profile was last updated
    
    Examples:
        >>> from polyglot_ai.core.domain.value_objects import (
        ...     LanguagePair, Language, CEFRLevel
        ... )
        >>> profile = UserProfile(
        ...     language_pair=LanguagePair.french_to_english(),
        ...     current_level=CEFRLevel.B1,
        ...     display_name="Marie"
        ... )
    """
    
    language_pair: LanguagePair
    current_level: CEFRLevel
    id: UUID = field(default_factory=uuid4)
    display_name: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def update_level(self, new_level: CEFRLevel) -> None:
        """
        Update the user's proficiency level.
        
        Args:
            new_level: The new CEFR level
        """
        self.current_level = new_level
        self._touch()
    
    @property
    def native_language(self) -> Language:
        """Get the user's native language."""
        return self.language_pair.source
    
    @property
    def target_language(self) -> Language:
        """Get the language being learned."""
        return self.language_pair.target
    
    @property
    def is_beginner(self) -> bool:
        """Check if user is at beginner level (A1-A2)."""
        return self.current_level.is_beginner
    
    @property
    def is_intermediate(self) -> bool:
        """Check if user is at intermediate level (B1-B2)."""
        return self.current_level.is_intermediate
    
    @property
    def is_advanced(self) -> bool:
        """Check if user is at advanced level (C1-C2)."""
        return self.current_level.is_advanced
    
    def _touch(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(timezone.utc)
    
    def __eq__(self, other: object) -> bool:
        """Two profiles are equal if they have the same ID."""
        if not isinstance(other, UserProfile):
            return NotImplemented
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash based on ID for use in sets/dicts."""
        return hash(self.id)
