"""
Role Value Object

Represents the role of a participant in a chat conversation.
"""

from enum import Enum

class Role(Enum):
    """
    Represents the role of a message sender in a conversation.
    
    Roles:
        STUDENT: Messages from the student
        TEACHER: Messages from the teacher
    """
    
    STUDENT = "student"
    TEACHER = "teacher"
    
    @property
    def is_student(self) -> bool:
        """Check if this role represents the student."""
        return self == Role.STUDENT
    
    @property
    def is_teacher(self) -> bool:
        """Check if this role represents the teacher."""
        return self == Role.TEACHER
