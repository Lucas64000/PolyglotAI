"""
Modèles liés à l'utilisateur
"""

from uuid import UUID, uuid4
from datetime import datetime

from pydantic import BaseModel, Field

from src.core.enums import (
    CECRLevel,
    Language,
) 

from src.utils.utils import utc_now

class User(BaseModel):
    """
    Utilisateur de l'application
    """
    id: UUID = Field(default_factory=uuid4)
    name: str
    
    native_language: Language
    target_language: Language
    
    current_level: CECRLevel
    initial_level: CECRLevel | None = None
    
    created_at: datetime = Field(default_factory=utc_now)