"""
Error Mapper

Converts between UserError entities and graph nodes.
"""

from typing import Any

from src.core.domain.entities import UserError
from src.infrastructure.graph.ontology import Mistake
from src.infrastructure.graph.ontology import StrugglesWith

class ErrorMapper:
    """
    Maps between UserError domain entity and graph nodes.
    
    A UserError maps to:
    - One Mistake node
    - One StrugglesWith edge (User -> Mistake)
    - Optionally one BelongsTo edge (Mistake -> GrammarRule)
    """
    
    @staticmethod
    def to_graph_node(error: UserError) -> Mistake:
        """
        Convert UserError to Mistake node data.
        
        Returns:
            Dictionary of node properties
        """
        return Mistake(
            wrong_form=error.wrong_form,
            correction= error.correction,
            explanation= error.explanation,
        )
    
    @staticmethod
    def to_edge_data(error: UserError) -> StrugglesWith:
        """
        Convert UserError to StrugglesWith edge data.
        
        Returns:
            Dictionary of edge properties
        """
        return StrugglesWith(
            occurrence_count=error.occurrence_count,
        )
    
    @staticmethod
    def from_graph_nodes(
        mistake_data: dict[str, Any],
        struggles_with_data: dict[str, Any],
        user_id: str,
        language: str,
        error_type: str,
    ) -> UserError:
        """
        Convert graph node data to UserError.
        
        Args:
            mistake_data: Mistake node properties
            struggles_with_data: StrugglesWith edge properties
            user_id: User UUID string
            language: Language code
            error_type: Error type string
            
        Returns:
            UserError entity
        """
        from uuid import UUID
        from src.core.domain.entities import UserError
        from src.core.domain.value_objects import ErrorType, Language
        
        return UserError(
            user_id=UUID(user_id),
            wrong_form=mistake_data["wrong_form"],
            correction=mistake_data["correction"],
            error_type=ErrorType(error_type),
            language=Language(language),
            explanation=mistake_data.get("explanation"),
            occurrence_count=struggles_with_data.get("occurrence_count", 1),
        )
