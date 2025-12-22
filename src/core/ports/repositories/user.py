"""
User Repository Port

Interface for persisting and retrieving user entities.
This port abstracts the database layer for user management.
"""

from typing import Protocol
from uuid import UUID

from src.core.domain import (
    User, 
)


class UserRepository(Protocol):
    """
    Port for user persistence operations.
    """

    async def save_user(self, user: User) -> None:
        """
        Persist or update a user in the repository.
        
        Args:
            user: The user entity to save
        """
        ...
    
    async def find_user_by_id(self, user_id: UUID) -> User | None:
        """
        Retrieve a user by their ID.
        
        Args:
            user_id: The ID of the user to retrieve
            
        Returns:
            The user if found, None otherwise
        """
        ...

    async def remove_user(self, user_id: UUID) -> None:
        """
        Delete a user from the repository.
        
        Args:
            user_id: The ID of the user to delete
        """
        ...