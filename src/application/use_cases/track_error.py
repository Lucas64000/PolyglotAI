"""
TrackError Use Case

Handles recording and tracking user errors.
"""


from dataclasses import dataclass
from uuid import UUID

from src.core.ports.driven import GraphMemory
from src.core.domain.entities import UserError
from src.core.domain.value_objects import ErrorType, Language


@dataclass
class TrackErrorInput:
    """Input for tracking an error."""
    user_id: UUID
    wrong_form: str
    correction: str
    error_type: ErrorType
    language: Language
    explanation: str | None = None
    related_rule: str | None = None


@dataclass
class TrackErrorOutput:
    """Output from tracking an error."""
    error: UserError
    is_recurring: bool
    occurrence_count: int


class TrackErrorUseCase:
    """
    Use case for tracking a user error.
    
    Determines if this is a new error or a recurring one,
    and updates the graph accordingly.
    """
    
    def __init__(self, graph_memory: GraphMemory) -> None:
        self._graph_memory = graph_memory
    
    async def execute(self, input_data: TrackErrorInput) -> TrackErrorOutput:
        """Execute the use case."""
        from src.core.domain.entities import UserError
        
        # Check for existing error with same wrong_form
        existing_errors = await self._graph_memory.get_recurring_errors(
            input_data.user_id, limit=100
        )
        
        for existing in existing_errors:
            if existing.wrong_form.lower() == input_data.wrong_form.lower():
                # Increment existing error
                await self._graph_memory.increment_error_count(
                    input_data.user_id, 
                    input_data.wrong_form
                )
                existing.record_occurrence()
                
                return TrackErrorOutput(
                    error=existing,
                    is_recurring=True,
                    occurrence_count=existing.occurrence_count,
                )
        
        # Create new error
        error = UserError(
            user_id=input_data.user_id,
            wrong_form=input_data.wrong_form,
            correction=input_data.correction,
            error_type=input_data.error_type,
            language=input_data.language,
            explanation=input_data.explanation,
            related_rule=input_data.related_rule,
        )
        
        await self._graph_memory.store_error(input_data.user_id, error)
        
        return TrackErrorOutput(
            error=error,
            is_recurring=False,
            occurrence_count=1,
        )
