"""
Graph Node Types

Pydantic models for graph entities (nodes).
These define the structure of data stored in Neo4j.

Note: User node is managed separately to avoid duplicates.
"""

from pydantic import BaseModel, Field
from typing import Optional


class Vocabulary(BaseModel):
    """
    Represents a valid dictionary entry.
    
    CRITICAL RULES:
    1. Extract ONLY the dictionary form (Lemma). Ex: for "ate", extract "eat".
    2. DO NOT include mistakes here. If the word is misspelled, ignore.
    3. DO NOT include sentences. Use ExampleSentence for that.
    
    DEDUPLICATION RULES:
    1. REUSE existing Vocabulary nodes - do NOT create duplicates.
    2. 'bonjour' mentioned twice should be ONE node, not two.
    3. Match by (term + language) - if exists, reuse it.
    """
    term: str = Field(
        ..., 
        description="The lemma/dictionary form of the word (e.g., 'eat', 'house'). MUST be unique per language."
    )
    language: str = Field(
        ..., 
        description="ISO 639-1 code (en, fr, es)."
    )
    pos: Optional[str] = Field(
        None, 
        description="Part of speech: NOUN, VERB, ADJ, ADV."
    )


class Definition(BaseModel):
    """
    Represents a specific meaning of a vocabulary word.
    """
    text: str = Field(
        ..., 
        description="The definition in the user's native language."
    )
    context_usage: Optional[str] = Field(
        None, 
        description="Ex: 'Formal', 'Slang', 'Medical context'."
    )


class GrammarRule(BaseModel):
    """
    Represents a linguistic rule or concept.
    
    DEDUPLICATION RULES:
    1. REUSE existing GrammarRule nodes - do NOT create duplicates.
    2. 'Contraction à+le=au' is ONE rule, not multiple.
    3. Match by rule_name - if a similar rule exists, reuse it.
    """
    rule_name: str = Field(
        ..., 
        description="Standard academic name (e.g., 'Contraction à+le', 'Passé composé avec être'). MUST be unique."
    )
    explanation: str = Field(
        ..., 
        description="Short pedagogical explanation."
    )
    language: str = Field(
        ..., 
        description="Language of the rule."
    )


class Mistake(BaseModel):
    """
    Represents a specific error pattern made by the user.
    
    DEDUPLICATION RULES:
    1. REUSE existing Mistake nodes if the error pattern is the same.
    2. 'à le' -> 'au' is the SAME mistake whether in 'à le magasin' or 'à le cinéma'.
    3. Focus on the GRAMMATICAL PATTERN, not the specific sentence.
    4. If a similar Mistake already exists, DO NOT create a new one.
    
    Examples of SAME mistake (should be ONE node):
    - 'à le magasin' and 'à le parc' -> same pattern: 'à le' -> 'au'
    - 'j'ai allé' and 'j'ai parti' -> same pattern: movement verb + avoir -> être
    """
    wrong_form: str = Field(
        ..., 
        description="The ERROR PATTERN (not full sentence). E.g., 'à le' not 'à le magasin'."
    )
    correction: str = Field(
        ..., 
        description="The corrected pattern. E.g., 'au' not 'au magasin'."
    )
    explanation: Optional[str] = Field(
        None, 
        description="Why it is wrong."
    )


class Topic(BaseModel):
    """
    Represents the semantic theme of the conversation.
    """
    topic_name: str = Field(
        ..., 
        description="High-level topic (e.g., 'Travel', 'Food', 'Business')."
    )


class ExampleSentence(BaseModel):
    """
    Represents a full sentence context.
    """
    text: str = Field(
        ..., 
        description="The full sentence verifying a usage."
    )
    language: str = Field(
        ..., 
        description="ISO code."
    )


class Exercise(BaseModel):
    """
    Represents a pedagogical activity.
    """
    type: str = Field(
        ..., 
        description="Type: 'translation', 'fill_in_blanks'."
    )
    instruction: str = Field(
        ..., 
        description="The question asked."
    )
