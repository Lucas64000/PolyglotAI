"""
Tests for ChatMessage entity.

ChatMessage represents a single message in a conversation.
Messages are classified by role (USER, ASSISTANT, SYSTEM).
"""

from __future__ import annotations

import pytest

from src.core.domain.value_objects import Role
from src.core.exceptions import InvalidChatMessageContentError, InvalidChatMessageEditError
from tests.conftest import MakeChatMessage


class TestChatMessageCreation:
    """Tests for ChatMessage instantiation."""

    def test_user_message_has_content(
        self, make_chat_message: MakeChatMessage
    ) -> None:
        """User messages have non-empty content."""
        message = make_chat_message(role=Role.USER, content="Hello!")
        assert message.content == "Hello!"

    def test_assistant_message_has_content(
        self, make_chat_message: MakeChatMessage
    ) -> None:
        """Assistant messages have non-empty content."""
        message = make_chat_message(role=Role.ASSISTANT, content="Hi there!")
        assert message.content == "Hi there!"

    def test_system_message_can_be_empty(
        self, make_chat_message: MakeChatMessage
    ) -> None:
        """System messages can have empty content."""
        message = make_chat_message(role=Role.SYSTEM, content="")
        assert message.content == ""

    def test_system_message_can_have_content(
        self, make_chat_message: MakeChatMessage
    ) -> None:
        """System messages can also have content."""
        message = make_chat_message(role=Role.SYSTEM, content="You are a helpful tutor.")
        assert message.content == "You are a helpful tutor."

    @pytest.mark.parametrize("role", [Role.USER, Role.ASSISTANT], ids=["user", "assistant"])
    def test_empty_content_raises_for_non_system_roles(
        self, make_chat_message: MakeChatMessage, role: Role
    ) -> None:
        """Invariant: User/Assistant messages cannot have empty content."""
        with pytest.raises(InvalidChatMessageContentError):
            make_chat_message(role=role, content="")


class TestChatMessageClassification:
    """Tests for role-based classification."""

    def test_user_message_classification(
        self, make_chat_message: MakeChatMessage
    ) -> None:
        """User messages report is_from_user=True."""
        message = make_chat_message(role=Role.USER, content="Question")

        assert message.is_from_user is True
        assert message.is_from_assistant is False
        assert message.is_system_message is False

    def test_assistant_message_classification(
        self, make_chat_message: MakeChatMessage
    ) -> None:
        """Assistant messages report is_from_assistant=True."""
        message = make_chat_message(role=Role.ASSISTANT, content="Answer")

        assert message.is_from_assistant is True
        assert message.is_from_user is False
        assert message.is_system_message is False

    def test_system_message_classification(
        self, make_chat_message: MakeChatMessage
    ) -> None:
        """System messages report is_system_message=True."""
        message = make_chat_message(role=Role.SYSTEM, content="You are a tutor")

        assert message.is_system_message is True
        assert message.is_from_user is False
        assert message.is_from_assistant is False


class TestChatMessageEditing:
    """Tests for message content editing."""

    def test_user_message_can_be_edited(
        self, make_chat_message: MakeChatMessage
    ) -> None:
        """User messages can have their content edited."""
        message = make_chat_message(role=Role.USER, content="Original content")
        
        message.edit_content("Updated content")
        
        assert message.content == "Updated content"

    def test_assistant_message_cannot_be_edited(
        self, make_chat_message: MakeChatMessage
    ) -> None:
        """Assistant messages cannot be edited."""
        message = make_chat_message(role=Role.ASSISTANT, content="AI response")
        
        with pytest.raises(InvalidChatMessageEditError):
            message.edit_content("Trying to edit AI message")

    def test_system_message_cannot_be_edited(
        self, make_chat_message: MakeChatMessage
    ) -> None:
        """System messages cannot be edited."""
        message = make_chat_message(role=Role.SYSTEM, content="System prompt")
        
        with pytest.raises(InvalidChatMessageEditError):
            message.edit_content("Trying to edit system message")

    def test_edit_with_empty_content_raises(
        self, make_chat_message: MakeChatMessage
    ) -> None:
        """Editing a user message with empty content raises an error."""
        message = make_chat_message(role=Role.USER, content="Original content")
        
        with pytest.raises(InvalidChatMessageContentError):
            message.edit_content("")