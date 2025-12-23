"""
Conversation Summary Read Model

Lightweight representation of a conversation for listing and querying operations.
Part of the query side in CQRS architecture.
"""

from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from src.core.domain.value_objects import Status


@dataclass(frozen=True, slots=True)
class ConversationSummary:
    """
    Read model for conversation list views.
    
    Contains just enough information for displaying conversations in lists
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
