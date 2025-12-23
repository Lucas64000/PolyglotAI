"""
Tests for Role value object.

Role represents the author of a chat message: STUDENT or TEACHER.
"""

from __future__ import annotations

import pytest

from src.core.domain.value_objects import Role


class TestRoleClassification:
    """Tests for role type classification."""

    @pytest.mark.parametrize("role, is_student, is_teacher", [
        (Role.STUDENT, True, False),
        (Role.TEACHER, False, True),
    ])
    def test_classification_logic(self, role: Role, is_student: bool, is_teacher: bool):
        """Ensure correct role-to-type mapping."""
        assert role.is_student is is_student
        assert role.is_teacher is is_teacher