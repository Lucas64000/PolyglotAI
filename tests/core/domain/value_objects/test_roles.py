"""
Tests for Role value object.

Role represents the author of a chat message: USER, ASSISTANT, or SYSTEM.
"""

from __future__ import annotations

import pytest

from src.core.domain.value_objects import Role


class TestRoleClassification:
    """Tests for role type classification."""

    @pytest.mark.parametrize("role, is_human, is_ai, is_system", [
        (Role.USER, True, False, False),
        (Role.ASSISTANT, False, True, False),
        (Role.SYSTEM, False, False, True),
    ])
    def test_classification_logic(self, role: Role, is_human: bool, is_ai: bool, is_system: bool):
        """Ensure correct role-to-type mapping."""
        assert role.is_human is is_human
        assert role.is_ai is is_ai
        assert role.is_system is is_system