"""
LearningService Port

Interface for learning progress and analytics services.
"""

from abc import abstractmethod
from typing import Any, Protocol
from uuid import UUID

from ...domain.entities import UserError, VocabularyItem


class LearningService(Protocol):
    """
    Interface for learning progress management.
    
    Handles:
    - Vocabulary review scheduling
    - Error pattern analysis
    - Progress statistics
    """
    
    @abstractmethod
    async def get_review_items(
        self,
        user_id: UUID,
        limit: int = 10,
    ) -> list[VocabularyItem]:
        """
        Get vocabulary items due for review.
        
        Uses SRS algorithm to determine which items need practice.
        
        Args:
            user_id: The user's identifier
            limit: Maximum items to return
            
        Returns:
            List of vocabulary items needing review
        """
        ...
    
    @abstractmethod
    async def record_review_result(
        self,
        user_id: UUID,
        term: str,
        correct: bool,
    ) -> VocabularyItem:
        """
        Record the result of a vocabulary review.
        
        Updates the SRS stability based on the result.
        
        Args:
            user_id: The user's identifier
            term: The term that was reviewed
            correct: Whether recall was correct
            
        Returns:
            Updated vocabulary item
        """
        ...
    
    @abstractmethod
    async def get_error_patterns(
        self,
        user_id: UUID,
        limit: int = 10,
    ) -> list[UserError]:
        """
        Get the user's most common error patterns.
        
        Args:
            user_id: The user's identifier
            limit: Maximum errors to return
            
        Returns:
            List of recurring errors, sorted by frequency
        """
        ...
    
    @abstractmethod
    async def get_progress_stats(
        self,
        user_id: UUID,
    ) -> dict[str, Any]:
        """
        Get learning progress statistics.
        
        Returns:
            Dictionary with stats like:
            {
                "total_vocabulary": 150,
                "mastered_count": 45,
                "learning_count": 80,
                "new_count": 25,
                "total_errors": 30,
                "resolved_errors": 20,
                "streak_days": 7,
            }
        """
        ...
    
    @abstractmethod
    async def get_weak_areas(
        self,
        user_id: UUID,
    ) -> list[str]:
        """
        Identify areas where the user needs more practice.
        
        Analyzes error patterns and low-mastery vocabulary
        to suggest focus areas.
        
        Args:
            user_id: The user's identifier
            
        Returns:
            List of topic/area suggestions
        """
        ...
