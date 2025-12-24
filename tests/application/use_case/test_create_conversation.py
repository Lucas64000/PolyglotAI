
from collections.abc import Callable
from uuid import uuid4
import pytest

from src.core.domain.value_objects import Language
from src.core.exceptions import InvalidLanguagePairError

from src.application.dtos.conversations import CreateConversationCommand
from src.application.commands import CreateConversationUseCase

from tests.doubles.stubs import StubTimeProvider
from tests.doubles.fakes import InMemoryConversationRepository

class TestCreateConversation:

    async def test_should_create_conversation_successfully(
        self,
        make_create_conversation_command: Callable[..., CreateConversationCommand],
        stub_time: StubTimeProvider,
    ) -> None:
        fake_repo = InMemoryConversationRepository()
        student_id = uuid4()

        initial_conversations = await fake_repo.get_student_conversations(student_id=student_id)

        command = make_create_conversation_command(
            student_id=student_id,
            title="Custom Title",
            native_lang=Language("fr"),
            target_lang=Language("en"),
        )

        use_case = CreateConversationUseCase(
            conv_repo=fake_repo,
            time_provider=stub_time
        )
        
        result = await use_case.execute(command)
        
        conversation = await fake_repo.get_by_id(id=result.conversation_id)
        final_conversations = await fake_repo.get_student_conversations(student_id=student_id)
        
        assert len(initial_conversations) == 0
        assert len(final_conversations) == 1
        assert final_conversations[0].conversation_id == result.conversation_id

        assert conversation.title == command.title
        assert conversation.native_lang == command.native_lang
        assert conversation.target_lang == command.target_lang
    
    async def test_same_native_and_target_raises_error(
        self,
        make_create_conversation_command: Callable[..., CreateConversationCommand],
        stub_time: StubTimeProvider,
    ) -> None:
        fake_repo = InMemoryConversationRepository()
        student_id = uuid4()

        command = make_create_conversation_command(
            student_id=student_id,
            title="Custom Title",
            native_lang=Language("fr"),
            target_lang=Language("fr"),
        )

        use_case = CreateConversationUseCase(
            conv_repo=fake_repo,
            time_provider=stub_time
        )
        
        with pytest.raises(InvalidLanguagePairError):
            await use_case.execute(command)

    