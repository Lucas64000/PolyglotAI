from typing import Protocol, Sequence

from src.core.domain import Language, CEFRLevel
from src.application.queries.read_models.student_summary import StudentSummary


class StudentReader(Protocol):
    """
    Port for student read operations.
    Separated from StudentRepository for CQRS-style architecture.
    """

    async def get_students_by_language_pair(
        self, 
        native_lang: Language, 
        target_lang: Language, 
        limit: int = 20, 
        offset: int = 0
    ) -> Sequence[StudentSummary]:
        """
        Get student summaries for students learning a specific language pair.
        
        Args:
            native_lang: Native language filter
            target_lang: Target language filter
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            Sequence of student summaries matching the criteria
        """
        ...

    async def get_students_by_level(
        self, 
        level: CEFRLevel, 
        limit: int = 20, 
        offset: int = 0
    ) -> Sequence[StudentSummary]:
        """
        Get student summaries for students at a specific proficiency level.
        
        Args:
            level: CEFR level filter
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            Sequence of student summaries at the specified level
        """
        ...

    async def get_all_students(self, limit: int = 100, offset: int = 0) -> Sequence[StudentSummary]:
        """
        Get a paginated list of all student summaries.
        
        Args:
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            Sequence of all student summaries (paginated)
        """
        ...
