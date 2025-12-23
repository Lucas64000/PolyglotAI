"""
CEFRLevel Value Object

Represents the Common European Framework of Reference for Languages (CEFR) levels.
These are the standard proficiency levels used internationally.
"""

from __future__ import annotations

from functools import total_ordering, lru_cache
from enum import Enum

@total_ordering
class CEFRLevel(Enum):
    """
    Common European Framework of Reference for Languages levels.
    
    Levels are ordered from beginner (A1) to proficient (C2).
    Supports comparison operations (e.g., CEFRLevel.B1 < CEFRLevel.B2).
    
    Levels:
        A1: Beginner
        A2: Elementary
        B1: Intermediate
        B2: Upper Intermediate
        C1: Advanced
        C2: Proficient
    """
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"

    @classmethod
    @lru_cache(maxsize=1) 
    def _get_ordered_members(cls) -> tuple[CEFRLevel, ...]:
        """
        Return all levels as tuple and cache it.
        """
        return tuple(cls)

    @property
    def is_beginner(self) -> bool:
        """Check if this is a beginner level (A1-A2)."""
        return self in (CEFRLevel.A1, CEFRLevel.A2)
    
    @property
    def is_intermediate(self) -> bool:
        """Check if this is an intermediate level (B1-B2)."""
        return self in (CEFRLevel.B1, CEFRLevel.B2)
    
    @property
    def is_advanced(self) -> bool:
        """Check if this is an advanced level (C1-C2)."""
        return self in (CEFRLevel.C1, CEFRLevel.C2)

    @property
    def description(self) -> str:
        """Get a description of the level."""
        descriptions = {
            CEFRLevel.A1: "Beginner - Can understand basic phrases",
            CEFRLevel.A2: "Elementary - Can communicate in simple tasks",
            CEFRLevel.B1: "Intermediate - Can deal with most travel situations",
            CEFRLevel.B2: "Upper Intermediate - Can interact with fluency",
            CEFRLevel.C1: "Advanced - Can express fluently and spontaneously",
            CEFRLevel.C2: "Proficient - Can understand everything",
        }
        return descriptions[self]

    @property
    def rank(self) -> int:
        """
        Get numeric value for comparison (1-6).
        Useful for progress tracking and level comparisons.
        """
        return self._get_ordered_members().index(self) + 1

    def is_adjacent_to(self, other: CEFRLevel) -> bool:
        """Verify the other rank is adjacent to this one."""
        return abs(self.rank - other.rank) == 1

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, CEFRLevel):
            return NotImplemented
        return self.rank < other.rank