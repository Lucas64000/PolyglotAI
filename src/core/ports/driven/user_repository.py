"""
UserRepository Port

Interface for user persistence operations.
"""

from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from ...domain.entities import UserProfile


class UserRepository(Protocol):
    """
    Interface for user data persistence.
    
    Abstracts away the storage mechanism for user profiles.
    Could be implemented with:
    - In-memory storage (for testing)
    - PostgreSQL
    - MongoDB
    - etc.
    
    Usage:
        ```python
        # In a use case
        user = await user_repository.get_by_id(user_id)
        if not user:
            raise EntityNotFoundError("User", str(user_id))
        ```
    """
    
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> UserProfile | None:
        """
        Retrieve a user by their unique identifier.
        
        Args:
            user_id: The user's UUID
            
        Returns:
            UserProfile if found, None otherwise
        """
        ...
    
    @abstractmethod
    async def save(self, user: UserProfile) -> None:
        """
        Save a user profile (create or update).
        
        Args:
            user: The user profile to save
        """
        ...
    
    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """
        Delete a user profile.
        
        Args:
            user_id: The user's UUID
            
        Returns:
            True if deleted, False if not found
        """
        ...
    
    @abstractmethod
    async def exists(self, user_id: UUID) -> bool:
        """
        Check if a user exists.
        
        Args:
            user_id: The user's UUID
            
        Returns:
            True if exists, False otherwise
        """
        ...
