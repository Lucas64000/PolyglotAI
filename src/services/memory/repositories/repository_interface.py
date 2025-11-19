
from abc import ABC, abstractmethod

from typing import List
from src.models.conversation_model import Conversation, Message

from uuid import UUID

class BaseMemoryRepository(ABC):
    """Interface pour le stockage des conversations"""

    @abstractmethod
    def create_conversation(self, user_id: UUID) -> Conversation:
        pass

    @abstractmethod
    def get_all_conversations(self, user_id: UUID) -> List[Conversation]:
        pass

    @abstractmethod
    def get_conversation_by_id(self, conversation_id: UUID) -> Conversation | None:
        pass

    @abstractmethod
    def update_conversation_metadata(self, updated_conversation: Conversation) -> None:
        pass

    @abstractmethod
    def delete_conversation(self, conversation_id: UUID) -> None:
        pass

    @abstractmethod
    def add_message(self, message: Message) -> None:
        pass

    @abstractmethod
    def get_messages(self, conversation_id: UUID) -> List[Message]:
        pass

    @abstractmethod
    def update_message(self, new_message: Message) -> None:
        pass