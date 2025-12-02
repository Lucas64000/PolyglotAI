"""
Role Value Object

Represents the role of a participant in a chat conversation.
"""

from enum import Enum


class Role(str, Enum):
    """
    Represents the role of a message sender in a conversation.
    
    Roles:
        SYSTEM: System instructions/prompts (invisible to user)
        USER: Messages from the learner
        ASSISTANT: Messages from the AI tutor
    
    The string values match OpenAI/Azure API expectations for seamless integration.
    """
    
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    
    def is_human(self) -> bool:
        """Check if this role represents a human participant."""
        return self == Role.USER
    
    def is_ai(self) -> bool:
        """Check if this role represents the AI assistant."""
        return self == Role.ASSISTANT
    
    def is_system(self) -> bool:
        """Check if this is a system message."""
        return self == Role.SYSTEM
