
from typing import Protocol
from uuid import UUID, uuid4

import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from src.application.commands.dtos.send_message import SendMessageRequest, SendMessageResponse

from src.core.domain import CreativityLevel, GenerationStyle
from src.core.ports import ChatProvider

from tests.doubles.stubs import StubTimeProvider

# Protocols

class MakeSendMessageRequest(Protocol):
    def __call__(
        self,
        conversation_id: UUID,
        student_message: str,
        creativity_level: CreativityLevel,
        generation_style: GenerationStyle,
    ) -> SendMessageRequest: ...


class MakeSendMessageResponse(Protocol):
    def __call__(
        self, 
        message_id: UUID,
        student_message_id: UUID,
        teacher_message: str
    ) -> SendMessageResponse: ...

# Fixtures

@pytest.fixture
def make_send_message_request() -> MakeSendMessageRequest:
    def _factory(
        conversation_id: UUID | None = None,
        student_message: str = "Student message",
        creativity_level: CreativityLevel = CreativityLevel.EXPRESSIVE,
        generation_style: GenerationStyle = GenerationStyle.CONVERSATIONAL,    
    ) -> SendMessageRequest:
        return SendMessageRequest(
            conversation_id=conversation_id or uuid4(),
            student_message=student_message,
            creativity_level=creativity_level,
            generation_style=generation_style
        )

    return _factory

@pytest.fixture
def make_send_message_response() -> MakeSendMessageResponse:
    def _factory(
        message_id: UUID | None = None,
        student_message_id: UUID | None = None,
        teacher_message: str = "Teacher response",
    ) -> SendMessageResponse:
        return SendMessageResponse(
            message_id=message_id or uuid4(),
            student_message_id=student_message_id or uuid4(),
            teacher_message=teacher_message,
        )
    
    return _factory

@pytest.fixture
def mock_chat() -> AsyncMock:
    """
    MOCK for ChatProvider.
    
    Use this to verify interactions (was it called? with what arguments?).
    Configure return_value or side_effect per test as needed.
    """
    mock = AsyncMock(spec=ChatProvider)
    mock.get_teacher_response.return_value = "Hello Student!"

    return mock

@pytest.fixture
def fixed_time() -> datetime:
    """Fixed timestamp for deterministic tests."""
    return datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

@pytest.fixture
def stub_time(fixed_time: datetime) -> StubTimeProvider:
    """
    STUB for TimeProvider.
    
    Returns a fixed, predictable time value.
    """
    return StubTimeProvider(now=fixed_time)