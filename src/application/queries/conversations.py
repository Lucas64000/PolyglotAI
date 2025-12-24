from typing import Sequence

from src.application.ports.conversations import ConversationReader
from src.application.dtos.conversations import (
    ListConversationsQuery, 
    ConversationSummary
)


class ListStudentConversationsUseCase:
    """
    Query Use Case responsible for retrieving student conversations.

    This use case orchestrates the read-only operation of fetching a paginated
    list of conversation summaries for a specific student. It bridges the
    controller query (DTO) and the secondary adapter (Reader).

    Attributes:
        reader: The data access port optimized for reading conversation summaries.
    """
    
    def __init__(self, reader: ConversationReader) -> None:
        """
        Initialize the use case with required dependencies.

        Args:
            reader: An implementation of the ConversationReader protocol.
        """
        self.reader = reader

    async def execute(self, query: ListConversationsQuery) -> Sequence[ConversationSummary]:
        """
        Executes the query to fetch conversation summaries.

        Delegates the retrieval to the reader port using the parameters provided in the query object. 

        Args:
            query: The input DTO containing filtering and pagination criteria
                    (student_id, limit, offset).

        Returns:
            A sequence of ConversationSummary objects representing the student's
            conversations. Returns an empty sequence if no conversations are found.
        """
        return await self.reader.get_student_conversations(
            student_id=query.student_id,
            limit=query.limit,
            offset=query.offset
        )