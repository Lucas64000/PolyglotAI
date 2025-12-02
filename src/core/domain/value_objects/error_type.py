"""
ErrorType Value Object

Categorizes the types of linguistic errors a learner can make.
Used for tracking patterns and providing targeted feedback.
"""

from enum import Enum


class ErrorType(str, Enum):
    """
    Categories of linguistic errors for learning analytics.
    
    These categories help:
    - Track error patterns over time
    - Provide targeted grammar explanations
    - Link errors to relevant GrammarRules in the knowledge graph
    
    Examples:
        >>> error = ErrorType.CONJUGATION
        >>> error.description
        'Incorrect verb conjugation or tense usage'
    """
    
    # Grammar-related
    GRAMMAR = "grammar"           # General grammar mistakes
    CONJUGATION = "conjugation"   # Verb tense/form errors (e.g., "I goed" -> "I went")
    AGREEMENT = "agreement"       # Subject-verb or gender agreement
    SYNTAX = "syntax"             # Word order issues
    
    # Vocabulary-related
    VOCABULARY = "vocabulary"     # Wrong word choice
    SPELLING = "spelling"         # Orthographic errors
    
    # Usage-related
    PREPOSITION = "preposition"   # Wrong preposition (e.g., "depend of" -> "depend on")
    ARTICLE = "article"           # Missing or wrong article (a/an/the, le/la/les)
    IDIOM = "idiom"               # Literal translation of idioms
    
    # Style-related
    REGISTER = "register"         # Formal/informal mismatch
    PUNCTUATION = "punctuation"   # Punctuation errors
    
    @property
    def description(self) -> str:
        """Get a description of this error type for user feedback."""
        descriptions = {
            ErrorType.GRAMMAR: "General grammar mistake",
            ErrorType.CONJUGATION: "Incorrect verb conjugation or tense usage",
            ErrorType.AGREEMENT: "Subject-verb or gender/number agreement error",
            ErrorType.SYNTAX: "Incorrect word order or sentence structure",
            ErrorType.VOCABULARY: "Incorrect word choice for the context",
            ErrorType.SPELLING: "Spelling or orthographic error",
            ErrorType.PREPOSITION: "Incorrect preposition usage",
            ErrorType.ARTICLE: "Missing, extra, or incorrect article",
            ErrorType.IDIOM: "Non-idiomatic expression or literal translation",
            ErrorType.REGISTER: "Inappropriate formality level",
            ErrorType.PUNCTUATION: "Punctuation error",
        }
        return descriptions[self]
    
    @property
    def is_grammar_related(self) -> bool:
        """Check if this is a grammar-related error."""
        return self in (
            ErrorType.GRAMMAR, 
            ErrorType.CONJUGATION, 
            ErrorType.AGREEMENT, 
            ErrorType.SYNTAX
        )
    
    @property
    def is_vocabulary_related(self) -> bool:
        """Check if this is a vocabulary-related error."""
        return self in (ErrorType.VOCABULARY, ErrorType.SPELLING)
