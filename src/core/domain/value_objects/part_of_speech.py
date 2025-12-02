"""
PartOfSpeech Value Object

Represents grammatical categories of words (noun, verb, adjective, etc.).
Used for vocabulary classification and grammar rule targeting.
"""

from enum import Enum


class PartOfSpeech(str, Enum):
    """
    Standard parts of speech for linguistic analysis.
    
    These are used to:
    - Classify vocabulary items
    - Target specific grammar rules
    - Provide appropriate exercises
    
    Values follow Universal Dependencies (UD) conventions where applicable.
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
    
    @property
    def is_content_word(self) -> bool:
        """
        Check if this is a content word (carries semantic meaning).
        Content words: nouns, verbs, adjectives, adverbs
        Function words: pronouns, prepositions, conjunctions, etc.
        """
        return self in (
            PartOfSpeech.NOUN, 
            PartOfSpeech.VERB, 
            PartOfSpeech.ADJ, 
            PartOfSpeech.ADV
        )
    
    @property
    def is_function_word(self) -> bool:
        """Check if this is a function word (grammatical role)."""
        return not self.is_content_word and self not in (
            PartOfSpeech.PHRASE, 
            PartOfSpeech.IDIOM
        )
    
    @property
    def french_name(self) -> str:
        """Get the French grammatical term."""
        names = {
            PartOfSpeech.NOUN: "nom",
            PartOfSpeech.VERB: "verbe",
            PartOfSpeech.ADJ: "adjectif",
            PartOfSpeech.ADV: "adverbe",
            PartOfSpeech.PRON: "pronom",
            PartOfSpeech.PREP: "préposition",
            PartOfSpeech.CONJ: "conjonction",
            PartOfSpeech.DET: "déterminant",
            PartOfSpeech.INTJ: "interjection",
            PartOfSpeech.NUM: "numéral",
            PartOfSpeech.PHRASE: "locution",
            PartOfSpeech.IDIOM: "expression idiomatique",
        }
        return names[self]
