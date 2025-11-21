"""
Modèles liés aux conversations
"""

from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime

from src.core.enums import (
    Role,
    ConversationStatus,
) 

from src.utils.utils import utc_now

class Message(BaseModel):
    """
    Un message dans une conversation
    """
    id: UUID = Field(default_factory=uuid4) 
    conversation_id: UUID
    role: Role
    content: str
    
    created_at: datetime = Field(default_factory=utc_now)
    
    metadata: Dict[str, Any] = {}

    def __str__(self) -> str:
        """Représentation simple du message."""
        return f"[{self.role.value}] {self.content}"


class Conversation(BaseModel):
    """
    Une session de conversation
    """
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID

    title: str = "Nouvelle Conversation"
    status: ConversationStatus = ConversationStatus.ACTIVE

    summary: str = ""
    
    created_at: datetime = Field(default_factory=utc_now)
