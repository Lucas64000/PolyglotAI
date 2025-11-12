"""
Models Complets POC - Version Finale
Basé sur tes models avec corrections et ajouts
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    """Retourne la date/heure UTC actuelle."""
    return datetime.now(timezone.utc)

from src.core.enums import (
    CECRLevel,
    Language,
    Role,
    ConversationStatus,
)

class User(BaseModel):
    """
    Utilisateur de l'application
    """
    id: UUID = Field(default_factory=uuid4)
    name: str
    
    # Langues
    native_language: Language
    target_language: Language
    
    # Niveau
    current_level: CECRLevel  
    initial_level: Optional[CECRLevel] = None  
    
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
    id: UUID = Field(default_factory=uuid4)
    conversation_id: UUID
    user_id: UUID
    content: str
    role: Role
    
class Correction(BaseModel):
    """
    Une correction appliquée à un message
    """
    id: UUID = Field(default_factory=uuid4)
    message_id: UUID
    
    # Texte
    original: str
    corrected: str
    
    # Position dans le message original
    start_index: int
    end_index: int
 