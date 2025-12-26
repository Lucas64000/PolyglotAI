
# 1. find conversation by id conv repo 
# 2. return conversation entity

from uuid import uuid4
from collections.abc import Callable
from datetime import datetime
import pytest 

from src.core.domain import Conversation, Role
from src.core.exceptions import ResourceNotFoundError

from src.application.dtos import SelectConversationQuery
from src.application.queries import SelectConversationUseCase

from tests.doubles.fakes import InMemoryConversationRepository

class TestSelectConversation:

    async def test_should_return_selected_conversation(
        self,
        make_conversation: Callable[..., Conversation],
        make_select_conversation_query: Callable[..., SelectConversationQuery],
        stub_time: datetime
    ) -> None:
        selected_conv_id = uuid4()
        message_id = uuid4()
        student_id = uuid4()
        fake_repo = InMemoryConversationRepository()

        # Set up 4 conversations attached to a specific student 
        for _ in range(3):
            conversation = make_conversation(student_id=student_id)
            await fake_repo.save(conversation=conversation)
        
        # Add a message to the selected conversation
        selected_conv = make_conversation(
            id=selected_conv_id,
            student_id=student_id,
        )
        selected_conv.add_message(
            new_message_id=message_id,
            now=stub_time,
            role=Role.TEACHER,
            content="Hello student!"
        )
        await fake_repo.save(conversation=selected_conv)    

        query = make_select_conversation_query(
            student_id=student_id,
            conversation_id=selected_conv_id,
        )

        use_case = SelectConversationUseCase(
            repository=fake_repo,
        )

        result = await use_case.execute(query=query)

        assert result.conversation_id == selected_conv_id
        assert len(result.messages) == 1
        assert result.messages[0].id == message_id

    async def test_should_raise_error_when_conversation_not_found(
        self,
        make_select_conversation_query: Callable[..., SelectConversationQuery],
    ) -> None:
        fake_repo = InMemoryConversationRepository()
        student_id = uuid4()
        non_existent_id = uuid4()

        query = make_select_conversation_query(
            student_id=student_id,
            conversation_id=non_existent_id,
        )

        use_case = SelectConversationUseCase(repository=fake_repo)

        with pytest.raises(ResourceNotFoundError):
            await use_case.execute(query=query)

    async def test_should_raise_error_when_accessing_other_student_conversation(
        self,
        make_conversation: Callable[..., Conversation],
        make_select_conversation_query: Callable[..., SelectConversationQuery],
    ) -> None:
        student1_id = uuid4()
        student1_conv = make_conversation(student_id=student1_id)
        fake_repo = InMemoryConversationRepository()

        await fake_repo.save(conversation=student1_conv)

        student2_id = uuid4()

        query = make_select_conversation_query(
            student_id=student2_id,
            conversation_id=student1_id
        )

        use_case = SelectConversationUseCase(repository=fake_repo)

        with pytest.raises(ResourceNotFoundError):
            await use_case.execute(query=query)