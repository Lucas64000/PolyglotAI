
from uuid import UUID
from typing import Annotated, Sequence

from fastapi import APIRouter, status, Path, Depends

from src.core.domain.value_objects import Language

from src.application.dtos import (
    CreateConversationCommand, CreateConversationResult, 
    ListConversationsQuery, ConversationSummary,
    SelectConversationQuery, SelectConversationResult,
    DeleteConversationCommand,
)

from ..models import CreateConversationRequest
from ..params import PaginationParams, ConversationFilterParams, DeleteConversationParams
from ..dependencies import (
    CreateConversationUseCaseDep,
    SelectConversationUseCaseDep,
    DeleteConversationUseCaseDep,
    ListConversationsUseCaseDep
)

router = APIRouter(tags=["Conversations"])

@router.post(
    "/conversations",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateConversationResult,
)
async def create_conversation(
    request: CreateConversationRequest,
    use_case: CreateConversationUseCaseDep
) -> CreateConversationResult:
    """
    Create a new conversation.
    """
    command = CreateConversationCommand(
        student_id=request.student_id,
        native_lang=Language(request.native_lang),
        target_lang=Language(request.target_lang)
    )

    return await use_case.execute(command)


@router.get(
    "/conversations",
    status_code=status.HTTP_200_OK,
    response_model=Sequence[ConversationSummary],
)
async def list_conversations(
    use_case: ListConversationsUseCaseDep,
    filters: Annotated[ConversationFilterParams, Depends()],
    pagination: Annotated[PaginationParams, Depends()]
) -> Sequence[ConversationSummary]:
    
    query = ListConversationsQuery(
        student_id=filters.student_id,
        limit=pagination.limit,
        offset=pagination.offset,
    )

    return await use_case.execute(query=query)


@router.get(
    "/conversations/{conversation_id}",
    status_code=status.HTTP_200_OK,
    response_model=SelectConversationResult,
)
async def get_conversation(
    conversation_id: Annotated[UUID, Path(description="Unique identifier of the conversation")],
    filters: Annotated[ConversationFilterParams, Depends()],
    use_case: SelectConversationUseCaseDep
) -> SelectConversationResult:
    """
    Retrieve conversation details including message history.
    """
    query = SelectConversationQuery(
        conversation_id=conversation_id,
        student_id=filters.student_id
    )

    return await use_case.execute(query=query)


@router.delete(
    "/conversations/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_conversation(
    conversation_id: Annotated[UUID, Path(description="Unique identifier of the conversation to delete")],
    delete_params: Annotated[DeleteConversationParams, Depends()],
    use_case: DeleteConversationUseCaseDep
) -> None:
    """
    Delete a conversation.
    """
    command = DeleteConversationCommand(
        conversation_id=conversation_id,
        student_id=delete_params.student_id
    )
    
    await use_case.execute(command)