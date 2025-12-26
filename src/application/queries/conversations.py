from typing import Sequence

from src.core.ports import ConversationRepository

from src.application.ports.conversations import ConversationReader
from src.application.dtos.conversations import (
    ListConversationsQuery, 
    ConversationSummary,
    SelectConversationQuery,
    SelectConversationResult,
    MessageView,
)


class ListStudentConversationsUseCase:
    """
    Query Use Case responsible for retrieving student conversations.

    This use case orchestrates the read-only operation of fetching a paginated
    list of conversation summaries for a specific student. It bridges the
    controller query (DTO) and the secondary adapter (Reader).
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
    
class SelectConversationUseCase:
    """
    Query Use Case responsible for retrieving a specific conversation.

    This use case orchestrates the read-only operation of retrieving a specific conversation. 
    """
    
    def __init__(self, repository: ConversationRepository) -> None:
        """
        Initialize the use case with required dependencies.

        Args:
            repository: Repository for conversation retrieving.
        """
        self.repository = repository

    async def execute(self, query: SelectConversationQuery) -> SelectConversationResult:
        """
        Executes the query to fetch conversation.

        Delegates the retrieval to the repository port using the parameters provided in the query object. 

        Args:
            query: The input DTO containing the conversation ID.

        Returns:
            A conversation view containing conversation informations and messages.
        """
        conversation = await self.repository.get_by_id(
            query.conversation_id
        )

        messages = [
            MessageView(
                id=message.id,
                role=message.role.value,
                content=message.content,
                created_at=message.created_at,
            ) for message in conversation.messages
        ]

        return SelectConversationResult(
            conversation_id=conversation.id,
            title=conversation.title,
            native_lang=conversation.native_lang.code,
            target_lang=conversation.target_lang.code,
            status=conversation.status.value,
            messages=messages
        )