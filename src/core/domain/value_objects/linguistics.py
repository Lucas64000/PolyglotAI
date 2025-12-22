"""
Linguistics Value Objects

Defines linguistic and grammatical concepts for language analysis.
"""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .language import Language

class PartOfSpeech(str, Enum):
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