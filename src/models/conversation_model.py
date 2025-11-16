"""
Modèles liés aux conversations
"""

from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import Dict, Any

from src.core.enums import (
    Role,
    ConversationStatus,
) 
    
class Conversation(BaseModel):
    """
    Une session de conversation
    """
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID

    title: str = "New Conversation"  
    status: ConversationStatus = ConversationStatus.ACTIVE


class Message(BaseModel):
    """
    Un message dans une conversation
    """
    role: Role
    content: str
    metadata: Dict[str, Any] = {}


class Correction(BaseModel):
    """
    Une correction appliquée à un message
    """
    id: UUID = Field(default_factory=uuid4)
    message_id: UUID
    
    original: str
    corrected: str
    
    start_index: int
    end_index: int


class Tool(BaseModel):
    """
    Le tool utilisé par l'agent pour fournir la réponse
    """
    type: str
    name: str
    description: str
    parameters: Dict[str, Any]