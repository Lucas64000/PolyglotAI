"""
GetLearningContext Use Case

Retrieves relevant context for a conversation from the knowledge graph.
"""

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from src.core.ports.driven import GraphMemory
from src.core.domain.entities import GrammarRule, UserError, VocabularyItem


@dataclass
class GetLearningContextInput:
    """Input for getting learning context."""
    user_id: UUID
    current_message: str
    max_vocabulary: int = 5
    max_errors: int = 3
    max_rules: int = 3


@dataclass
class GetLearningContextOutput:
    """Structured learning context."""
    relevant_vocabulary: list[VocabularyItem]
    recent_errors: list[UserError]
    relevant_rules: list[GrammarRule]
    raw_context: dict[str, Any]


class GetLearningContextUseCase:
    """
    Use case for retrieving learning context.
    
    Uses semantic search to find relevant:
    - Vocabulary the user has learned
    - Errors the user commonly makes
    - Grammar rules that might be relevant
    """
    
    def __init__(self, graph_memory: GraphMemory) -> None:
        self._graph_memory = graph_memory
    
    async def execute(
        self, input_data: GetLearningContextInput
    ) -> GetLearningContextOutput:
        """Execute the use case."""
        # Get raw context from graph
        raw_context = await self._graph_memory.get_learning_context(
            user_id=input_data.user_id,
            current_message=input_data.current_message,
            limit=max(
                input_data.max_vocabulary,
                input_data.max_errors,
                input_data.max_rules,
            ),
        )
        
        # Extract and limit results
        vocabulary = raw_context.get("vocabulary", [])[:input_data.max_vocabulary]
        errors = raw_context.get("errors", [])[:input_data.max_errors]
        rules = raw_context.get("rules", [])[:input_data.max_rules]
        
        return GetLearningContextOutput(
            relevant_vocabulary=vocabulary,
            recent_errors=errors,
            relevant_rules=rules,
            raw_context=raw_context,
        )
