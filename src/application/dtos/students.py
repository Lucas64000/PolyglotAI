"""
Student DTOs

All student-related Data Transfer Objects .
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

# ──────────────────────────────────────────────────────────────────────────
# READ MODELS (Query Operations)
# ──────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True, slots=True)
class StudentSummary:
    """
    Read model for student information.
    
    Lightweight summary containing essential student data without heavy relationships.
    Used for efficient querying and display without loading full Student entities.
    
    Attributes:
        id: Unique student identifier
        native_lang: Student's native language
        target_lang: Language the student is learning
        level: Current proficiency level (CEFR)
        created_at: When the student account was created
    """
    id: UUID
    native_lang: str
    target_lang: str
    level: str
    created_at: datetime
