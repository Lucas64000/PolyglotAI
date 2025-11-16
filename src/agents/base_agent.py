from abc import ABC, abstractmethod
from typing import Any, List

from src.models.conversation_model import Message
from src.models.user_model import User
from src.models.conversation_model import Message

from src.services.providers.provider_llm import ProviderLLM
from src.services.memory.memory_service import MemoryService


class BaseAgent(ABC):
    """Classe abstraite des agents"""
    def __init__(self, llm: ProviderLLM, memory: MemoryService):
        self.llm = llm
        self.memory = memory

    # Type de retour à revoir plus tard
    @abstractmethod
    def run(self, user: User, message: Message) -> Any:
        """
        Fonction principale executant le rôle de l'agent
        
        Args: 
            user: Informations de l'utilisateur
            message: Message de l'utilisateur

        Returns:
            A redéfinir plus tard
        """
        pass

    @abstractmethod
    def _build_prompt(self, user: User) -> Message:
        pass

    def format_messages(self, user: User, message: Message) -> List[Message]:
        """
        Créé la conversation avec SYSTEM_PROMPT + HISTORIQUE + INPUT_USER

        Args:
            user: Informations de l'utilisateur
            message: Message de l'utilisateur
        
        Returns:
            La conversation formatée pour l'agent
        """
        system_prompt = self._build_prompt(user)
        historic_messages = self.memory.historic
        
        messages = [system_prompt]
        messages.extend(historic_messages)
        messages.append(message)

        return messages

