"""
Student Summary Read Model

Lightweight representation of a student for listing and querying operations.
Avoids loading full Student entities for performance.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.core.domain.value_objects import Language, CEFRLevel


@dataclass(frozen=True, slots=True)
class StudentSummary:
    """
    Summary of student information for read operations.
    
    Contains essential student data without heavy relationships or methods.
    Used in StudentReader for efficient querying.
    
    Attributes:
        id: Unique student identifier
        native_lang: Student's native language
        target_lang: Language the student is learning
        level: Current proficiency level
        created_at: When the student account was created
    """
    id: UUID
    native_lang: Language
    target_lang: Language
    level: CEFRLevel
    created_at: datetime
