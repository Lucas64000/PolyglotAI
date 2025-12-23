"""
Conversation Entity

Represents a conversation thread between a student and the teacher.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.core.domain.entities.base import Entity
from src.core.domain.entities.chat_message import ChatMessage
from src.core.domain.value_objects import Status, Role
from src.core.exceptions import ConversationNotWritableError, EmptyConversationTitleError, ConversationTitleTooLongError


@dataclass(eq=False, kw_only=True, slots=True)
class Conversation(Entity):
    """
    Represents a learning conversation between a student and the teacher.
    
    A conversation groups related messages and tracks their lifecycle.
    Conversations can be ACTIVE (editable), ARCHIVED (read-only), or DELETED.

    Attributes:
        _student_id: Identifier of the conversation owner (student)
        _title: Title of the conversation
        _status: Current conversation status (ACTIVE, ARCHIVED, DELETED)
        _messages: History of the conversation
        _last_activity_at: Timestamp of the last activity (message addition or status change)
    """

    _student_id: UUID
    _last_activity_at: datetime
    _title: str = field(default_factory=lambda: "Conversation")
    _status: Status = field(default_factory=lambda: Status.ACTIVE)
    _messages: list[ChatMessage] = field(default_factory=list) # type: ignore

    @property
    def student_id(self) -> UUID:
        """Return the conversation owner's ID."""
        return self._student_id
    
    @property
    def title(self) -> str:
        """Return the conversation title."""
        return self._title
    
    @property
    def last_activity_at(self) -> datetime:
        """Return the timestamp of the last activity."""
        return self._last_activity_at
    
    @property
    def status(self) -> Status:
        """Return the conversation status."""
        return self._status

    @property
    def messages(self) -> tuple[ChatMessage, ...]:
        """Return an immutable view of the conversation messages."""
        return tuple(self._messages)
        
    @property
    def message_count(self) -> int:
        """Return the total number of messages in this conversation."""
        return len(self.messages)

    @classmethod
    def create_new(
        cls, id: UUID, 
        student_id: UUID, 
        now: datetime, 
        title: str = "Conversation"
    ) -> Conversation:
        """
        Factory method for creating a new, empty, and active conversation.
        
        Args:
            id: Unique identifier for the conversation
            student_id: Identifier of the conversation owner
            now: Current timestamp for creation
            title: Title of the conversation (defaults to "Conversation")
        
        Returns:
            Conversation: a new conversation with empty messages and ACTIVE status
            
        Raises:
            EmptyConversationTitleError: if title is empty
            ConversationTitleTooLongError: if title is too long
        """
        cleaned_title = title.strip()
        if not cleaned_title:
            raise EmptyConversationTitleError(id)
        
        max_len = 100
        if len(cleaned_title) > max_len:
            raise ConversationTitleTooLongError(id, len(cleaned_title), max_len)

        return cls(
            _id=id,
            _student_id=student_id, 
            _created_at=now,
            _last_activity_at=now,
            _title=cleaned_title,
        )
    
    def add_message(self, new_message_id: UUID, now: datetime, role: Role, content: str) -> ChatMessage:
        """
        Create a message within this conversation context.

        Raises:
            ConversationNotWritableError: if the conversation is not writable (ARCHIVED or DELETED)

        Returns: 
            ChatMessage: a message within the conversation
        """
        if not self.status.is_writable:
            raise ConversationNotWritableError(self.id, self.status.value)
            
        self.touch(now)

        message = ChatMessage.create_new(
            id=new_message_id,
            role=role,
            content=content,
            now=now
        )

        self._messages.append(message)
        return message

    def touch(self, now: datetime) -> None:
        """
        Update the last activity timestamp.
        
        Args:
            now: Current timestamp
        """
        self._last_activity_at = now

    def archive(self, now: datetime) -> None:
        """
        Archive the conversation.
        
        Archived conversations are read-only and cannot accept new messages.
        
        Args:
            now: Current timestamp
        """
        self._status = Status.ARCHIVED
        self.touch(now)

    def delete(self, now: datetime) -> None:
        """
        Delete the conversation.
        
        Deleted conversations are not accessible and cannot accept new messages.
        
        Args:
            now: Current timestamp
        """
        self._status = Status.DELETED
        self.touch(now)

    def modify_title(self, new_title: str, now: datetime) -> None:
        """
        Modify the conversation title.
        
        Raises:
            ConversationNotWritableError: if the conversation is not writable (ARCHIVED or DELETED)
            EmptyConversationTitleError: if the title is empty after stripping
            ConversationTitleTooLongError: if the title is longer than max_len characters
        
        Args:
            new_title: The new title for the conversation
            now: Current timestamp
        """
        if not self.status.is_writable:
            raise ConversationNotWritableError(self.id, self.status.value)
        
        cleaned_title = new_title.strip()
        if not cleaned_title:
            raise EmptyConversationTitleError(self.id)
        max_len = 100
        if len(cleaned_title) > max_len:
             raise ConversationTitleTooLongError(self.id, len(cleaned_title), max_len)
        
        self._title = cleaned_title
        self.touch(now)

    def __repr__(self) -> str:
        """Readable representation showing status, student, and message count."""
        return f"The Conversation {self.title} contains {self.message_count} messages and is {self.status.value}."
