
from typing import Callable
from uuid import uuid4
import pytest

from src.core.domain import Conversation, Status
from src.core.ports import TimeProvider
from src.core.exceptions import ResourceNotFoundError

from src.application.dtos import DeleteConversationCommand
from src.application.commands import DeleteConversationUseCase

from tests.doubles.fakes import InMemoryConversationRepository

class TestDeleteConversation:
    
    async def test_should_delete_conversation_successfully(
        self,
        make_conversation: Callable[..., Conversation],
        make_delete_conversation_command: Callable[..., DeleteConversationCommand],
        stub_time: TimeProvider,
    ) -> None:
        fake_repo = InMemoryConversationRepository()
        student_id = uuid4()

        conversation = make_conversation(student_id=student_id)
        await fake_repo.save(conversation=conversation)

        initial_conversations = await fake_repo.get_student_conversations(student_id=student_id)

        command = make_delete_conversation_command(
            conversation_id=conversation.id,
            student_id=student_id,
        )

        use_case = DeleteConversationUseCase(
            repository=fake_repo,
            time_provider=stub_time,
        )

        await use_case.execute(command=command)

        conversation_removed = await fake_repo.get_by_id(conversation.id)
        final_conversations = await fake_repo.get_student_conversations(student_id=student_id)

        assert conversation_removed.status == Status.DELETED
        assert conversation_removed.last_activity_at == stub_time.now()
        assert len(initial_conversations) == 1
        assert len(final_conversations) == 0

    async def test_should_raise_error_when_conversation_not_found(
        self,
        make_delete_conversation_command: Callable[..., DeleteConversationCommand],
        stub_time: TimeProvider,
    ) -> None:
        fake_repo = InMemoryConversationRepository()
        
        command = make_delete_conversation_command(
            conversation_id=uuid4(), 
            student_id=uuid4(),
        )
        
        use_case = DeleteConversationUseCase(fake_repo, stub_time)

        with pytest.raises(ResourceNotFoundError):
            await use_case.execute(command)

    async def test_should_prevent_deletion_of_other_student_conversation(
        self,
        make_conversation: Callable[..., Conversation],
        make_delete_conversation_command: Callable[..., DeleteConversationCommand],
        stub_time: TimeProvider,
    ) -> None:
        fake_repo = InMemoryConversationRepository()
        
        student1_id = uuid4()
        student1_conv = make_conversation(student_id=student1_id)
        await fake_repo.save(student1_conv)
        
        # Student2 tries to delete it
        student2_id = uuid4()
        command = make_delete_conversation_command(
            conversation_id=student1_conv.id,
            student_id=student2_id,
        )
        
        use_case = DeleteConversationUseCase(fake_repo, stub_time)

        # Should fail securely
        with pytest.raises(ResourceNotFoundError):
            await use_case.execute(command)
            
        # Verify data is still intact
        saved_conv = await fake_repo.get_by_id(student1_conv.id)
        assert saved_conv.status != Status.DELETED