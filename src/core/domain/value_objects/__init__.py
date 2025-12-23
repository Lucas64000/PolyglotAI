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

from .role import Role
from .linguistics import (
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
from .cefr_level import CEFRLevel
from .language import Language
from .status import Status
from .vocab_source import VocabularySource
from .teacher_profile import (
    GenerationStyle,
    CreativityLevel,
    TeacherProfile,
)

__all__ = [
    # Conversation
    "Role",
    "Status",
    # Linguistics
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
    # Language & Learning
    "CEFRLevel",
    "Language",
    "VocabularySource",
    # Teacher Configuration
    "GenerationStyle",
    "CreativityLevel",
    "TeacherProfile",
]
