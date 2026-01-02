
from uuid import UUID
from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from src.core.domain.value_objects import CreativityLevel, GenerationStyle


class CreateConversationRequest(BaseModel):
    """
    Payload required to initialize a new learning session.
    """
    student_id: Annotated[UUID, Field(..., description="Unique identifier of the student owner")]
    title: Annotated[str | None, Field(None, min_length=1, max_length=100, description="Optional custom title")] = None
    native_lang: Annotated[str, Field(..., min_length=2, max_length=2, pattern="^[a-z]{2}$", description="ISO 639-1 code (e.g. 'fr')")]
    target_lang: Annotated[str, Field(..., min_length=2, max_length=2, pattern="^[a-z]{2}$", description="ISO 639-1 code (e.g. 'en')")]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "student_id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "English Basics - Past Tense",
                "native_lang": "fr",
                "target_lang": "en"
            }
        }
    )


class SendMessageRequest(BaseModel):
    """
    Payload for sending a user message to the AI Tutor.
    """
    student_message: Annotated[str, Field(..., min_length=1, description="The content text sent by the student")]
    creativity_level: Annotated[CreativityLevel, Field(default=CreativityLevel.MODERATE, description="Adjusts response temperature")] = CreativityLevel.MODERATE
    generation_style: Annotated[GenerationStyle, Field(default=GenerationStyle.CONVERSATIONAL, description="Adjusts pedagogical tone")] = GenerationStyle.CONVERSATIONAL

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "student_message": "I goed to the cinema yesterday.",
                "creativity_level": "moderate",
                "generation_style": "corrective"
            }
        }
    )


class SelectConversationRequest(BaseModel):
    """
    Security payload to verify ownership.
    """
    student_id: Annotated[UUID, Field(..., description="ID of the student attempting to access the resource")]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "student_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }
    )


class DeleteConversationRequest(BaseModel):
    """
    Security payload to confirm authority before deleting.
    """
    student_id: Annotated[UUID, Field(..., description="ID of the student requesting deletion")]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "student_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }
    )


class ConversationSummaryResponse(BaseModel):
    """
    Lightweight representation of a conversation.
    """
    conversation_id: UUID
    title: str
    created_at: datetime
    last_activity_at: datetime
    status: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "conversation_id": "a1b2c3d4-e5f6-7890-1234-56789abcdef0",
                "title": "English Basics - Past Tense",
                "created_at": "2023-10-27T10:00:00Z",
                "last_activity_at": "2023-10-27T10:05:30Z",
                "status": "active"
            }
        }
    )


class ListConversationsRequest(BaseModel):
    """
    Pagination parameters.
    """
    student_id: Annotated[UUID, Field(..., description="ID of the student")]
    limit: Annotated[int, Field(default=20, ge=1, le=100, description="Page size")] = 20
    offset: Annotated[int, Field(default=0, ge=0, description="Number of items to skip")] = 0

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "student_id": "123e4567-e89b-12d3-a456-426614174000",
                "limit": 10,
                "offset": 0
            }
        }
    )