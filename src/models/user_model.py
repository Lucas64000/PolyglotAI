"""
Modèles liés à l'utilisateur
"""

from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.agents.core.enums import (
    CECRLevel,
    Language,
) 

class User(BaseModel):
    """
    Utilisateur de l'application
    """
    id: UUID = Field(default_factory=uuid4)
    name: str
    
    native_language: Language
    target_language: Language
    
    current_level: CECRLevel  
    initial_level: Optional[CECRLevel] = None 