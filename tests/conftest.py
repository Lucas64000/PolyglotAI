"""
Root test fixtures.

Fixtures shared across multiple test layers (domain, application and infrastructure).
"""

from __future__ import annotations

from typing import Protocol
from uuid import UUID, uuid4
from datetime import datetime, timezone

import pytest
from unittest.mock import AsyncMock

from src.core.domain.entities import (
    ChatMessage, 
    Student, 
    Conversation,
    VocabularyItem,
    VocabularySource
)
from src.core.domain.value_objects import (
    Role, 
    Language, 
    CEFRLevel,
    Status,
    Lexeme,
    Lemma,
    PartOfSpeech,
)
from src.core.ports import ChatProvider

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

# Protocols

class MakeChatMessage(Protocol):
    def __call__(
        self,
        id: UUID | None = None,
        role: Role = Role.STUDENT,
        content: str = "Test message",
        now: datetime | None = None,
    ) -> ChatMessage: ...

class MakeStudent(Protocol):
    def __call__(
        self,
        id: UUID | None = None,
        native_lang: Language | None = None,
        target_lang: Language | None = None,
        level: CEFRLevel = CEFRLevel.B1,
        now: datetime | None = None,
    ) -> Student: ...

class MakeConversation(Protocol):
    def __call__(
        self,
        id: UUID | None = None,
        student_id: UUID | None = None,
        native_lang: Language | None = None,
        target_lang: Language | None = None,
        messages: list[ChatMessage] | None = None,
        status: Status = Status.ACTIVE,
        title: str | None = None,
        now: datetime | None = None,
    ) -> Conversation: ...

class MakeVocab(Protocol):
    def __call__(
        self,
        id: UUID | None = None,
        student_id: UUID | None = None,
        term: str = "test",
        language: Language = Language("en"),
        pos: PartOfSpeech = PartOfSpeech.NOUN,
        definition: str = "Test definition",
        source: VocabularySource = VocabularySource.STUDENT,
        review_count: int = 1,
        now: datetime | None = None,
    ) -> VocabularyItem: ...


# Fixtures

@pytest.fixture
def make_chat_message() -> MakeChatMessage:
    def _factory(
        id: UUID | None = None,
        role: Role = Role.STUDENT,
        content: str = "Test message",
        now: datetime | None = None,
    ) -> ChatMessage:
        return ChatMessage(
            _id=id or uuid4(),
            _created_at=now or utc_now(),
            _role=role,
            _content=content
        )
    return _factory

@pytest.fixture
def make_student() -> MakeStudent:
    def _factory(
        id: UUID | None = None,
        native_lang: Language | None = None,
        target_lang: Language | None = None,
        level: CEFRLevel = CEFRLevel.B1,
        now: datetime | None = None,
    ) -> Student:
        return Student(
            _id=id or uuid4(),
            _created_at=now or utc_now(),
            _native_lang=native_lang or Language("fr"),
            _target_lang=target_lang or Language("en"),
            _level=level
        )
    return _factory

@pytest.fixture
def make_conversation(make_student: MakeStudent) -> MakeConversation:
    def _factory(
        id: UUID | None = None,
        student_id: UUID | None = None,
        native_lang: Language | None = None,
        target_lang: Language | None = None,
        messages: list[ChatMessage] | None = None,
        status: Status = Status.ACTIVE,
        title: str | None = None,
        now: datetime | None = None,
    ) -> Conversation:
        ts = now or utc_now()
        return Conversation(
            _id=id or uuid4(),
            _created_at=ts,
            _student_id=student_id or make_student().id,
            _native_lang=native_lang or Language("fr"),
            _target_lang=target_lang or Language("en"),
            _last_activity_at=ts,
            _status=status,
            _title=title or "Conversation",
            _messages=messages or []
        )
    return _factory

@pytest.fixture
def make_vocab(make_student: MakeStudent) -> MakeVocab:
    def _factory(
        id: UUID | None = None,
        student_id: UUID | None = None,
        term: str = "test",
        language: Language = Language("en"),
        pos: PartOfSpeech = PartOfSpeech.NOUN,
        definition: str = "Test definition",
        source: VocabularySource = VocabularySource.STUDENT,
        review_count: int = 1,
        now: datetime | None = None,
    ) -> VocabularyItem:
        lemma = Lemma(term=term, pos=pos, language=language)
        lexeme = Lexeme(lemma=lemma, definition=definition)
        ts = now or utc_now()
        
        return VocabularyItem(
            _id=id or uuid4(),
            _created_at=ts,
            _student_id=student_id or make_student().id,
            _lexeme=lexeme,
            _source=source,
            _last_reviewed_at=ts,
            _review_count=review_count
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