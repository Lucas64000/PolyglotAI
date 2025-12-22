"""
Role Value Object

Represents the role of a participant in a chat conversation.
"""

from enum import Enum

class Role(str, Enum):
    """
    Represents the role of a message sender in a conversation.
    
    Roles:
        SYSTEM: System instructions/prompts 
        USER: Messages from the learner
        ASSISTANT: Messages from the AI tutor
    """
    
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    
    @property
    def is_human(self) -> bool:
        """Check if this role represents a human participant."""
        return self == Role.USER
    
    @property
    def is_ai(self) -> bool:
        """Check if this role represents the AI assistant."""
        return self == Role.ASSISTANT
    
    @property
    def is_system(self) -> bool:
        """Check if this is a system message."""
        return self == Role.SYSTEM
