"""
Tests for CEFRLevel value object.
"""

from __future__ import annotations

import pytest
from typing import Any

from src.core.domain.value_objects import CEFRLevel


class TestCEFRLevelCategories:
    """Tests for level categorization (beginner/intermediate/advanced)."""

    @pytest.mark.parametrize("level, is_beginner, is_intermediate, is_advanced", [
        (CEFRLevel.A1, True, False, False),
        (CEFRLevel.A2, True, False, False),
        (CEFRLevel.B1, False, True, False),
        (CEFRLevel.B2, False, True, False),
        (CEFRLevel.C1, False, False, True),
        (CEFRLevel.C2, False, False, True),
    ])
    def test_categories_and_invariants(self, level: CEFRLevel, is_beginner: bool, is_intermediate: bool, is_advanced: bool):
        """Each level must map to exactly one educational category."""
        assert level.is_beginner is is_beginner
        assert level.is_intermediate is is_intermediate
        assert level.is_advanced is is_advanced
        assert sum([level.is_beginner, level.is_intermediate, level.is_advanced]) == 1

    def test_total_ordering(self):
        """Levels must follow the strict CEFR hierarchy for progression logic."""
        expected = [
            CEFRLevel.A1, CEFRLevel.A2, 
            CEFRLevel.B1, CEFRLevel.B2, 
            CEFRLevel.C1, CEFRLevel.C2
        ]
        assert sorted(list(CEFRLevel)) == expected
        assert CEFRLevel.A1 < CEFRLevel.B1
        assert CEFRLevel.C2 > CEFRLevel.C1

    @pytest.mark.parametrize("level, other, expected", [
        (CEFRLevel.A1, CEFRLevel.A2, True),   
        (CEFRLevel.B2, CEFRLevel.B1, True),   
        (CEFRLevel.A1, CEFRLevel.B1, False),  
        (CEFRLevel.A1, CEFRLevel.A1, False),  
        (CEFRLevel.C1, CEFRLevel.C2, True),   
    ])
    def test_is_adjacent_to(self, level: CEFRLevel, other: CEFRLevel, expected: bool):
        """Adjacency is strictly defined as a distance of 1 rank."""
        assert level.is_adjacent_to(other) is expected

    @pytest.mark.parametrize("invalid_type", [
        "B2",           
        2,              
        None,           
    ], ids=["string", "int", "none"])
    def test_comparison_with_different_types_raises_type_error(self, invalid_type: Any):
        """Comparing CEFRLevel with non-CEFRLevel types raises TypeError."""
        with pytest.raises(TypeError):
            CEFRLevel.B1 < invalid_type # type: ignore
    
    @pytest.mark.parametrize("invalid_type", [
    "B2",           
    2,              
    None,           
    ], ids=["string", "int", "none"])
    def test_equality_with_different_types_returns_false(self, invalid_type: Any):
        """Equality comparison with non-CEFRLevel types returns False (not error)."""
        assert (CEFRLevel.B1 == invalid_type) is False