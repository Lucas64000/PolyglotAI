"""
Conversation Repository Port

Interface for persisting and retrieving conversation entities.
This port abstracts the database layer for conversation management.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from src.core.domain import Conversation
from src.core.exceptions import ResourceNotFoundError

class ConversationRepository(ABC):
    """
    Port for conversation persistence operations.
    """

    @abstractmethod
    async def save(self, conversation: Conversation) -> None:
        """
        Persist or update a conversation in the repository.
        
        Args:
            conversation: The conversation entity to save
        """
        ...
    
    @abstractmethod
    async def find_by_id(self, id: UUID) -> Conversation | None:
        """
        Retrieve a conversation by its ID with message history.
        
        Args:
            id: The ID of the conversation to retrieve
            
        Returns:
            The conversation if found, None otherwise
        """
        ...

    async def get_by_id(self, id: UUID) -> Conversation:
        """
        Retrieve a conversation by its ID, raising an exception if not found.
        
        Args:
            id: The ID of the conversation to retrieve
            
        Returns:
            The conversation
            
        Raises:
            ResourceNotFoundError: If conversation is not found
        """
        conv = await self.find_by_id(id=id)
        if conv is None:
            raise ResourceNotFoundError(resource_type="Conversation", resource_id=id)
        return conv
    
    @abstractmethod
    async def remove(self, id: UUID) -> None:
        """
        Delete a conversation from the repository.
        
        Args:
            id: The ID of the conversation to delete
        """
        ...
