from typing import Protocol, Sequence
from uuid import UUID

from src.application.dtos.conversations import ConversationSummary

class ConversationReader(Protocol):
    """
    Application Port for retrieving conversation read models.
    """

    async def get_student_conversations(
            self, 
            student_id: UUID, 
            limit: int = 20, 
            offset: int = 0
        ) -> Sequence[ConversationSummary]:
        """Get a paginated list of conversation summaries for a student."""
        ...
