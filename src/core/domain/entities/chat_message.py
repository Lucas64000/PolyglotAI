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
from src.core.exceptions import InvalidChatMessageContentError, InvalidChatMessageEditError

@dataclass(eq=False, kw_only=True, slots=True)
class ChatMessage(Entity):
    """
    Represents a message in a conversation.
    
    Messages are the atomic units of conversation:
    - SYSTEM messages set context/instructions
    - USER messages are learner inputs
    - ASSISTANT messages are tutor responses
    
    Attributes:
        _role: Who sent the message (SYSTEM, USER, ASSISTANT)
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
    def is_from_user(self) -> bool:
        """Check if this message is from the user."""
        return self.role.is_human
    
    @property
    def is_from_assistant(self) -> bool:
        """Check if this message is from the AI assistant."""
        return self.role.is_ai
    
    @property
    def is_system_message(self) -> bool:
        """Check if this is a system message."""
        return self.role.is_system

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
        
        Only USER messages can be edited.
        
        Args:
            new_content: The new content for the message
            
        Raises:
            InvalidChatMessageEditError: If message is not from USER
            InvalidChatMessageContentError: If new content is empty
        """
        if self.role != Role.USER:
            raise InvalidChatMessageEditError(self.id, self.role.value)
        if not new_content:
            raise InvalidChatMessageContentError(self.id, self.role.value)
        self._content = new_content

    def __post_init__(self) -> None:
        """
        Validate the message content based on its role.
        
        System messages may have empty content (they represent prompts),
        but user and assistant messages must have non-empty content.
        
        Raises:
            InvalidChatMessageContentError: If non-system message has no content
        """
        if self.role != Role.SYSTEM and not self.content:
            raise InvalidChatMessageContentError(self.id, self.role.value)
    
    def __repr__(self) -> str:
        return f"[{self.role.value.upper()}]: {self.content}"