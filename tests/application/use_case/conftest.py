
from typing import Protocol
from uuid import UUID, uuid4

import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from src.core.domain import (
    CreativityLevel, 
    GenerationStyle, 
    Language,
)
from src.core.ports import ChatProvider

from src.application.dtos.conversations import (
    # ListStudentConversationsUseCase
    ListConversationsQuery,
    # CreateConversationUseCase
    CreateConversationCommand,
    # SelectConversationUseCase
    SelectConversationQuery, MessageView,
    # SendMessageUseCase 
    SendMessageCommand,
    # DeleteConversationUseCase
    DeleteConversationCommand,
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

class MakeCreateConversationCommand(Protocol):
    def __call__(
        self,
        student_id: UUID,
        native_lang: Language,
        target_lang: Language,
        title: str,
    ) -> CreateConversationCommand: ...

class MakeSelectConversationQuery(Protocol):
    def __call__(
        self,
        student_id: UUID,
        conversation_id: UUID,
    ) -> SelectConversationQuery: ...

class MakeMessageView(Protocol):
    def __call__(
        self,
        id: UUID,
        role: str,
        content: str,
        created_at: datetime,
    ) -> MessageView: ...


class MakeSendMessageCommand(Protocol):
    def __call__(
        self,
        conversation_id: UUID,
        student_message: str,
        creativity_level: CreativityLevel,
        generation_style: GenerationStyle,
    ) -> SendMessageCommand: ...

class MakeDeleteConversationCommand(Protocol):
    def __call__(
        self,
        conversation_id: UUID,
    ) -> DeleteConversationCommand: ...

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

# ──────────────────────────────────────────────────────────────────────────
# CreateConversationUseCase 
# ──────────────────────────────────────────────────────────────────────────

@pytest.fixture
def make_create_conversation_command() -> MakeCreateConversationCommand:
    """
    Factory fixture for creating CreateConversationCommand DTOs.
    
    Provides default values for all required fields.
    Default languages are French (native) and English (target).
    """
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

# ──────────────────────────────────────────────────────────────────────────
# SelectConversationUseCase 
# ──────────────────────────────────────────────────────────────────────────

@pytest.fixture
def make_message_view(fixed_time: datetime) -> MakeMessageView:
    """
    Factory fixture for creating MessageView DTOs.
    
    Uses fixed_time as default for timestamps to ensure deterministic tests.
    Default role is "student".
    """
    def _factory(
        id: UUID | None = None,
        role: str = "student",
        content: str = "Message content",
        created_at: datetime | None = None,
    ) -> MessageView:
        return MessageView(
            id=id or uuid4(),
            role=role,
            content=content,
            created_at=created_at or fixed_time,
        )
    
    return _factory

@pytest.fixture
def make_select_conversation_query() -> MakeSelectConversationQuery:
    """
    Factory fixture for creating SelectConversationQuery DTOs.
    
    Generates random UUIDs for student and conversation IDs if not provided.
    """
    def _factory(
        student_id: UUID | None = None,
        conversation_id: UUID | None = None
    ) -> SelectConversationQuery:
        return SelectConversationQuery(
            student_id=student_id or uuid4(),
            conversation_id=conversation_id or uuid4()
        )
    
    return _factory

# ──────────────────────────────────────────────────────────────────────────
# SendMessageUseCase 
# ──────────────────────────────────────────────────────────────────────────

@pytest.fixture
def make_send_message_command() -> MakeSendMessageCommand:
    """
    Factory fixture for creating SendMessageCommand DTOs.
    
    Default creativity level is moderate and default style is conversational.
    """
    def _factory(
        conversation_id: UUID | None = None,
        student_message: str = "Student message",
        creativity_level: CreativityLevel = CreativityLevel.MODERATE,
        generation_style: GenerationStyle = GenerationStyle.CONVERSATIONAL,    
    ) -> SendMessageCommand:
        return SendMessageCommand(
            conversation_id=conversation_id or uuid4(),
            student_message=student_message,
            creativity_level=creativity_level,
            generation_style=generation_style
        )

    return _factory

# ──────────────────────────────────────────────────────────────────────────
# DeleteConversationUseCase 
# ──────────────────────────────────────────────────────────────────────────

@pytest.fixture
def make_delete_conversation_command() -> MakeDeleteConversationCommand:
    """
    Factory fixture for creating DeleteConversationCommand DTOs.
    
     Generates random UUIDs conversation IDs if not provided.
    """
    def _factory(
        conversation_id: UUID | None = None,
        student_id: UUID | None = None,
    ) -> DeleteConversationCommand:
        return DeleteConversationCommand(
            conversation_id=conversation_id or uuid4(),
            student_id=student_id or uuid4(),
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
    """
    Fixture providing a fixed timestamp for deterministic tests.
    
    Returns 2024-01-01 12:00:00 UTC to ensure consistent datetime values across tests.
    """
    return datetime(2024, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

@pytest.fixture
def stub_time(fixed_time: datetime) -> StubTimeProvider:
    """
    STUB for TimeProvider.
    
    Returns a fixed, predictable time value.
    """
    return StubTimeProvider(now=fixed_time)