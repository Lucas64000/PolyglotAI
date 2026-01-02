
from uuid import UUID
from typing import Annotated
from dataclasses import dataclass
from fastapi import Query

@dataclass
class PaginationParams:
    """
    Standard pagination parameters reusable across all list endpoints.
    """
    limit: Annotated[int, Query(ge=1, le=100, description="Number of items to return per page")] = 20
    offset: Annotated[int, Query(ge=0, description="Number of items to skip")] = 0


@dataclass
class ConversationFilterParams:
    """
    Filtering parameters for listing conversations.
    """
    student_id: Annotated[UUID, Query(..., description="ID of the student to retrieve conversations for")]


@dataclass
class DeleteConversationParams:
    """
    Security parameters for deletion.
    """
    student_id: Annotated[UUID, Query(..., description="ID of the conversation owner (security check)")]