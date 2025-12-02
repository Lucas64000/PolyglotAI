"""
Language Value Object

Represents a language using ISO 639-1 codes.
Immutable and validated on creation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True, slots=True)
class Language:
    """
    Represents a language with ISO 639-1 code validation.
    
    Examples:
        >>> english = Language("en")
        >>> french = Language("fr")
        >>> english == Language("en")
        True
    """
    
    code: str
    
    # Supported languages for PolyglotAI (extensible)
    SUPPORTED_CODES: ClassVar[frozenset[str]] = frozenset({
        "en",  # English
        "fr",  # French
        "es",  # Spanish (future)
        "de",  # German (future)
        "it",  # Italian (future)
    })
    
    # Human-readable names
    NAMES: ClassVar[dict[str, str]] = {
        "en": "English",
        "fr": "Français",
        "es": "Español",
        "de": "Deutsch",
        "it": "Italiano",
    }
    
    def __post_init__(self) -> None:
        """Validate the language code."""
        # Normalize to lowercase
        object.__setattr__(self, "code", self.code.lower())
        
        if self.code not in self.SUPPORTED_CODES:
            raise ValueError(
                f"Unsupported language code: '{self.code}'. "
                f"Supported: {', '.join(sorted(self.SUPPORTED_CODES))}"
            )
    
    @property
    def name(self) -> str:
        """Get the human-readable name of the language."""
        return self.NAMES.get(self.code, self.code.upper())
    
    def __str__(self) -> str:
        return self.code
    
    def __repr__(self) -> str:
        return f"Language({self.code!r})"
    
    # We will add more languages in the future
    @classmethod
    def english(cls) -> Language:
        """Create an English language instance."""
        return cls("en")
    
    @classmethod
    def french(cls) -> Language:
        """Create a French language instance."""
        return cls("fr")
    