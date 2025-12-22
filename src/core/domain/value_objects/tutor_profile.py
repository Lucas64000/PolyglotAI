"""
Tutor Profile Value Object

Defines the configuration for the tutor's behavior and generation style.
"""

from dataclasses import dataclass
from enum import Enum, IntEnum

class GenerationStyle(str, Enum):
    """
    Defines the pedagogical approach for generating tutoring responses.
    
    Styles:
        PRACTICE: Focus on exercises and drills
        EXPLANATORY: Provide detailed explanations
        CORRECTIVE: Emphasize error correction
        CONVERSATIONAL: Natural dialogue-based learning
    """
    PRACTICE = "practice"
    EXPLANATORY = "explanatory"
    CORRECTIVE = "corrective"
    CONVERSATIONAL = "conversational"


class CreativityLevel(IntEnum):
    """
    Controls the variability and expressiveness of generated responses.
    
    Levels:
        STRICT: Highly deterministic, consistent responses
        CONTROLLED: Moderate variation with guardrails
        MODERATE: Balanced creativity and consistency
        EXPRESSIVE: High variability and natural expressions
    """
    STRICT = 0
    CONTROLLED = 1
    MODERATE = 2
    EXPRESSIVE = 3


@dataclass(frozen=True, slots=True)
class TutorProfile:
    """
    Configures the AI tutor's behavior and response generation.
    
    The MVP does not validate all compatibility combinations
    (e.g., corrective style with expressive creativity may be ambiguous,
    but is acceptable for now).
    
    Attributes:
        creativity_level: How varied and expressive the tutor responses should be
        generation_style: The pedagogical approach for generating responses
    """

    creativity_level: CreativityLevel = CreativityLevel.MODERATE
    generation_style: GenerationStyle = GenerationStyle.CONVERSATIONAL