"""
In-Memory Conversation Repository (Fake)

Fake implementation of ConversationRepository using in-memory storage.
Has real logic but simplified storage - no persistence between runs.
"""

import copy
from typing import Sequence
from uuid import UUID

from src.core.domain import Conversation
from src.core.ports import ConversationRepository
from src.core.exceptions import ResourceNotFoundError

from src.application.ports import ConversationReader
from src.application.queries.conversations import ConversationSummary


class InMemoryConversationRepository(ConversationRepository, ConversationReader):
    """
    In-memory Fake implementation of ConversationRepository and ConversationReader.
    
    Uses deep copying to prevent external modifications to stored entities.
    """

    def __init__(self) -> None:
        self._storage: dict[UUID, Conversation] = {}

    # ──────────────────────────────────────────────────────────────────────────
    # ConversationRepository (Write Operations)
    # ──────────────────────────────────────────────────────────────────────────

    async def save(self, conversation: Conversation) -> None:
        """Save or update a conversation."""
        self._storage[conversation.id] = copy.deepcopy(conversation)

    async def find_by_id(self, id: UUID) -> Conversation | None:
        """Find a conversation by ID, returns None if not found."""
        if id not in self._storage:
            return None
        return copy.deepcopy(self._storage[id])

    async def remove(self, id: UUID) -> None:
        """Remove a conversation by ID, raises if not found (only for in-memory storage)."""
        if id not in self._storage:
            raise ResourceNotFoundError(resource_type="Conversation", resource_id=id)
        del self._storage[id]

    # ──────────────────────────────────────────────────────────────────────────
    # ConversationReader (Query Operations)
    # ──────────────────────────────────────────────────────────────────────────

    async def get_student_conversations(
        self, 
        student_id: UUID, 
        limit: int = 20, 
        offset: int = 0
    ) -> Sequence[ConversationSummary]:
        """Get paginated conversation summaries for a student."""
        student_conversations = [
            conv for conv in self._storage.values() 
            if conv.student_id == student_id
        ]
        student_conversations.sort(key=lambda c: c.created_at, reverse=True)
        paginated_convs = student_conversations[offset : offset + limit]
        return [self._to_summary(c) for c in paginated_convs]

    def _to_summary(self, conversation: Conversation) -> ConversationSummary:
        """Map entity to read model."""
        return ConversationSummary(
            conversation_id=conversation.id,
            title=conversation.title or "Conversation",
            created_at=conversation.created_at,
            last_activity_at=conversation.last_activity_at,
            status=conversation.status
        )


