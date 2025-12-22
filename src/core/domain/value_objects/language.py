"""
Language Value Object

Represents a language using ISO 639-1 codes.
"""

from dataclasses import dataclass

from src.core.exceptions import InvalidLanguageIsoCodeError

@dataclass(frozen=True, slots=True)
class Language:
    """
    Represents a language with ISO 639-1 code validation.
    
    The code is normalized to lowercase on instantiation.
    
    Attributes:
        code: ISO 639-1 language code (2 characters)
    
    Examples:
        >>> english = Language("en")
        >>> spanish = Language("ES")  # lowered to "es"
        >>> french = Language(" fr")  # stripped to "fr" 
    """
    code: str
    
    def __post_init__(self) -> None:
        """
        Validate the language code format.
        
        Normalizes the code to lowercase and validates ISO 639-1 format (2 characters).
        
        Raises:
            InvalidLanguageIsoCodeError: If code is not 2 alphabetic characters
        """
        normalized = self.code.lower().strip()
        # We need to use setattr because this is a frozen dataclass
        object.__setattr__(self, "code", normalized)
        if not self.code.isalpha() or len(self.code) != 2:
            raise InvalidLanguageIsoCodeError(self.code)    