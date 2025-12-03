"""
VocabularyRepository Port

Interface for vocabulary persistence operations.
Separate from GraphMemory for simple CRUD without graph semantics.
"""

from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from ...domain.entities import VocabularyItem
from ...domain.value_objects import Language


class VocabularyRepository(Protocol):
    """
    Interface for vocabulary data persistence.
    
    This is for simple CRUD operations on vocabulary.
    For graph-based operations (relations, semantic search),
    use GraphMemory instead.
    
    Why both VocabularyRepository and GraphMemory?
        - VocabularyRepository: Simple CRUD, listing, filtering
        - GraphMemory: Graph relationships, semantic search, context
    
    Usage:
        ```python
        # Simple lookup
        items = await vocab_repo.get_by_user(user_id, limit=100)
        
        # For semantic search, use GraphMemory
        context = await graph_memory.get_learning_context(user_id, message)
        ```
    """
    
    @abstractmethod
    async def get_by_id(self, item_id: UUID) -> VocabularyItem | None:
        """
        Retrieve a vocabulary item by ID.
        
        Args:
            item_id: The item's UUID
            
        Returns:
            VocabularyItem if found, None otherwise
        """
        ...
    
    @abstractmethod
    async def get_by_term(
        self,
        user_id: UUID,
        term: str,
        language: Language,
    ) -> VocabularyItem | None:
        """
        Retrieve a vocabulary item by term.
        
        Args:
            user_id: The user's UUID
            term: The term to look up
            language: The language of the term
            
        Returns:
            VocabularyItem if found, None otherwise
        """
        ...
    
    @abstractmethod
    async def get_by_user(
        self,
        user_id: UUID,
        limit: int = 100,
        offset: int = 0,
    ) -> list[VocabularyItem]:
        """
        Get all vocabulary items for a user.
        
        Args:
            user_id: The user's UUID
            limit: Maximum items to return
            offset: Number of items to skip (for pagination)
            
        Returns:
            List of vocabulary items
        """
        ...
    
    @abstractmethod
    async def save(self, user_id: UUID, item: VocabularyItem) -> None:
        """
        Save a vocabulary item (create or update).
        
        Args:
            user_id: The user's UUID
            item: The vocabulary item to save
        """
        ...
    
    @abstractmethod
    async def delete(self, item_id: UUID) -> bool:
        """
        Delete a vocabulary item.
        
        Args:
            item_id: The item's UUID
            
        Returns:
            True if deleted, False if not found
        """
        ...
    
    @abstractmethod
    async def count_by_user(self, user_id: UUID) -> int:
        """
        Count vocabulary items for a user.
        
        Args:
            user_id: The user's UUID
            
        Returns:
            Total count of vocabulary items
        """
        ...
