"""
Conversation DTOs

Command DTOs for conversation-related operations.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.core.domain.value_objects import (
    CreativityLevel, 
    GenerationStyle, 
    Language,
)

# ──────────────────────────────────────────────────────────────────────────
# List Conversation Use Case (Query)
# ──────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True, slots=True)
class ListConversationsQuery:
    """
    Query DTO for retrieving a paginated list of student conversations.

    Encapsulates the query parameters required to fetch conversation
    summaries for a specific student. It serves as the input contract for the
    ListUserConversations use case, enforcing pagination to ensure performance.

    Attributes:
        student_id: The unique identifier of the student whose conversations are requested.
        limit: The maximum number of results to return (default: 20).
        offset: The number of items to skip before starting to collect the result set (default: 0).
    """
    student_id: UUID
    limit: int = 20
    offset: int = 0

@dataclass(frozen=True, slots=True)
class ConversationSummary:
    """
    Read model for conversation list views.
    
    Lightweight summary for displaying conversations in lists
    without loading full entities with all messages. Optimized for read performance.
    
    Attributes:
        conversation_id: Unique conversation identifier
        title: Conversation title
        created_at: When the conversation was created
        last_activity_at: When the conversation was last modified
        status: Current conversation status
    """
    conversation_id: UUID
    title: str
    created_at: datetime
    last_activity_at: datetime
    status: str

# ──────────────────────────────────────────────────────────────────────────
# Create Conversation Use Case (Command)
# ──────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True, slots=True)
class CreateConversationCommand:
    """
    Command to create a conversation.
    
    Encapsulates all parameters needed to execute the CreateConversation use case.
    
    Attributes:
        student_id: ID of the student who wants to start a conversation
        title: The title of the conversation
        native_lang: The student's native language
        target_lang: The language the student is learning in this conversation
    """
    student_id: UUID
    title: str
    native_lang: Language
    target_lang: Language

@dataclass(frozen=True, slots=True)
class CreateConversationResult:
    """
    Result after creating a conversation.
    
    Contains the conversation id.
    
    Attributes:
        conversation_id: ID of the conversation.
    """
    conversation_id: UUID

# ──────────────────────────────────────────────────────────────────────────
# Select Conversation Use Case (Query)
# ──────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True, slots=True)
class SelectConversationQuery:
    """
    Query for retrieving a selected conversation.

    Encapsulates the query parameters required to fetch the conversation 
    for a specific student. It serves as the input contract for the SelectConversation use case.

    Attributes:
        student_id: The unique identifier of the student.
        conversation_id: The unique identifier of the requested conversation.
    """
    student_id: UUID
    conversation_id: UUID

@dataclass(frozen=True)
class MessageView:
    """
    Read model for displaying messages in a conversation.
    
    Represents a single message with its metadata, optimized for view/display purposes.
    
    Attributes:
        id: Unique message identifier
        role: Message sender role ("student" or "teacher")
        content: The text content of the message
        created_at: Timestamp when the message was created
    """
    id: UUID
    role: str       
    content: str
    created_at: datetime

@dataclass(frozen=True, slots=True)
class SelectConversationResult:
    """
    Result after retrieving a conversation.
    
    Contains the complete conversation information including metadata and all associated messages.
    Used as the response model for the SelectConversation use case.
    
    Attributes:
        conversation_id: Unique conversation identifier
        title: The conversation title
        native_lang: Student's native language (ISO 639-1 code)
        target_lang: Language being learned (ISO 639-1 code)
        status: Current conversation status (e.g., "ACTIVE", "ARCHIVED")
        messages: List of all messages in the conversation
    """
    conversation_id: UUID
    title: str
    native_lang: str 
    target_lang: str
    status: str      
    messages: list[MessageView]

# ──────────────────────────────────────────────────────────────────────────
# Send Message Use Case (Command)
# ──────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True, slots=True)
class SendMessageCommand:
    """
    Command to send a student message and get a teacher response.
    
    Encapsulates all parameters needed to execute the SendMessage use case.
    
    Attributes:
        conversation_id: ID of the conversation to add messages to
        student_message: The text content of the student's message
        creativity_level: Teacher creativity level default: MODERATE)
        generation_style: Pedagogical style (default: CONVERSATIONAL)
    """
    conversation_id: UUID
    student_message: str
    creativity_level: CreativityLevel = CreativityLevel.MODERATE
    generation_style: GenerationStyle = GenerationStyle.CONVERSATIONAL


@dataclass(frozen=True, slots=True)
class SendMessageResult:
    """
    Result after sending a message and getting teacher response.
    
    Contains the teacher response and metadata about created messages.
    
    Attributes:
        message_id: ID of the teacher's message
        student_message_id: ID of the student's message that was added
        teacher_message: Text content of the teacher's response
    """
    message_id: UUID
    student_message_id: UUID
    teacher_message: str

# ──────────────────────────────────────────────────────────────────────────
# Delete Conversation Use Case (Command)
# ──────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True, slots=True)
class DeleteConversationCommand:

    conversation_id: UUID
    student_id: UUID