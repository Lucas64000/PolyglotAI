
from typing import Callable
from uuid import uuid4

from src.core.domain.entities import Conversation

from src.application.dtos.conversations import ListConversationsQuery
from src.application.queries.conversations import ListStudentConversationsUseCase

from tests.doubles.fakes import InMemoryConversationRepository

class TestListStudentConversations:
    """
    Tests for the happy path of ListStudentConversationsUseCase.
    """

    async def test_should_only_return_conversations_owned_by_student(
        self,
        make_list_conversations_query: Callable[..., ListConversationsQuery],
        make_conversation: Callable[..., Conversation]
    ) -> None:
        """
        Ensure that a student can only see their own conversations
        and not those belonging to other students.
        """
        fake_reader = InMemoryConversationRepository()
        
        # Create data for two different students
        student1_id = uuid4()
        student2_id = uuid4()
        
        # Student 1 has 1 conversation
        student1_conversation = make_conversation(student_id=student1_id, title="Student1's Chat")
        await fake_reader.save(student1_conversation)
        
        # Student 2 has 2 conversations
        await fake_reader.save(make_conversation(student_id=student2_id, title="Student2's Chat 1"))
        await fake_reader.save(make_conversation(student_id=student2_id, title="Student2's Chat 2"))

        # Student 1 requests his conversations
        query = make_list_conversations_query(student_id=student1_id)
        use_case = ListStudentConversationsUseCase(reader=fake_reader)
        summaries = await use_case.execute(query)

        # Student 1 should only see his single conversation
        assert len(summaries) == 1
        assert summaries[0].conversation_id == student1_conversation.id
        assert summaries[0].title == "Student1's Chat"

    async def test_should_respect_pagination_limit_and_offset(
        self,
        make_list_conversations_query: Callable[..., ListConversationsQuery],
        make_conversation: Callable[..., Conversation]
    ) -> None:
        """
        Verify that the query respects the 'limit' and 'offset' parameters
        to return the correct subset of results.
        """
        fake_reader = InMemoryConversationRepository()
        student_id = uuid4()

        # Create a sequence of 10 conversations
        for i in range(10):
            conv = make_conversation(student_id=student_id, title=f"Conversation {i}")
            await fake_reader.save(conv)

        use_case = ListStudentConversationsUseCase(reader=fake_reader)

        # Fetch the first page (Limit 3, Offset 0)
        # Expected: Conversations 0, 1, 2
        query_page_1 = make_list_conversations_query(
            student_id=student_id, 
            limit=3, 
            offset=0
        )
        page_1 = await use_case.execute(query_page_1)

        # Fetch the second page (Limit 3, Offset 3)
        # Expected: Conversations 3, 4, 5
        query_page_2 = make_list_conversations_query(
            student_id=student_id, 
            limit=3, 
            offset=3
        )
        page_2 = await use_case.execute(query_page_2)

        query_last_page = make_list_conversations_query(
            student_id=student_id, 
            limit=3, 
            offset=9
        )
        last_page = await use_case.execute(query_last_page)

        assert len(page_1) == 3
        assert len(page_2) == 3
        assert len(last_page) == 1
        
        # Ensure we retrieved different sets of conversations
        page_1_ids = {s.conversation_id for s in page_1}
        page_2_ids = {s.conversation_id for s in page_2}
        last_page_ids = {s.conversation_id for s in last_page}
        
        # The intersection of IDs should be empty (no duplicates between pages)
        assert page_1_ids.isdisjoint(page_2_ids)
        assert page_1_ids.isdisjoint(last_page_ids)
        assert page_2_ids.isdisjoint(last_page_ids)

    async def test_should_return_empty_list_for_new_student(
        self, 
        make_list_conversations_query: Callable[..., ListConversationsQuery]
    ) -> None:
        """
        Verify that querying a student with no history returns an empty list.
        """
        fake_reader = InMemoryConversationRepository()
        student_id = uuid4()

        query = make_list_conversations_query(student_id=student_id)
        use_case = ListStudentConversationsUseCase(reader=fake_reader)
        summaries = await use_case.execute(query)

        assert summaries == []