"""
Student Repository Port

Interface for persisting and retrieving student entities.
This port abstracts the database layer for student management.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from src.core.domain import Student
from src.core.exceptions import ResourceNotFoundError

class StudentRepository(ABC):
    """
    Port for student persistence operations.
    """

    @abstractmethod
    async def save(self, student: Student) -> None:
        """
        Persist or update a student in the repository.
        
        Args:
            student: The student entity to save
        """
        ...
    
    @abstractmethod
    async def find_by_id(self, id: UUID) -> Student | None:
        """
        Retrieve a student by its ID with message history.
        
        Args:
            id: The ID of the student to retrieve
            
        Returns:
            The student if found, None otherwise
        """
        ...

    async def get_by_id(self, id: UUID) -> Student:
        """
        Retrieve a student by its ID, raising an exception if not found.
        
        Args:
            id: The ID of the student to retrieve
            
        Returns:
            The student
            
        Raises:
            ResourceNotFoundError: If student is not found
        """
        student = await self.find_by_id(id=id)
        if student is None:
            raise ResourceNotFoundError(resource_type="Student", resource_id=id)
        return student
    
    @abstractmethod
    async def remove(self, id: UUID) -> None:
        """
        Delete a student from the repository.
        
        Args:
            id: The ID of the student to delete
        """
        ...
