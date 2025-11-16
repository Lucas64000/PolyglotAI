
from typing import List
from src.models.conversation_model import Message

class MemoryService:

    def __init__(self) -> None:
        self.historic: List[Message] =  [] # Pour l'instant on save dans array, plus tard on fera dans bdd

    def save_message(self, message: Message) -> None:
        self.historic.append(message)