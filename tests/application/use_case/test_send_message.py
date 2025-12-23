"""
Tests for SendMessageUseCase.

Test Strategy:
- FAKE (InMemoryConversationRepository): Verify state changes and persistence
- STUB (StubTimeProvider): Control time for deterministic assertions
- MOCK (AsyncMock for ChatProvider): Verify interactions with response service
"""

from collections.abc import Callable
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.core.domain import (
    Conversation,
    ChatMessage,
    Role,
    TeacherProfile,
    CreativityLevel,
    GenerationStyle,
)
from src.core.exceptions import ResourceNotFoundError, TeacherResponseError
from src.application.commands.dtos.send_message import SendMessageRequest
from src.application.commands.use_cases.send_message import SendMessageUseCase

from tests.doubles.fakes import InMemoryConversationRepository
from tests.doubles.stubs import StubTimeProvider


class TestSendMessageUseCase:
    """
    Tests for the happy path of SendMessageUseCase.
    """

    async def test_should_send_message_successfully(
        self, 
        mock_chat: AsyncMock, 
        stub_time: StubTimeProvider,
        make_send_message_request: Callable[..., SendMessageRequest],
        make_conversation: Callable[..., Conversation],
        make_chat_message: Callable[..., ChatMessage] 
    ) -> None:
        """
        Given an active conversation with existing messages, when a student sends a new message
        Then the student message and teacher response are added and persisted.
        
        This test validates:
        1. Response DTO contains correct data
        2. Persistence: messages are saved to repository
        3. Interaction: ChatProvider is called with correct history and profile
        """
        # FAKE: In-memory repository to verify state changes
        fake_repo = InMemoryConversationRepository()

        # Set up existing conversation with 2 messages
        conv_id = uuid4()
        msg1 = make_chat_message(role=Role.STUDENT, content="Bonjour!")
        msg2 = make_chat_message(role=Role.TEACHER, content="Hello! How can I help?")
        existing_conversation = make_conversation(id=conv_id, messages=[msg1, msg2])
        await fake_repo.save(existing_conversation)
        initial_message_count = len(existing_conversation.messages)

        # MOCK: Configure expected teacher response
        student_message = "Comment dit-on 'chat' en anglais?"
        expected_teacher_response = "The word 'chat' translates to 'cat' in English."
        mock_chat.get_teacher_response.return_value = expected_teacher_response

        # Build request DTO
        request = make_send_message_request(
            conversation_id=conv_id, 
            student_message=student_message,
            creativity_level=CreativityLevel.MODERATE,
            generation_style=GenerationStyle.CONVERSATIONAL,
        )

        # Build use case with all dependencies injected
        use_case = SendMessageUseCase(
            chat_provider=mock_chat,     
            conv_repo=fake_repo,          
            time_provider=stub_time,      
        )

        # Execute use case with the request DTO
        response = await use_case.execute(request)

        # 1. Response DTO correctness
        assert response.teacher_message == expected_teacher_response

        # 2. Persistence: verify state in FAKE repository
        saved_conversation = await fake_repo.get_by_id(conv_id)
        assert len(saved_conversation.messages) == initial_message_count + 2

        # Student message was persisted correctly
        student_message = saved_conversation.messages[-2]
        assert student_message.role == Role.STUDENT
        assert student_message.content == student_message.content
        assert student_message.created_at == stub_time.now()  # STUB provides fixed time

        # Teacher message was persisted correctly
        teacher_message = saved_conversation.messages[-1]
        assert teacher_message.role == Role.TEACHER
        assert teacher_message.content == expected_teacher_response
        assert teacher_message.created_at == stub_time.now()

        # 3. Interaction: verify MOCK was called correctly
        expected_history = tuple(saved_conversation.messages[:-1])  # Excludes teacher response
        expected_teacher_profile = TeacherProfile(
            creativity_level=request.creativity_level,
            generation_style=request.generation_style
        )
        mock_chat.get_teacher_response.assert_awaited_once_with(
            history=expected_history,
            teacher_profile=expected_teacher_profile
        )


class TestSendMessageErrors:
    """
    Tests for error handling in SendMessageUseCase.
    
    These tests verify that the use case properly propagates exceptions
    from its dependencies (domain entities, repositories, response service).
    """

    async def test_should_propagate_chat_provider_exception(
        self,
        mock_chat: AsyncMock,
        stub_time: StubTimeProvider,
        make_send_message_request: Callable[..., SendMessageRequest],
        make_conversation: Callable[..., Conversation],
    ) -> None:
        """
        Given an active conversation
        When the ChatProvider raises an exception
        Then the exception propagates to the caller.
        
        The use case should NOT silently swallow infrastructure errors.
        """
        # FAKE: In-memory repository to verify state changes
        fake_repo = InMemoryConversationRepository()
        conv_id = uuid4()
        await fake_repo.save(make_conversation(id=conv_id, messages=[]))

        # STUB behavior on Mock: force failure
        error_message = "Service connection timeout"
        mock_chat.get_teacher_response.side_effect = TeacherResponseError(cause=error_message)

        request = make_send_message_request(conversation_id=conv_id)
        use_case = SendMessageUseCase(
            chat_provider=mock_chat,
            conv_repo=fake_repo,
            time_provider=stub_time,
        )

        # Execute use case, should raise TeacherResponseError
        with pytest.raises(TeacherResponseError) as exc_info:
            await use_case.execute(request)
        
        assert error_message in str(exc_info.value)

    async def test_should_raise_when_conversation_not_found(
        self,
        mock_chat: AsyncMock,
        stub_time: StubTimeProvider,
        make_send_message_request: Callable[..., SendMessageRequest],
    ) -> None:
        """
        Given a non-existent conversation ID when sending a message
        Then ResourceNotFoundError is raised.
        """
        # Empty storage
        fake_repo = InMemoryConversationRepository()  
        non_existent_id = uuid4()

        request = make_send_message_request(conversation_id=non_existent_id)
        use_case = SendMessageUseCase(
            chat_provider=mock_chat,
            conv_repo=fake_repo,
            time_provider=stub_time,
        )

        # Execute use case, should raise ResourceNotFoundError
        with pytest.raises(ResourceNotFoundError):
            await use_case.execute(request)