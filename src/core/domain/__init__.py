"""
Domain Package

Contains the core domain model: entities, value objects, and domain logic.
Represents the business concepts and rules for language learning.

All classes in this package are:
- Framework-independent
- Self-contained
- Testable in isolation
- Expressing business concepts and invariants
"""

from .entities import (
    ChatMessage,
    Conversation,
    Entity,
    Student,
    VocabularyItem,
)
from .value_objects import (
    Role, 
    PartOfSpeech,
    GrammaticalNumber,
    Gender,
    Tense,
    Person,
    Morphology,
    Lemma,
    Lexeme, 
    WordForm, 
    SemanticRelationship,
    CEFRLevel,
    Language,
    Status,
    VocabularySource,
    GenerationStyle,
    CreativityLevel,
    TeacherProfile,
)

__all__ = [
    # Entities
    "ChatMessage",
    "Conversation",
    "Entity",
    "Student",
    "VocabularyItem",
    # Value Objects
    "Role",
    "Status",
    "PartOfSpeech",
    "GrammaticalNumber",
    "Gender",
    "Tense",
    "Person",
    "Morphology",
    "Lemma",
    "Lexeme",
    "WordForm",
    "SemanticRelationship",
    "CEFRLevel",
    "Language",
    "VocabularySource",
    "GenerationStyle",
    "CreativityLevel",
    "TeacherProfile",
]
