"""
Value Objects Package

Contains immutable domain value objects - objects defined by their attributes.
Value objects have no unique identity and are compared by value.

Categories:
- Language & Learning: Language, CEFRLevel
- Conversation: Role, Status
- Teacher Configuration: TeacherProfile, CreativityLevel, GenerationStyle
- Linguistics: PartOfSpeech, Gender, Tense, Person, Morphology, Lemma, Lexeme, WordForm, SemanticRelationship
- Vocabulary: VocabularySource
"""

from .chat_options import (
    Role,
    Status,
    GenerationStyle,
    CreativityLevel,
    TeacherProfile,
)
from .linguistics import (
    Language,
    CEFRLevel,
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
)

__all__ = [
    # Conversation
    "Role",
    "Status",
    # Linguistics
    "Language",
    "CEFRLevel",
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
    # Teacher Configuration
    "GenerationStyle",
    "CreativityLevel",
    "TeacherProfile",
]
