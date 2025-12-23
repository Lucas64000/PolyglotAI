"""
Base Entity Class

Defines the contract for all domain entities.
Entities are uniquely identified by their ID, not their attributes.
"""

from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass(kw_only=True, slots=True)
class Entity:
    """
    Abstract base class for all Domain Entities.
    
    Entities are objects with a unique identity that persists over time,
    regardless of changes to their attributes. They are compared by ID,
    not by their state.
    
    Attributes:
        _id: Unique identifier for this entity instance
        _created_at: Timestamp when the entity was created
    """
    _id: UUID
    _created_at: datetime

    @property
    def id(self) -> UUID:
        """Get the unique identifier of this entity."""
        return self._id
    
    @property
    def created_at(self) -> datetime:
        """Get the creation timestamp of this entity."""
        return self._created_at

    def __eq__(self, other: object) -> bool:
        """
        Entities are equal if they are of the same type and have the same id.
        
        This ensures that two different instances of the same entity
        (with the same ID) are considered equal.
        """
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """
        Hash based on identity (ID), allowing entities to be used in sets and as dict keys.
        """
        return hash(self.id)
    
    
class AggregateRoot(Entity):
    pass