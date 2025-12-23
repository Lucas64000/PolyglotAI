"""
Send Message DTOs

Data Transfer Objects for the SendMessage use case.
"""

from dataclasses import dataclass
from uuid import UUID

from src.core.domain.value_objects import CreativityLevel, GenerationStyle

@dataclass(frozen=True)
class SendMessageRequest:
    """
    Request to send a student message and get a teacher response.
    
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
class SendMessageResponse:
    """
    Response after sending a message and getting teacher response.
    
    Contains the teacher response and metadata about created messages.
    
    Attributes:
        message_id: ID of the teacher's message
        student_message_id: ID of the student's message that was added
        teacher_message: Text content of the teacher's response
    """
    message_id: UUID
    student_message_id: UUID
    teacher_message: str
    