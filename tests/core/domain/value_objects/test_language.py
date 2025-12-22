"""
Tests for Language value object.

Language represents an ISO 639-1 language code with validation.
Languages are immutable and normalized to lowercase.
"""

from __future__ import annotations

import pytest

from src.core.domain.value_objects import Language
from src.core.exceptions import InvalidLanguageIsoCodeError


class TestLanguageValidation:
    """Tests for language code validation at creation."""

    @pytest.mark.parametrize("input_code, expected", [
        ("FR", "fr"),
        ("  en  ", "en"),
        ("eS", "es"),
    ])
    def test_normalization(self, input_code: str, expected: str) -> None:
        """Language codes must be normalized to lowercase and stripped."""
        assert Language(input_code).code == expected

    @pytest.mark.parametrize("invalid_code", [
        "a",      # Too short
        "abc",    # Too long
        "12",     # Numeric
        "f!",     # Special char
        "",       # Empty
        "   ",    # Whitespace only
    ])
    def test_validation_rejects_invalid_codes(self, invalid_code: str) -> None:
        """ISO 639-1 requires exactly two alphabetic characters."""
        with pytest.raises(InvalidLanguageIsoCodeError):
            Language(invalid_code)