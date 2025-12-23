"""
ChatMessage Entity

Represents a single message in a learning conversation.
"""

from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass
from uuid import UUID

from src.core.domain.entities.base import Entity
from src.core.domain.value_objects import Role
from src.core.exceptions import InvalidChatMessageContentError

@dataclass(eq=False, kw_only=True, slots=True)
class ChatMessage(Entity):
    """
    Represents a message in a conversation.
    
    Messages are the atomic units of conversation:
    - STUDENT messages are student inputs
    - TEACHER messages are teacher responses
    
    Attributes:
        _role: Who sent the message (STUDENT, TEACHER)
        _content: The content of the message
    """
    
    _role: Role
    _content: str
    
    @property
    def role(self) -> Role:
        """Return the message sender role."""
        return self._role
    
    @property
    def content(self) -> str:
        """Return the message content."""
        return self._content

    @property
    def is_from_student(self) -> bool:
        """Check if this message is from the student."""
        return self.role.is_student
    
    @property
    def is_from_teacher(self) -> bool:
        """Check if this message is from the teacher."""
        return self.role.is_teacher

    @classmethod
    def create_new(
        cls, 
        id: UUID, 
        role: Role, 
        content: str, 
        now: datetime
    ) -> ChatMessage:
        """
        Factory method for creating a new chat message withing a conversation.
        
        Returns:
            ChatMessage: a new message within a conversation
        """
        return cls(
            _id=id,
            _role=role,
            _content=content,
            _created_at=now
        )
    
    def edit_content(self, new_content: str) -> None:
        """
        Edit the content of this message.
        
        Args:
            new_content: The new content for the message
            
        Raises:
            InvalidChatMessageContentError: If the new content is empty
        """
        self._validate_content(new_content)
        self._content = new_content

    def _validate_content(self, content: str) -> None:
        """
        Validate the content of a message.

        Messages cannot be empty.

        Args:
            content: The content of the message

        Raises:
            InvalidChatMessageContentError: If the content is empty
        """
        if not content or not content.strip():
            raise InvalidChatMessageContentError()

    def __post_init__(self) -> None:
        """
        Validate the message.
        
        Raises:
            InvalidChatMessageContentError: If the message has no content
        """
        self._validate_content(self.content)
    
    def __repr__(self) -> str:
        return f"[{self.role.value.upper()}]: {self.content}"