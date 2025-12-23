"""
Linguistics Value Objects

Defines linguistic and grammatical concepts for language analysis.
"""

from __future__ import annotations

from enum import Enum
from functools import total_ordering, lru_cache
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


@total_ordering
class CEFRLevel(Enum):
    """
    Common European Framework of Reference for Languages levels.
    
    Levels are ordered from beginner (A1) to proficient (C2).
    Supports comparison operations (e.g., CEFRLevel.B1 < CEFRLevel.B2).
    
    Levels:
        A1: Beginner
        A2: Elementary
        B1: Intermediate
        B2: Upper Intermediate
        C1: Advanced
        C2: Proficient
    """
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"

    @classmethod
    @lru_cache(maxsize=1) 
    def _get_ordered_members(cls) -> tuple[CEFRLevel, ...]:
        """
        Return all levels as tuple and cache it.
        """
        return tuple(cls)

    @property
    def is_beginner(self) -> bool:
        """Check if this is a beginner level (A1-A2)."""
        return self in (CEFRLevel.A1, CEFRLevel.A2)
    
    @property
    def is_intermediate(self) -> bool:
        """Check if this is an intermediate level (B1-B2)."""
        return self in (CEFRLevel.B1, CEFRLevel.B2)
    
    @property
    def is_advanced(self) -> bool:
        """Check if this is an advanced level (C1-C2)."""
        return self in (CEFRLevel.C1, CEFRLevel.C2)

    @property
    def description(self) -> str:
        """Get a description of the level."""
        descriptions = {
            CEFRLevel.A1: "Beginner - Can understand basic phrases",
            CEFRLevel.A2: "Elementary - Can communicate in simple tasks",
            CEFRLevel.B1: "Intermediate - Can deal with most travel situations",
            CEFRLevel.B2: "Upper Intermediate - Can interact with fluency",
            CEFRLevel.C1: "Advanced - Can express fluently and spontaneously",
            CEFRLevel.C2: "Proficient - Can understand everything",
        }
        return descriptions[self]

    @property
    def rank(self) -> int:
        """
        Get numeric value for comparison (1-6).
        Useful for progress tracking and level comparisons.
        """
        return self._get_ordered_members().index(self) + 1

    def is_adjacent_to(self, other: CEFRLevel) -> bool:
        """Verify the other rank is adjacent to this one."""
        return abs(self.rank - other.rank) == 1

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, CEFRLevel):
            return NotImplemented
        return self.rank < other.rank


class PartOfSpeech(Enum):
    """
    Standard parts of speech for linguistic analysis.

    These are used to classify vocabulary items and words in sentences.
    """
    
    NOUN = "NOUN"           # Nouns (person, place, thing)
    VERB = "VERB"           # Verbs (actions, states)
    ADJ = "ADJ"             # Adjectives (descriptors)
    ADV = "ADV"             # Adverbs (modify verbs/adjectives)
    PRON = "PRON"           # Pronouns (I, you, he, she)
    PREP = "PREP"           # Prepositions (in, on, at)
    CONJ = "CONJ"           # Conjunctions (and, but, or)
    DET = "DET"             # Determiners (the, a, this)
    INTJ = "INTJ"           # Interjections (wow, ouch)
    NUM = "NUM"             # Numerals (one, two, first)
    
    # Special categories
    PHRASE = "PHRASE"       # Multi-word expressions
    IDIOM = "IDIOM"         # Idiomatic expressions
    UNKNOWN = "UNKNOWN"     # Fallback for unknown POS


class GrammaticalNumber(str, Enum):
    """
    Grammatical number categories for nouns and pronouns.
    """
    
    SINGULAR = "singular"
    PLURAL = "plural"


class Gender(str, Enum):
    """
    Grammatical gender categories for nouns and pronouns.

    Neutral is used for languages without gender or for common gender.
    """
    
    MASCULINE = "masculine"
    FEMININE = "feminine"
    NEUTRAL = "neutral"


class Tense(str, Enum):
    """
    Grammatical tenses for verbs in linguistic analysis.
    """
    
    PRESENT = "present"
    PAST_COMPOUND = "past_compound" 
    IMPERFECT = "imperfect"
    FUTURE = "future"
    PAST_SIMPLE = "past_simple"
    PRESENT_PERFECT = "present_perfect"
    PAST_PERFECT = "past_perfect"
    FUTURE_PERFECT = "future_perfect"
    CONDITIONAL = "conditional"
    SUBJUNCTIVE = "subjunctive"
    IMPERATIVE = "imperative"


class Person(str, Enum):
    """
    Grammatical person categories for pronouns and verb conjugations.
    """
    
    FIRST = "1"
    SECOND = "2"
    THIRD = "3"


@dataclass(frozen=True, slots=True)
class Morphology:
    """
    Universal container for grammatical properties.
    
    All properties are optional and set to None when not applicable.
    This allows flexible representation across different languages and contexts.
    
    Attributes:
        number: Singular or plural (None if not applicable)
        gender: Masculine, feminine, or neutral (None if not applicable)
        person: First, second, or third person (None if not applicable)
        tense: Verb tense (None if not applicable)
    """
    number: GrammaticalNumber | None = None
    gender: Gender | None = None
    person: Person | None = None
    tense: Tense | None = None


@dataclass(frozen=True, slots=True)
class Lemma: 
    """
    Dictionary entry representing the canonical form of a word.
    
    The lemma is the base form used in dictionaries.
    For example, "run" is the lemma for "runs", "running", "ran".
    
    Attributes:
        term: The canonical form (e.g., "run")
        pos: Part of speech classification
        language: The language of this lemma
    """
    term: str             
    pos: PartOfSpeech  
    language: Language


@dataclass(frozen=True, slots=True)
class Lexeme:
    """
    Dictionary entry representing the abstract concept of a word.
    A lexeme represents the semantic meaning independent of grammatical form.
    Example: The verb concept "to run" encompasses "run", "runs", "running", "ran".
    
    Attributes:
        lemma: The base form and metadata
        definition: Human-readable definition
    """
    lemma: Lemma          
    definition: str


@dataclass(frozen=True, slots=True)
class WordForm:
    """
    The concrete occurrence of a word in a sentence.
    Links the specific form used to its dictionary entry and grammatical properties.
    Example: "mangés" (what is written) links to "manger" (lexeme) with specific morphology.
    
    Attributes:
        text: The actual word as written in the sentence
        lexeme: The dictionary entry this form belongs to
        morphology: Grammatical properties of this specific form
    """
    text: str             
    lexeme: Lexeme        
    morphology: Morphology


class SemanticRelationship(str, Enum):
    """
    Semantic relationships between lexemes for vocabulary network building.
    
    Used to establish connections between words for enhanced learning.
    
    Relationships:
        SYNONYM: Words with similar meanings
        ANTONYM: Words with opposite meanings
        HYPERNYM: More general category (e.g., "animal" for "dog")
        RELATED_TO: General semantic connection
    """
    SYNONYM = "SYNONYM"
    ANTONYM = "ANTONYM"
    HYPERNYM = "HYPERNYM"  
    RELATED_TO = "RELATED_TO"