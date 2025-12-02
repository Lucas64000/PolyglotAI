"""
LanguagePair Value Object

Represents a directional pair of languages (source -> target).
Used to define learning direction (e.g., French speaker learning English).
"""

from __future__ import annotations

from dataclasses import dataclass

from .language import Language


@dataclass(frozen=True, slots=True)
class LanguagePair:
    """
    Represents a directional language pair for learning.
    
    The source is the learner's native language.
    The target is the language being learned.
    
    Examples:
        >>> pair = LanguagePair(Language("fr"), Language("en"))
        >>> pair.source.code
        'fr'
        >>> pair.target.code
        'en'
        >>> pair.reversed()
        LanguagePair(source=Language('en'), target=Language('fr'))
    """
    
    source: Language  # Native language
    target: Language  # Language being learned
    
    def __post_init__(self) -> None:
        """Validate that source and target are different."""
        if self.source == self.target:
            raise ValueError(
                f"Source and target languages must be different. "
                f"Got: {self.source.code}"
            )
    
    def reversed(self) -> LanguagePair:
        """
        Return the reverse language pair.
        
        Useful for bidirectional learning or translation lookups.
        """
        return LanguagePair(source=self.target, target=self.source)
    
    def __str__(self) -> str:
        return f"{self.source.code}->{self.target.code}"
    
    def __repr__(self) -> str:
        return f"LanguagePair(source={self.source!r}, target={self.target!r})"
    
    @classmethod
    def french_to_english(cls) -> LanguagePair:
        """French speaker learning English."""
        return cls(Language.french(), Language.english())
    
    @classmethod
    def english_to_french(cls) -> LanguagePair:
        """English speaker learning French."""
        return cls(Language.english(), Language.french())
