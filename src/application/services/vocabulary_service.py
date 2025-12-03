"""
VocabularyService

Service for vocabulary management operations.
"""

from uuid import UUID

from src.core.ports.driven import GraphMemory, VocabularyRepository
from src.core.domain.entities import VocabularyItem
from src.core.domain.value_objects import Language


class VocabularyService:
    """
    Service for vocabulary-related operations.
    
    Coordinates between VocabularyRepository (simple CRUD)
    and GraphMemory (graph relationships).
    """
    
    def __init__(
        self,
        vocabulary_repository: VocabularyRepository,
        graph_memory: GraphMemory,
    ) -> None:
        """
        Initialize with injected dependencies.
        
        Args:
            vocabulary_repository: For CRUD operations
            graph_memory: For graph relationships
        """
        self._vocab_repo = vocabulary_repository
        self._graph_memory = graph_memory
    
    async def add_vocabulary(
        self,
        user_id: UUID,
        term: str,
        definition: str,
        language: Language,
        context_example: str | None = None,
    ) -> VocabularyItem:
        """
        Add a new vocabulary item for the user.
        
        Creates the item in both the repository and graph.
        """
        from src.core.domain.entities import VocabularyItem
        
        # Check if already exists
        existing = await self._vocab_repo.get_by_term(user_id, term, language)
        if existing:
            return existing
        
        # Create new item
        item = VocabularyItem(
            term=term,
            definition=definition,
            language=language,
            context_example=context_example,
        )
        
        # Save to repository
        await self._vocab_repo.save(user_id, item)
        
        # Store in graph with relationships
        await self._graph_memory.store_vocabulary(user_id, item)
        
        return item
    
    async def get_vocabulary(
        self,
        user_id: UUID,
        term: str,
        language: Language,
    ) -> VocabularyItem | None:
        """Get a vocabulary item by term."""
        return await self._vocab_repo.get_by_term(user_id, term, language)
    
    async def get_all_vocabulary(
        self,
        user_id: UUID,
        limit: int = 100,
        offset: int = 0,
    ) -> list[VocabularyItem]:
        """Get all vocabulary for a user."""
        return await self._vocab_repo.get_by_user(user_id, limit, offset)
    
    async def get_review_items(
        self,
        user_id: UUID,
        limit: int = 10,
    ) -> list[VocabularyItem]:
        """Get vocabulary items due for review."""
        return await self._graph_memory.get_vocabulary_for_review(user_id, limit)
    
    async def record_review(
        self,
        user_id: UUID,
        term: str,
        correct: bool,
    ) -> None:
        """Record a vocabulary review result."""
        await self._graph_memory.update_vocabulary_mastery(user_id, term, correct)
