"""
Tests for ChatMessage entity.

ChatMessage represents a single message in a conversation.
Messages are classified by role (STUDENT, TEACHER).
"""

from __future__ import annotations

import pytest

from src.core.domain.value_objects import Role
from src.core.exceptions import InvalidChatMessageContentError
from tests.conftest import MakeChatMessage


class TestChatMessageCreation:
    """Tests for ChatMessage instantiation."""

    def test_student_message_has_content(
        self, make_chat_message: MakeChatMessage
    ) -> None:
        """Student messages have non-empty content."""
        message = make_chat_message(role=Role.STUDENT, content="Hello!")
        assert message.content == "Hello!"

    def test_teacher_message_has_content(
        self, make_chat_message: MakeChatMessage
    ) -> None:
        """Teacher messages have non-empty content."""
        message = make_chat_message(role=Role.TEACHER, content="Hi there!")
        assert message.content == "Hi there!"

    @pytest.mark.parametrize("role", [Role.STUDENT, Role.TEACHER], ids=["student", "teacher"])
    def test_empty_content_raises(
        self, make_chat_message: MakeChatMessage, role: Role
    ) -> None:
        """Student and teacher messages cannot have empty content."""
        with pytest.raises(InvalidChatMessageContentError):
            make_chat_message(role=role, content="")


class TestChatMessageClassification:
    """Tests for role-based classification."""

    def test_student_message_classification(
        self, make_chat_message: MakeChatMessage
    ) -> None:
        """Student messages report is_from_student=True."""
        message = make_chat_message(role=Role.STUDENT, content="Question")

        assert message.is_from_student is True
        assert message.is_from_teacher is False

    def test_teacher_message_classification(
        self, make_chat_message: MakeChatMessage
    ) -> None:
        """Teacher messages report is_from_teacher=True."""
        message = make_chat_message(role=Role.TEACHER, content="Answer")

        assert message.is_from_teacher is True
        assert message.is_from_student is False


class TestChatMessageEditing:
    """Tests for message content editing."""

    @pytest.mark.parametrize("role", [Role.STUDENT, Role.TEACHER], ids=["student", "teacher"])
    def test_messages_can_be_edited(
        self, make_chat_message: MakeChatMessage, role: Role
    ) -> None:
        """Student and teacher messages can have their content edited."""
        message = make_chat_message(role=role, content="Original content")
        
        message.edit_content("Updated content")
        
        assert message.content == "Updated content"

    @pytest.mark.parametrize("role", [Role.STUDENT, Role.TEACHER], ids=["student", "teacher"])
    def test_edit_with_empty_content_raises(
        self, make_chat_message: MakeChatMessage, role: Role
    ) -> None:
        """Editing a student message with empty content raises an error."""
        message = make_chat_message(role=role, content="Original content")
        
        with pytest.raises(InvalidChatMessageContentError):
            message.edit_content(" ")