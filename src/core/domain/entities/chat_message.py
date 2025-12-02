"""
ChatMessage Entity

Represents a single message in a learning conversation.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from ..value_objects import Role


@dataclass
class ChatMessage:
    """
    Represents a message in a conversation.
    
    Messages are the atomic units of conversation:
    - SYSTEM messages set context/instructions
    - USER messages are learner inputs
    - ASSISTANT messages are tutor responses
    
    Attributes:
        id: Unique message identifier
        session_id: Reference to the learning session
        role: Who sent the message (SYSTEM, USER, ASSISTANT)
        content: The text content of the message
        timestamp: When the message was sent
        metadata: Optional additional data (API response info, etc.)
    
    Examples:
        >>> from src.core.domain.value_objects import Role
        >>> msg = ChatMessage(
        ...     session_id=session.id,
        ...     role=Role.USER,
        ...     content="How do I use the present perfect tense?"
        ... )
    """
    
    session_id: UUID
    role: Role
    content: str
    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict[str, Any])
    
    def __post_init__(self) -> None:
        """Validate the message."""
        # Allow empty content only for system messages
        from ..value_objects import Role
        
        if self.role != Role.SYSTEM and not self.content:
            raise ValueError("Message content cannot be empty")
    
    @property
    def is_from_user(self) -> bool:
        """Check if this message is from the user."""
        return self.role.is_human()
    
    @property
    def is_from_assistant(self) -> bool:
        """Check if this message is from the AI assistant."""
        return self.role.is_ai()
    
    @property
    def is_system_message(self) -> bool:
        """Check if this is a system message."""
        return self.role.is_system()
    
    @property
    def word_count(self) -> int:
        """Get the approximate word count of the message."""
        return len(self.content.split())
    
    def to_dict(self) -> dict[str, str]:
        """
        Convert to a simple dict format for LLM APIs.
        
        Returns:
            Dict with 'role' and 'content' keys
        """
        return {
            "role": self.role.value,
            "content": self.content,
        }
    
    def __eq__(self, other: object) -> bool:
        """Two messages are equal if they have the same ID."""
        if not isinstance(other, ChatMessage):
            return NotImplemented
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash based on ID."""
        return hash(self.id)
    
    def __repr__(self) -> str:
        content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"ChatMessage(role={self.role.value}, content={content_preview!r})"
