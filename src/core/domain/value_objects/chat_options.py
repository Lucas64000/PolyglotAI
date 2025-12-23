"""
Chat Configuration Value Objects

Defines conversation roles, status, and teacher behavior configuration.
"""

from dataclasses import dataclass
from enum import Enum, IntEnum


class Role(Enum):
    """
    Represents the role of a message sender in a conversation.
    
    Roles:
        STUDENT: Messages from the student
        TEACHER: Messages from the teacher
    """
    
    STUDENT = "student"
    TEACHER = "teacher"
    
    @property
    def is_student(self) -> bool:
        """Check if this role represents the student."""
        return self == Role.STUDENT
    
    @property
    def is_teacher(self) -> bool:
        """Check if this role represents the teacher."""
        return self == Role.TEACHER


class Status(Enum):
    """
    Represents the status of a conversation.
    
    Statuses:
        ACTIVE: Conversation is open and accepting new messages
        ARCHIVED: Conversation is read-only and no new messages can be added
        DELETED: Conversation is marked for deletion 
    """
    
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"
    
    @property
    def is_active(self) -> bool:
        """Check if this conversation is active."""
        return self == Status.ACTIVE
    
    @property
    def is_archived(self) -> bool:
        """Check if this conversation is archived."""
        return self == Status.ARCHIVED
    
    @property
    def is_writable(self) -> bool:
        """Check if new messages can be added to this conversation."""
        return self.is_active


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

    def __repr__(self) -> str:
        """
        Returns a human-readable description of the teacher's behavior configuration
        suitable for humans or LLM system prompts.
        """
        creativity_descriptions = {
            CreativityLevel.STRICT: "strictly deterministic and consistent",
            CreativityLevel.CONTROLLED: "controlled with moderate variation",
            CreativityLevel.MODERATE: "naturally varied and expressive",
            CreativityLevel.EXPRESSIVE: "highly variable and creative",
        }
        
        style_instructions = {
            GenerationStyle.PRACTICE: "focus on exercises and drills to reinforce learning",
            GenerationStyle.EXPLANATORY: "provide detailed explanations and deep understanding",
            GenerationStyle.CORRECTIVE: "emphasize error correction and guidance toward correct responses",
            GenerationStyle.CONVERSATIONAL: "use natural dialogue and conversational language",
        }
        
        creativity_desc = creativity_descriptions[self.creativity_level]
        style_desc = style_instructions[self.generation_style]
        
        return (
            f"This is how you should answer:\n"
            f"- Style: {style_desc}\n"
            f"- Tone: {creativity_desc}"
        )
