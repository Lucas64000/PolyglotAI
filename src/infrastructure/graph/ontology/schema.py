"""
Graph Schema Configuration

Defines which entity and edge types are available,
and constrains which nodes can connect to which.
"""

from typing import Type
from pydantic import BaseModel

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


# Mapping of entity type names to their Pydantic models
ENTITY_TYPES: dict[str, Type[BaseModel]] = {
    "Vocabulary": Vocabulary,
    "Definition": Definition,
    "GrammarRule": GrammarRule,
    "Mistake": Mistake,
    "Topic": Topic,
    "ExampleSentence": ExampleSentence,
    "Exercise": Exercise,
}

# Mapping of edge type names to their Pydantic models
EDGE_TYPES: dict[str, Type[BaseModel]] = {
    "MemoryTrace": MemoryTrace,
    "StrugglesWith": StrugglesWith,
    "HasDefinition": HasDefinition,
    "IsFormOf": IsFormOf,
    "TranslationOf": TranslationOf,
    "BelongsTo": BelongsTo,
    "Illustrates": Illustrates,
    "Tests": Tests,
}

# Constraints: Which source nodes can connect to which target nodes, and how
# Format: (source_type, target_type) -> [allowed_edge_types]
# Note: "User" is a string because it's managed manually, not via extraction
EDGE_TYPE_MAP: dict[tuple[str, str], list[str]] = {
    # User learning profile
    ("User", "Vocabulary"): ["MemoryTrace"],
    ("User", "GrammarRule"): ["MemoryTrace"],
    ("User", "Mistake"): ["StrugglesWith"],
    
    # Semantic structure
    ("Vocabulary", "Definition"): ["HasDefinition"],
    ("Vocabulary", "Topic"): ["BelongsTo"],
    ("Definition", "Definition"): ["TranslationOf"],
    ("GrammarRule", "Topic"): ["BelongsTo"],
    
    # Morphology
    ("Vocabulary", "Vocabulary"): ["IsFormOf"],
    
    # Pedagogy
    ("ExampleSentence", "Vocabulary"): ["Illustrates"],
    ("ExampleSentence", "GrammarRule"): ["Illustrates"],
    ("Exercise", "Vocabulary"): ["Tests"],
    ("Exercise", "GrammarRule"): ["Tests"],
    
    # Error tracking
    ("Mistake", "GrammarRule"): ["BelongsTo"],  # Link error to violated rule
}
