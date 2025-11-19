
from abc import ABC, abstractmethod
from ..repositories.repository_interface import BaseMemoryRepository
from src.models.conversation_model import Message
from typing import List
from uuid import UUID

class BaseMemoryStrategy(ABC):
    
    def __init__(self, repository: BaseMemoryRepository) -> None:
        self.repository=repository

    @abstractmethod
    def get_context(self, cid: UUID) -> List[Message]:
        pass

    @abstractmethod
    def save_message(self, message: Message) -> None:
        pass