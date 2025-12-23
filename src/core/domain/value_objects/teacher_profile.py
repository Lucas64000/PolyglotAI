"""
Teacher Profile Value Object

Defines the configuration for the teacher's behavior and generation style.
"""

from dataclasses import dataclass
from enum import Enum, IntEnum

class GenerationStyle(Enum):
    """
    Defines the pedagogical approach for the teacher's responses.
    
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
    Controls the variability and expressiveness of the teacher's responses.
    
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
class TeacherProfile:
    """
    Configures the teacher's behavior.
    
    Attributes:
        creativity_level: How varied and expressive the teacher responses should be
        generation_style: The pedagogical approach for giving responses
    """

    creativity_level: CreativityLevel = CreativityLevel.MODERATE
    generation_style: GenerationStyle = GenerationStyle.CONVERSATIONAL