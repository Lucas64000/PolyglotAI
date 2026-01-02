"""
Conversation AggregateRoot

Contains the Conversation aggregate root and ChatMessage entity.
Represents a conversation thread between a student and the teacher.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.core.domain.entities.base import Entity, AggregateRoot
from src.core.domain.value_objects import Status, Role, Language
from src.core.exceptions import (
    ConversationNotWritableError, 
    EmptyConversationTitleError, 
    ConversationTitleTooLongError,
    InvalidChatMessageContentError,
    InvalidLanguagePairError,
)


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


@dataclass(eq=False, kw_only=True, slots=True)
class Conversation(AggregateRoot):
    """
    Represents a learning conversation between a student and the teacher.
    
    A conversation groups related messages and tracks their lifecycle.
    Conversations can be ACTIVE (editable), ARCHIVED (read-only), or DELETED.
    The conversation maintains the language pair context for generating appropriate responses.

    Attributes:
        _student_id: Identifier of the conversation owner (student)
        _native_lang: The student's native language
        _target_lang: The language the student is learning
        _title: Title of the conversation
        _status: Current conversation status (ACTIVE, ARCHIVED, DELETED)
        _messages: History of the conversation
        _last_activity_at: Timestamp of the last activity (message addition or status change)
    """

    _student_id: UUID
    _last_activity_at: datetime
    _native_lang: Language
    _target_lang: Language
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
    def native_lang(self) -> Language:
        return self._native_lang
    
    @property
    def target_lang(self) -> Language:
        return self._target_lang

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
        cls, 
        id: UUID, 
        student_id: UUID, 
        title: str,
        native_lang: Language,
        target_lang: Language,
        now: datetime, 
    ) -> Conversation:
        """
        Factory method for creating a new, empty, and active conversation.
        
        Args:
            id: Unique identifier for the conversation
            student_id: Identifier of the conversation owner
            title: Title of the conversation
            native_lang: The student's native language
            target_lang: The language being learned
            now: Current timestamp for creation
        
        Returns:
            Conversation: a new conversation with empty messages and ACTIVE status
            
        Raises:
            InvalidLanguagePairError: if native_lang and target_lang are identical
            EmptyConversationTitleError: if title is empty
            ConversationTitleTooLongError: if title is too long
        """
        if native_lang == target_lang:
            raise InvalidLanguagePairError(native=native_lang.code, target=target_lang.code)

        cleaned_title = title.strip()
        if not cleaned_title:
            raise EmptyConversationTitleError(id)
        
        max_len = 100
        if len(cleaned_title) > max_len:
            raise ConversationTitleTooLongError(id, len(cleaned_title), max_len)

        return cls(
            _id=id,
            _student_id=student_id, 
            _native_lang=native_lang,
            _target_lang=target_lang,
            _created_at=now,
            _last_activity_at=now,
            _title=cleaned_title,
        )
    
    def add_message(
            self, 
            new_message_id: UUID, 
            now: datetime, 
            role: Role, 
            content: str
        ) -> ChatMessage:
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