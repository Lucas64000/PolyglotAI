"""
Graph Edge Types

Pydantic models for graph relationships (edges).
These define how nodes connect to each other.
"""

from datetime import datetime
from pydantic import BaseModel, Field


class MemoryTrace(BaseModel):
    """
    Links USER -> CONCEPT (Vocabulary or GrammarRule).
    
    Represents the state of learning.
    Created when a user encounters a word/rule.
    """
    stability: float = Field(
        0.1, 
        description="SRS Stability. 0.1=New, 1.0=Mastered."
    )
    last_review: datetime = Field(
        default_factory=datetime.now,
        description="When the concept was last reviewed."
    )


class StrugglesWith(BaseModel):
    """
    Links LEARNER -> MISTAKE (error pattern).
    
    CRITICAL: This edge tracks how many times the learner made this error.
    
    DEDUPLICATION RULES:
    1. If a StrugglesWith edge already exists between Learner and a Mistake,
       DO NOT create a new edge. Instead, INCREMENT occurrence_count.
    2. One Learner should have AT MOST ONE StrugglesWith edge per Mistake pattern.
    
    Example: If learner says "à le magasin" then "à le cinéma", this is the 
    SAME error pattern. Increment occurrence_count to 2, don't create 2 edges.
    """
    occurrence_count: int = Field(
        1, 
        description="How many times this exact error occurred. INCREMENT on repeat, don't create new edge."
    )


class HasDefinition(BaseModel):
    """
    Links VOCABULARY -> DEFINITION.
    
    A vocabulary word can have multiple definitions.
    """
    pass


class IsFormOf(BaseModel):
    """
    Links VOCABULARY (Conjugated) -> VOCABULARY (Lemma).
    
    Ex: 'Went' -> 'Go'.
    """
    grammatical_features: str = Field(
        ..., 
        description="Ex: 'Past Tense', 'Plural'."
    )


class TranslationOf(BaseModel):
    """
    Links DEFINITION (Lang A) -> DEFINITION (Lang B).
    
    Do NOT link Vocabulary directly if definitions differ.
    """
    confidence: float = Field(
        1.0,
        description="Translation confidence (0.0-1.0)."
    )


class BelongsTo(BaseModel):
    """
    Links CONCEPT -> TOPIC.
    
    Ex: 'Fork' -> 'Kitchen'.
    """
    pass


class Illustrates(BaseModel):
    """
    Links EXAMPLE_SENTENCE -> VOCABULARY/RULE.
    
    Shows how a word or rule is used in context.
    """
    pass


class Tests(BaseModel):
    """
    Links EXERCISE -> VOCABULARY/RULE.
    
    Connects exercises to the concepts they test.
    """
    pass
