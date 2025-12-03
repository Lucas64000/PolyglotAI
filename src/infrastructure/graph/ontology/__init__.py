"""
Graph Ontology Module

Contains the schema definitions for the knowledge graph:
- Node types (Vocabulary, Mistake, GrammarRule, etc.)
- Edge types (MemoryTrace, StrugglesWith, etc.)
- Schema constraints (which nodes can connect to which)

These are Pydantic models used by Graphiti for entity extraction.
"""

from .node_types import (
    Vocabulary,
    Definition,
    GrammarRule,
    Mistake,
    Topic,
    ExampleSentence,
    Exercise,
)
from .edge_types import (
    MemoryTrace,
    StrugglesWith,
    HasDefinition,
    IsFormOf,
    TranslationOf,
    BelongsTo,
    Illustrates,
    Tests,
)
from .schema import ENTITY_TYPES, EDGE_TYPES, EDGE_TYPE_MAP

__all__ = [
    # Node Types
    "Vocabulary",
    "Definition",
    "GrammarRule",
    "Mistake",
    "Topic",
    "ExampleSentence",
    "Exercise",
    # Edge Types
    "MemoryTrace",
    "StrugglesWith",
    "HasDefinition",
    "IsFormOf",
    "TranslationOf",
    "BelongsTo",
    "Illustrates",
    "Tests",
    # Schema
    "ENTITY_TYPES",
    "EDGE_TYPES",
    "EDGE_TYPE_MAP",
]
