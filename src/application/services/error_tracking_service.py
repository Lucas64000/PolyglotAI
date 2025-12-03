"""
ErrorTrackingService

Service for tracking and analyzing user errors.
"""

from uuid import UUID

from src.core.ports.driven import GraphMemory
from src.core.domain.entities import UserError
from src.core.domain.value_objects import ErrorType, Language


class ErrorTrackingService:
    """
    Service for error tracking and analysis.
    
    Tracks user mistakes and provides insights for targeted practice.
    """
    
    def __init__(self, graph_memory: GraphMemory) -> None:
        """
        Initialize with injected dependencies.
        
        Args:
            graph_memory: For storing/retrieving errors
        """
        self._graph_memory = graph_memory
    
    async def record_error(
        self,
        user_id: UUID,
        wrong_form: str,
        correction: str,
        error_type: ErrorType,
        language: Language,
        explanation: str | None = None,
        related_rule: str | None = None,
    ) -> UserError:
        """
        Record a new error or increment existing error count.
        """
        from src.core.domain.entities import UserError
        
        # Check if this exact error exists
        existing_errors = await self._graph_memory.get_recurring_errors(user_id, limit=100)
        
        for error in existing_errors:
            if error.wrong_form.lower() == wrong_form.lower():
                # Increment existing
                await self._graph_memory.increment_error_count(user_id, wrong_form)
                error.record_occurrence()
                return error
        
        # Create new error
        error = UserError(
            user_id=user_id,
            wrong_form=wrong_form,
            correction=correction,
            error_type=error_type,
            language=language,
            explanation=explanation,
            related_rule=related_rule,
        )
        
        await self._graph_memory.store_error(user_id, error)
        return error
    
    async def get_recurring_errors(
        self,
        user_id: UUID,
        limit: int = 10,
    ) -> list[UserError]:
        """Get the user's most frequent errors."""
        return await self._graph_memory.get_recurring_errors(user_id, limit)
    
    async def get_errors_by_type(
        self,
        user_id: UUID,
        error_type: ErrorType,
    ) -> list[UserError]:
        """Get errors filtered by type."""
        all_errors = await self._graph_memory.get_recurring_errors(user_id, limit=100)
        return [e for e in all_errors if e.error_type == error_type]
    
    async def get_chronic_errors(
        self,
        user_id: UUID,
    ) -> list[UserError]:
        """Get errors that occur very frequently (5+ times)."""
        all_errors = await self._graph_memory.get_recurring_errors(user_id, limit=100)
        return [e for e in all_errors if e.is_chronic]
