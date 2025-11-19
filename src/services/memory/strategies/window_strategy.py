
from src.models.conversation_model import Message
from src.services.memory.repositories.repository_interface import BaseMemoryRepository
from .strategy_interface import BaseMemoryStrategy
from uuid import UUID
from typing import List

class WindowMemoryStrategy(BaseMemoryStrategy):

    def __init__(self, repository: BaseMemoryRepository, window_size: int = 5) -> None:
        super().__init__(repository)
        self.window_size = window_size

    def get_context(self, cid: UUID) -> List[Message]:
        all_messages = self.repository.get_messages(cid)

        return all_messages[-self.window_size:]

    def save_message(self, message: Message) -> None:
        self.repository.add_message(message)