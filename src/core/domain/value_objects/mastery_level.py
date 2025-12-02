"""
MasteryLevel Value Object

Represents the learner's mastery level for a vocabulary item or grammar rule.
Based on Spaced Repetition System (SRS) principles.
"""

from __future__ import annotations

from enum import Enum


class MasteryLevel(str, Enum):
    """
    Represents the learner's mastery of a concept.
    
    Based on SRS (Spaced Repetition System) stages:
    - NEW: Just encountered, needs immediate review
    - LEARNING: In active learning phase, frequent reviews
    - FAMILIAR: Known but needs occasional review
    - MASTERED: Well-known, rare reviews needed
    
    Maps to stability values in the graph:
    - NEW: stability 0.0-0.25
    - LEARNING: stability 0.25-0.5
    - FAMILIAR: stability 0.5-0.75
    - MASTERED: stability 0.75-1.0
    """
    
    NEW = "new"
    LEARNING = "learning"
    FAMILIAR = "familiar"
    MASTERED = "mastered"
    
    @classmethod
    def from_stability(cls, stability: float) -> MasteryLevel:
        """
        Convert a numeric stability value to a MasteryLevel.
        
        Args:
            stability: Float between 0.0 and 1.0
            
        Returns:
            Corresponding MasteryLevel
            
        Examples:
            >>> MasteryLevel.from_stability(0.1)
            <MasteryLevel.NEW: 'new'>
            >>> MasteryLevel.from_stability(0.8)
            <MasteryLevel.MASTERED: 'mastered'>
        """
        if stability < 0.0 or stability > 1.0:
            raise ValueError(f"Stability must be between 0.0 and 1.0, got {stability}")
        
        if stability < 0.25:
            return cls.NEW
        elif stability < 0.5:
            return cls.LEARNING
        elif stability < 0.75:
            return cls.FAMILIAR
        else:
            return cls.MASTERED
    
    @property
    def stability_range(self) -> tuple[float, float]:
        """Get the stability range for this mastery level."""
        ranges = {
            MasteryLevel.NEW: (0.0, 0.25),
            MasteryLevel.LEARNING: (0.25, 0.5),
            MasteryLevel.FAMILIAR: (0.5, 0.75),
            MasteryLevel.MASTERED: (0.75, 1.0),
        }
        return ranges[self]
    
    @property
    def review_priority(self) -> int:
        """
        Get review priority (higher = needs review sooner).
        
        Returns:
            Priority from 1 (low) to 4 (high)
        """
        priorities = {
            MasteryLevel.MASTERED: 1,
            MasteryLevel.FAMILIAR: 2,
            MasteryLevel.LEARNING: 3,
            MasteryLevel.NEW: 4,
        }
        return priorities[self]
    
    def __lt__(self, other: object) -> bool:
        """Compare mastery levels (NEW < LEARNING < FAMILIAR < MASTERED)."""
        if not isinstance(other, MasteryLevel):
            return NotImplemented
        order = [MasteryLevel.NEW, MasteryLevel.LEARNING, 
                 MasteryLevel.FAMILIAR, MasteryLevel.MASTERED]
        return order.index(self) < order.index(other)
