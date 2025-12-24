"""
Conversation DTOs

Command DTOs for conversation-related operations.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.core.domain.value_objects import CreativityLevel, GenerationStyle, Status

# ──────────────────────────────────────────────────────────────────────────
# Send Message Use Case (Command)
# ──────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class SendMessageCommand:
    """
    Command to send a student message and get a teacher response.
    
    Encapsulates all parameters needed to execute the SendMessage use case.
    
    Attributes:
        conversation_id: ID of the conversation to add messages to
        student_message: The text content of the student's message
        creativity_level: AI creativity level (0-3, default: 2 for moderate)
        generation_style: Pedagogical style (default: "conversational")
    """
    conversation_id: UUID
    student_message: str
    creativity_level: CreativityLevel = CreativityLevel.MODERATE
    generation_style: GenerationStyle = GenerationStyle.CONVERSATIONAL


@dataclass(frozen=True)
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
# READ MODELS (Query operations) 
# ──────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True, slots=True)
class ConversationSummary:
    """
    Read model for conversation list views.
    
    Lightweight summary for displaying conversations in lists
    without loading full entities with all messages. Optimized for read performance.
    
    Attributes:
        id: Unique conversation identifier
        title: Conversation title
        created_at: When the conversation was created
        last_activity_at: When the conversation was last modified
        status: Current conversation status (ACTIVE, ARCHIVED, DELETED)
    """
    id: UUID
    title: str
    created_at: datetime
    last_activity_at: datetime
    status: Status
    