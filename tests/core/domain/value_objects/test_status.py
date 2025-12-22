"""
Tests for Status value object.

Status represents the lifecycle state of a Conversation: ACTIVE, ARCHIVED, DELETED.
"""

from __future__ import annotations

import pytest

from src.core.domain.value_objects import Status


class TestStatusFlags:
    """Tests for status boolean flags."""

    @pytest.mark.parametrize("status, is_active, is_archived, is_writable", [
        (Status.ACTIVE, True, False, True),
        (Status.ARCHIVED, False, True, False),
        (Status.DELETED, False, False, False),
    ])
    def test_status_logic_flags(self, status: Status, is_active: bool, is_archived: bool, is_writable: bool):
        """Ensure lifecycle flags match business rules."""
        assert status.is_active is is_active
        assert status.is_archived is is_archived
        assert status.is_writable is is_writable