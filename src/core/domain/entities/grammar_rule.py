"""
GrammarRule Entity

Represents a linguistic rule or grammatical concept.
Used for teaching and linking errors to explanations.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from ..value_objects import CEFRLevel, Language


@dataclass
class GrammarRule:
    """
    Represents a grammar rule or linguistic concept.
    
    Grammar rules are pedagogical units that:
    - Explain how the language works
    - Can be linked to user errors (Mistake -> GrammarRule)
    - Have a difficulty level (CEFR)
    - Belong to topics for organization
    
    Corresponds to the GrammarRule node in the graph ontology.
    
    Attributes:
        id: Unique identifier
        rule_name: Standard academic name (e.g., "Present Perfect")
        explanation: Pedagogical explanation
        language: Language this rule applies to
        cefr_level: Difficulty level (A1-C2)
        topic: High-level topic (e.g., "Verbs", "Articles")
        examples: Example sentences illustrating the rule
    
    Examples:
        >>> from polyglot_ai.core.domain.value_objects import Language, CEFRLevel
        >>> rule = GrammarRule(
        ...     rule_name="Present Perfect",
        ...     explanation="Used for actions that started in the past and continue to the present, or for past actions with present relevance.",
        ...     language=Language.english(),
        ...     cefr_level=CEFRLevel.B1,
        ...     topic="Verb Tenses"
        ... )
    """
    
    rule_name: str
    explanation: str
    language: Language
    id: UUID = field(default_factory=uuid4)
    cefr_level: CEFRLevel | None = None
    topic: str | None = None
    examples: list[str] = field(default_factory=list[str])
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def __post_init__(self) -> None:
        """Validate the grammar rule."""
        if not self.rule_name or not self.rule_name.strip():
            raise ValueError("Rule name cannot be empty")
        if not self.explanation or not self.explanation.strip():
            raise ValueError("Explanation cannot be empty")
        
        self.rule_name = self.rule_name.strip()
        self.explanation = self.explanation.strip()
    
    def add_example(self, example: str) -> None:
        """
        Add an example sentence for this rule.
        
        Args:
            example: A sentence illustrating the rule
        """
        if example and example.strip():
            self.examples.append(example.strip())
    
    @property
    def is_beginner_level(self) -> bool:
        """Check if this rule is beginner-appropriate."""
        return self.cefr_level is not None and self.cefr_level.is_beginner
    
    @property
    def is_advanced_level(self) -> bool:
        """Check if this is an advanced rule."""
        return self.cefr_level is not None and self.cefr_level.is_advanced
    
    def __eq__(self, other: object) -> bool:
        """Two rules are equal if they have the same ID."""
        if not isinstance(other, GrammarRule):
            return NotImplemented
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash based on ID."""
        return hash(self.id)
    
    def __repr__(self) -> str:
        level = self.cefr_level.value if self.cefr_level else "?"
        return f"GrammarRule({self.rule_name!r}, level={level})"
