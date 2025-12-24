
from typing import Protocol
from uuid import UUID, uuid4

import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from src.core.domain import (
    CreativityLevel, 
    GenerationStyle, 
    Status,
    Language,
)
from src.core.ports import ChatProvider

from src.application.dtos.conversations import (
    # ListStudentConversationsUseCase
    ListConversationsQuery, ConversationSummary,
    # CreateConversationUseCase
    CreateConversationCommand, CreateConversationResult,
    # SendMessageUseCase 
    SendMessageCommand, SendMessageResult,
)

from tests.doubles.stubs import StubTimeProvider

# Protocols

class MakeListConversationsQuery(Protocol):
    def __call__(
        self,
        student_id: UUID,
        limit: int,
        offset: int,
    ) -> ListConversationsQuery: ...


class MakeConversationSummary(Protocol):
    def __call__(
        self,
        conversation_id: UUID,
        title: str,
        created_at: datetime,
        last_activity_at: datetime,
        status: Status,
    ) -> ConversationSummary: ...

class MakeCreateConversationCommand(Protocol):
    def __call__(
        self,
        student_id: UUID,
        native_lang: Language,
        target_lang: Language,
        title: str,
    ) -> CreateConversationCommand: ...

class MakeCreateConversationResult(Protocol):
    def __call__(
        self,
        conversation_id: UUID,
    ) -> CreateConversationResult: ...

class MakeSendMessageCommand(Protocol):
    def __call__(
        self,
        conversation_id: UUID,
        student_message: str,
        native_lang: Language,
        target_lang: Language,
        creativity_level: CreativityLevel,
        generation_style: GenerationStyle,
    ) -> SendMessageCommand: ...


class MakeSendMessageResult(Protocol):
    def __call__(
        self, 
        message_id: UUID,
        student_message_id: UUID,
        teacher_message: str
    ) -> SendMessageResult: ...

# Fixtures

# ──────────────────────────────────────────────────────────────────────────
# ListStudentConversationsUseCase 
# ──────────────────────────────────────────────────────────────────────────

@pytest.fixture
def make_list_conversations_query() -> MakeListConversationsQuery:
    """
    Factory fixture for creating ListConversationsQuery DTOs.
    
    Provides sensible defaults for pagination while allowing customization.
    """
    def _factory(
        student_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> ListConversationsQuery:
        return ListConversationsQuery(
            student_id=student_id or uuid4(),
            limit=limit,
            offset=offset,
        )
    
    return _factory

@pytest.fixture
def make_conversation_summary(fixed_time: datetime) -> MakeConversationSummary:
    """
    Factory fixture for creating ConversationSummary DTOs.
    
    Uses fixed_time as default for timestamps to ensure deterministic tests.
    """
    def _factory(
        conversation_id: UUID | None = None,
        title: str = "Conversation Title",
        created_at: datetime | None = None,
        last_activity_at: datetime | None = None,
        status: Status = Status.ACTIVE,
    ) -> ConversationSummary:
        return ConversationSummary(
            conversation_id=conversation_id or uuid4(),
            title=title,
            created_at=created_at or fixed_time,
            last_activity_at=last_activity_at or fixed_time,
            status=status,
        )
    
    return _factory

# ──────────────────────────────────────────────────────────────────────────
# CreateConversationUseCase 
# ──────────────────────────────────────────────────────────────────────────

@pytest.fixture
def make_create_conversation_command() -> MakeCreateConversationCommand:
    def _factory(
        student_id: UUID | None = None,
        native_lang: Language = Language("fr"),
        target_lang: Language = Language("en"),
        title: str = "New conversation",
    ) -> CreateConversationCommand:
        return CreateConversationCommand(
            student_id=student_id or uuid4(),
            native_lang=native_lang,
            target_lang=target_lang,
            title=title,
        )
    
    return _factory

@pytest.fixture
def make_create_conversation_result() -> MakeCreateConversationResult:
    def _factory(
        conversation_id: UUID | None = None
    ) -> CreateConversationResult:
        return CreateConversationResult(
            conversation_id=conversation_id or uuid4()
        )
    
    return _factory

# ──────────────────────────────────────────────────────────────────────────
# SendMessageUseCase 
# ──────────────────────────────────────────────────────────────────────────

@pytest.fixture
def make_send_message_command() -> MakeSendMessageCommand:
    def _factory(
        conversation_id: UUID | None = None,
        student_message: str = "Student message",
        native_lang: Language = Language("fr"),
        target_lang: Language = Language("en"),
        creativity_level: CreativityLevel = CreativityLevel.EXPRESSIVE,
        generation_style: GenerationStyle = GenerationStyle.CONVERSATIONAL,    
    ) -> SendMessageCommand:
        return SendMessageCommand(
            conversation_id=conversation_id or uuid4(),
            student_message=student_message,
            native_lang=native_lang,
            target_lang=target_lang,
            creativity_level=creativity_level,
            generation_style=generation_style
        )

    return _factory

@pytest.fixture
def make_send_message_result() -> MakeSendMessageResult:
    def _factory(
        message_id: UUID | None = None,
        student_message_id: UUID | None = None,
        teacher_message: str = "Teacher response",
    ) -> SendMessageResult:
        return SendMessageResult(
            message_id=message_id or uuid4(),
            student_message_id=student_message_id or uuid4(),
            teacher_message=teacher_message,
        )
    
    return _factory

# Mock

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