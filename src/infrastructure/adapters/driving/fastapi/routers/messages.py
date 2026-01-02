
from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, status, Path

from src.application.dtos import (
    SendMessageCommand, SendMessageResult,
)

from ..models import SendMessageRequest
from ..dependencies import SendMessageUseCaseDep

router = APIRouter(tags=["Messages"])

@router.post(
    "/conversations/{conversation_id}/messages",
    status_code=status.HTTP_200_OK,
    response_model=SendMessageResult,
)
async def send_message(
    conversation_id: Annotated[UUID, Path(description="The conversation context")],
    request: SendMessageRequest,
    use_case: SendMessageUseCaseDep
) -> SendMessageResult:
    """
    Send a message and receive AI response.
    """
    command = SendMessageCommand(
        conversation_id=conversation_id,
        student_message=request.student_message,
        creativity_level=request.creativity_level,
        generation_style=request.generation_style
    )

    return await use_case.execute(command)