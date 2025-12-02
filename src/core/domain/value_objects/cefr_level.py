"""
CEFRLevel Value Object

Represents the Common European Framework of Reference for Languages (CEFR) levels.
These are the standard proficiency levels used internationally.
"""

from enum import Enum


class CEFRLevel(str, Enum):
    """
    CEFR (Common European Framework of Reference) proficiency levels.
    
    Levels:
        A1: Breakthrough / Beginner
        A2: Waystage / Elementary  
        B1: Threshold / Intermediate
        B2: Vantage / Upper Intermediate
        C1: Effective Operational Proficiency / Advanced
        C2: Mastery / Proficient
    
    Examples:
        >>> level = CEFRLevel.B1
        >>> level.is_beginner
        False
        >>> level.is_intermediate
        True
        >>> CEFRLevel.A1 < CEFRLevel.B2
        True
    """
    
    A1 = "A1"  # Beginner
    A2 = "A2"  # Elementary
    B1 = "B1"  # Intermediate
    B2 = "B2"  # Upper Intermediate
    C1 = "C1"  # Advanced
    C2 = "C2"  # Proficient/Mastery
    
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
        """Get a human-readable description of the level."""
        descriptions = {
            CEFRLevel.A1: "Beginner - Can understand basic phrases",
            CEFRLevel.A2: "Elementary - Can communicate in simple tasks",
            CEFRLevel.B1: "Intermediate - Can deal with most travel situations",
            CEFRLevel.B2: "Upper Intermediate - Can interact with fluency",
            CEFRLevel.C1: "Advanced - Can express fluently and spontaneously",
            CEFRLevel.C2: "Proficient - Can understand virtually everything",
        }
        return descriptions[self]
    
    @property 
    def numeric_value(self) -> int:
        """
        Get numeric value for comparison (1-6).
        Useful for progress tracking and level comparisons.
        """
        order = [CEFRLevel.A1, CEFRLevel.A2, CEFRLevel.B1, 
                 CEFRLevel.B2, CEFRLevel.C1, CEFRLevel.C2]
        return order.index(self) + 1
    
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, CEFRLevel):
            return NotImplemented
        return self.numeric_value < other.numeric_value
    
    def __le__(self, other: object) -> bool:
        if not isinstance(other, CEFRLevel):
            return NotImplemented
        return self.numeric_value <= other.numeric_value
    
    def __gt__(self, other: object) -> bool:
        if not isinstance(other, CEFRLevel):
            return NotImplemented
        return self.numeric_value > other.numeric_value
    
    def __ge__(self, other: object) -> bool:
        if not isinstance(other, CEFRLevel):
            return NotImplemented
        return self.numeric_value >= other.numeric_value
