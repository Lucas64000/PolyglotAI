"""
User Entity

Represents an application user (learner).
"""

from __future__ import annotations

from dataclasses import dataclass

from uuid import UUID
from datetime import datetime

from src.core.domain.entities.base import Entity
from src.core.domain.value_objects import (
    Language,
    CEFRLevel,
)
from src.core.exceptions import InvalidLanguagePairError, InvalidLevelChangeError


@dataclass(eq=False, kw_only=True, slots=True)
class User(Entity):
    """
    Represents a registered learner in the application.
    
    Each user has a native language (mother tongue) and a target language
    they are learning. These cannot be the same.
    
    Attributes:
        _native_lang: Language user speaks fluently
        _target_lang: Language user is learning
        _level: Current proficiency level (CEFR)
    """

    _native_lang: Language
    _target_lang: Language
    _level: CEFRLevel

    @property
    def native_lang(self) -> Language:
        """Return the user's native language."""
        return self._native_lang

    @property
    def target_lang(self) -> Language:
        """Return the language the user is learning."""
        return self._target_lang

    @property
    def level(self) -> CEFRLevel:
        """Return the user's current proficiency level."""
        return self._level
 
    @classmethod
    def create_new(
        cls, 
        id: UUID, 
        now: datetime,
        native_lang: Language, 
        target_lang: Language,
        level: CEFRLevel,
    ) -> User:
        """
        Factory method for creating a new user.
        
        Returns:
            User: a new user with different native and target languages
        """
        return cls(
            _id=id,
            _created_at=now,
            _native_lang=native_lang,
            _target_lang=target_lang,
            _level=level
        )
    
    def correct_native_language(self, new_native: Language) -> None:
        """
        Correct the native language.
        
        Ensures the new native language differs from the target language.
        
        Args:
            new_native: The corrected native language
            
        Raises:
            InvalidLanguagePairError: If new native equals target language
        """
        if self.target_lang == new_native:
            raise InvalidLanguagePairError(self.target_lang.code, new_native.code)
        self._native_lang = new_native
         
    def switch_learning_goal(self, new_target: Language) -> None:
        """
        Switch to a different learning goal.
        
        Ensures the new target language differs from the native language.
        
        Args:
            new_target: The new language to learn
            
        Raises:
            InvalidLanguagePairError: If new target equals native language
        """
        if self.native_lang == new_target:
            raise InvalidLanguagePairError(self.native_lang.code, new_target.code)
        self._target_lang = new_target

    def assess_level(self, new_level: CEFRLevel) -> None:
        """
        Update the user's proficiency level.
        
        Only allows changes to adjacent levels (next or previous).
        
        Args:
            new_level: The new proficiency level
            
        Raises:
            InvalidLevelChangeError: If new level is not adjacent to current level
        """
        if not self.level.is_adjacent_to(new_level):
            raise InvalidLevelChangeError(self.level, new_level)
        self._level = new_level

    def __post_init__(self) -> None:
        """Validate user invariants."""
        if self.native_lang == self.target_lang:
            raise InvalidLanguagePairError(self.native_lang.code, self.target_lang.code)

    def __repr__(self) -> str:
        return f"The user speaks {self.native_lang.code} and is learning {self.target_lang.code}"
