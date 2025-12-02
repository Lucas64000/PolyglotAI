"""
LearningSession Entity

Represents a learning session (conversation) with the tutor.
Tracks session state, context, and aggregates messages.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from .chat_message import ChatMessage


@dataclass
class LearningSession:
    """
    Represents an active learning session with the AI tutor.
    
    A session:
    - Has a user and learning context
    - Contains a sequence of messages
    - Tracks start/end times
    - May have a specific focus topic
    
    Attributes:
        id: Unique session identifier
        user_id: Reference to the user
        started_at: When the session began
        ended_at: When the session ended (None if active)
        focus_topic: Optional specific topic being practiced
        context_summary: Summary of the conversation context
        messages: List of messages in the session
    
    Examples:
        >>> session = LearningSession(
        ...     user_id=user.id,
        ...     focus_topic="Past tense verbs"
        ... )
        >>> session.is_active
        True
    """
    
    user_id: UUID
    id: UUID = field(default_factory=uuid4)
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ended_at: datetime | None = None
    focus_topic: str | None = None
    context_summary: str | None = None
    messages: list[ChatMessage] = field(default_factory=list[ChatMessage])
    
    @property
    def is_active(self) -> bool:
        """Check if the session is still active."""
        return self.ended_at is None
    
    @property
    def duration_minutes(self) -> float:
        """
        Get session duration in minutes.
        
        Returns current duration if session is active.
        """
        end = self.ended_at or datetime.now(timezone.utc)
        delta = end - self.started_at
        return delta.total_seconds() / 60
    
    @property
    def message_count(self) -> int:
        """Get the number of messages in this session."""
        return len(self.messages)
    
    def add_message(self, message: ChatMessage) -> None:
        """
        Add a message to the session.
        
        Args:
            message: The message to add
            
        Raises:
            ValueError: If session is ended
        """
        if not self.is_active:
            raise ValueError("Cannot add messages to an ended session")
        
        self.messages.append(message)
    
    def end_session(self) -> None:
        """
        End the current session.
        
        Sets the ended_at timestamp if not already set.
        """
        if self.is_active:
            self.ended_at = datetime.now(timezone.utc)
    
    def get_recent_messages(self, count: int = 10) -> list[ChatMessage]:
        """
        Get the most recent messages.
        
        Args:
            count: Maximum number of messages to return
            
        Returns:
            List of recent messages, most recent last
        """
        return self.messages[-count:] if self.messages else []
    
    def get_user_messages(self) -> list[ChatMessage]:
        """Get only user messages from the session."""
        from ..value_objects import Role
        return [m for m in self.messages if m.role == Role.USER]
    
    def get_assistant_messages(self) -> list[ChatMessage]:
        """Get only assistant messages from the session."""
        from ..value_objects import Role
        return [m for m in self.messages if m.role == Role.ASSISTANT]
    
    def __eq__(self, other: object) -> bool:
        """Two sessions are equal if they have the same ID."""
        if not isinstance(other, LearningSession):
            return NotImplemented
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash based on ID."""
        return hash(self.id)
    
    def __repr__(self) -> str:
        status = "active" if self.is_active else "ended"
        return f"LearningSession(id={self.id}, {status}, messages={self.message_count})"
