"""
Status Value Object

Represents the status of a user conversation.
"""

from enum import Enum

class Status(str, Enum):
    """
    Represents the status of a conversation.
    
    Statuses:
        ACTIVE: Conversation is open and accepting new messages
        ARCHIVED: Conversation is read-only and no new messages can be added
        DELETED: Conversation is marked for deletion 
    """
    
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"
    
    @property
    def is_active(self) -> bool:
        """Check if this conversation is active."""
        return self == Status.ACTIVE
    
    @property
    def is_archived(self) -> bool:
        """Check if this conversation is archived."""
        return self == Status.ARCHIVED
    
    @property
    def is_writable(self) -> bool:
        """Check if new messages can be added to this conversation."""
        return self.is_active
