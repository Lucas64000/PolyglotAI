"""
Tests for Conversation entity.

Conversation represents a conversation thread between a User and the AI tutor.
Conversations can be ACTIVE, ARCHIVED, or DELETED.
"""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from uuid import uuid4

import pytest

from src.core.domain.entities import ChatMessage, Conversation
from src.core.domain.value_objects import Status, Role
from src.core.exceptions import ConversationNotWritableError, EmptyConversationTitleError, ConversationTitleTooLongError
from tests.conftest import MakeConversation


class TestConversationCreation:
    """Tests for Conversation instantiation."""

    def test_new_conversation_is_empty(
        self, make_conversation: MakeConversation
    ) -> None:
        """New conversations start with zero messages."""
        conversation = make_conversation()

        assert conversation.message_count == 0
        assert conversation.messages == ()

    def test_new_conversation_is_active(
        self, make_conversation: MakeConversation
    ) -> None:
        """New conversations start with ACTIVE status."""
        conversation = make_conversation()

        assert conversation.status == Status.ACTIVE
        assert conversation.status.is_active is True

    def test_conversation_has_user_id(
        self, make_conversation: MakeConversation
    ) -> None:
        """Conversations are associated with a user."""
        user_id = uuid4()
        conversation = make_conversation(user_id=user_id)

        assert conversation.user_id == user_id

    def test_conversation_has_default_title(
        self, make_conversation: MakeConversation
    ) -> None:
        """New conversations have a default title.""" 
        conversation = make_conversation()

        assert conversation.title == "Conversation"

    def test_conversation_can_have_custom_title(
        self, make_conversation: MakeConversation
    ) -> None:
        """Conversations can be created with a custom title."""
        conversation = make_conversation(title="Custom Title")

        assert conversation.title == "Custom Title"

    def test_create_conversation_with_empty_title_raises_error(self) -> None:
        """Creating a conversation with empty title raises EmptyConversationTitleError."""
        id = uuid4()
        user_id = uuid4()
        now = datetime.now(timezone.utc)
        title = ""

        with pytest.raises(EmptyConversationTitleError):
            Conversation.create_new(
                id=id,
                user_id=user_id,
                now=now,
                title=title
            )

    def test_create_conversation_with_too_long_title_raises_error(
            self
        ) -> None:
        """Creating a conversation with title longer than 100 chars raises ConversationTitleTooLongError."""
        id = uuid4()
        user_id = uuid4()
        now = datetime.now(timezone.utc)
        long_title = "A" * 101

        with pytest.raises(ConversationTitleTooLongError):
            Conversation.create_new(
                id=id,
                user_id=user_id,
                now=now,
                title=long_title
            )
        
    def test_conversation_timestamps_are_set(
        self, make_conversation: MakeConversation
    ) -> None:
        """Conversation creation sets timestamps."""
        now = datetime.now(timezone.utc)
        conversation = make_conversation(now=now)

        assert conversation.created_at == now
        assert conversation.last_activity_at == now


class TestConversationMessages:
    """Tests for adding messages to a conversation."""

    def test_add_message_increases_count(
        self, make_conversation: MakeConversation
    ) -> None:
        """Adding a message increases the message count."""
        conversation = make_conversation()
        now = datetime.now(timezone.utc)

        conversation.add_message(
            new_message_id=uuid4(),
            now=now,
            role=Role.USER,
            content="Hello"
        )

        assert conversation.message_count == 1

    def test_add_message_returns_chat_message(
        self, make_conversation: MakeConversation
    ) -> None:
        """add_message returns a ChatMessage instance."""
        conversation = make_conversation()
        now = datetime.now(timezone.utc)

        message = conversation.add_message(
            new_message_id=uuid4(),
            now=now,
            role=Role.USER,
            content="Hello"
        )

        assert isinstance(message, ChatMessage)
        assert message.content == "Hello"
        assert message.role == Role.USER
        
    def test_add_message_updates_last_activity(
        self, make_conversation: MakeConversation
    ) -> None:
        """Adding a message updates the last_activity_at timestamp."""
        initial_time = datetime.now(timezone.utc)
        conversation = make_conversation(now=initial_time)
        
        later_time = initial_time + timedelta(minutes=5)
        conversation.add_message(
            new_message_id=uuid4(),
            now=later_time,
            role=Role.USER,
            content="Hello"
        )

        assert conversation.last_activity_at == later_time

    def test_add_multiple_messages(
        self, make_conversation: MakeConversation
    ) -> None:
        """Multiple messages can be added to a conversation."""
        conversation = make_conversation()
        now = datetime.now(timezone.utc)

        conversation.add_message(
            new_message_id=uuid4(),
            now=now,
            role=Role.USER,
            content="Hello"
        )
        conversation.add_message(
            new_message_id=uuid4(),
            now=now + timedelta(seconds=1),
            role=Role.ASSISTANT,
            content="Hi there!"
        )
        conversation.add_message(
            new_message_id=uuid4(),
            now=now + timedelta(seconds=2),
            role=Role.USER,
            content="How are you?"
        )

        assert conversation.message_count == 3

    def test_messages_property_returns_tuple(
        self, make_conversation: MakeConversation
    ) -> None:
        """messages property returns an immutable tuple."""
        conversation = make_conversation()
        now = datetime.now(timezone.utc)

        conversation.add_message(
            new_message_id=uuid4(),
            now=now,
            role=Role.USER,
            content="Hello"
        )

        messages = conversation.messages
        
        assert isinstance(messages, tuple)
        assert len(messages) == 1

    def test_messages_preserve_order(
        self, make_conversation: MakeConversation
    ) -> None:
        """Messages are returned in the order they were added."""
        conversation = make_conversation()
        now = datetime.now(timezone.utc)

        msg1 = conversation.add_message(
            new_message_id=uuid4(),
            now=now,
            role=Role.USER,
            content="First"
        )
        msg2 = conversation.add_message(
            new_message_id=uuid4(),
            now=now + timedelta(seconds=1),
            role=Role.ASSISTANT,
            content="Second"
        )

        assert conversation.messages[0] == msg1
        assert conversation.messages[1] == msg2


class TestConversationLifecycle:
    """Tests for conversation state transitions."""

    def test_archive_changes_status(
        self, make_conversation: MakeConversation
    ) -> None:
        """Archiving changes status to ARCHIVED."""
        conversation = make_conversation()
        now = datetime.now(timezone.utc)

        conversation.archive(now)

        assert conversation.status == Status.ARCHIVED
        assert conversation.status.is_archived is True

    def test_archive_updates_last_activity(
        self, make_conversation: MakeConversation
    ) -> None:
        """Archiving updates last_activity_at timestamp."""
        initial_time = datetime.now(timezone.utc)
        conversation = make_conversation(now=initial_time)
        
        archive_time = initial_time + timedelta(hours=1)
        conversation.archive(archive_time)

        assert conversation.last_activity_at == archive_time

    def test_cannot_add_message_when_archived(
        self, make_conversation: MakeConversation
    ) -> None:
        """Archived conversations are read-only."""
        conversation = make_conversation()
        now = datetime.now(timezone.utc)
        conversation.archive(now)

        with pytest.raises(ConversationNotWritableError):
            conversation.add_message(
                new_message_id=uuid4(),
                now=now + timedelta(seconds=1),
                role=Role.USER,
                content="Too late"
            )

    def test_delete_changes_status(
        self, make_conversation: MakeConversation
    ) -> None:
        """Deleting changes status to DELETED."""
        conversation = make_conversation()
        now = datetime.now(timezone.utc)

        conversation.delete(now)

        assert conversation.status == Status.DELETED

    def test_delete_updates_last_activity(
        self, make_conversation: MakeConversation
    ) -> None:
        """Deleting updates last_activity_at timestamp."""
        initial_time = datetime.now(timezone.utc)
        conversation = make_conversation(now=initial_time)
        
        delete_time = initial_time + timedelta(hours=1)
        conversation.delete(delete_time)

        assert conversation.last_activity_at == delete_time

    def test_cannot_add_message_when_deleted(
        self, make_conversation: MakeConversation
    ) -> None:
        """Deleted conversations cannot accept messages."""
        conversation = make_conversation()
        now = datetime.now(timezone.utc)
        conversation.delete(now)

        with pytest.raises(ConversationNotWritableError):
            conversation.add_message(
                new_message_id=uuid4(),
                now=now + timedelta(seconds=1),
                role=Role.USER,
                content="Message to deleted conversation"
            )

    def test_modify_title_successfully(
        self, make_conversation: MakeConversation
    ) -> None:
        """Modifying title updates the title and last activity.""" 
        conversation = make_conversation(title="Old Title")
        now = datetime.now(timezone.utc)
        new_time = now + timedelta(hours=1)

        conversation.modify_title("New Title", new_time)

        assert conversation.title == "New Title"
        assert conversation.last_activity_at == new_time

    def test_modify_title_strips_whitespace(
        self, make_conversation: MakeConversation
    ) -> None:
        """Title modification strips leading/trailing whitespace."""
        conversation = make_conversation()
        now = datetime.now(timezone.utc)

        conversation.modify_title("  Spaced Title  ", now)

        assert conversation.title == "Spaced Title"

    def test_modify_title_empty_raises_error(
        self, make_conversation: MakeConversation
    ) -> None:
        """Cannot edit title with an empty content."""
        conversation = make_conversation()
        now = datetime.now(timezone.utc)

        with pytest.raises(EmptyConversationTitleError):
            conversation.modify_title("", now)

        with pytest.raises(EmptyConversationTitleError):
            conversation.modify_title("   ", now)

    def test_modify_title_too_long_raises_error(
        self, make_conversation: MakeConversation
    ) -> None:
        """Title cannot be longer than 100 characters (max_len)."""
        conversation = make_conversation()
        now = datetime.now(timezone.utc)
        long_title = "A" * 101  # 101 characters

        with pytest.raises(ConversationTitleTooLongError):
            conversation.modify_title(long_title, now)

    def test_modify_title_when_archived_raises_error(
        self, make_conversation: MakeConversation
    ) -> None:
        """Cannot modify title of archived conversation."""
        conversation = make_conversation()
        now = datetime.now(timezone.utc)
        conversation.archive(now)

        with pytest.raises(ConversationNotWritableError):
            conversation.modify_title("New Title", now + timedelta(seconds=1))

    def test_modify_title_when_deleted_raises_error(
        self, make_conversation: MakeConversation
    ) -> None:
        """Cannot modify title of deleted conversation."""
        conversation = make_conversation()
        now = datetime.now(timezone.utc)
        conversation.delete(now)

        with pytest.raises(ConversationNotWritableError):
            conversation.modify_title("New Title", now + timedelta(seconds=1))


class TestConversationTouch:
    """Tests for the touch method."""

    def test_touch_updates_last_activity(
        self, make_conversation: MakeConversation
    ) -> None:
        """touch() updates last_activity_at timestamp."""
        initial_time = datetime.now(timezone.utc)
        conversation = make_conversation(now=initial_time)
        
        new_time = initial_time + timedelta(minutes=30)
        conversation.touch(new_time)

        assert conversation.last_activity_at == new_time