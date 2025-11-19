
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Generic

from src.models.conversation_model import Message
from src.clients.client_interface import ClientWrapper
from src.adapters.llm_adapter.adapter_interface import MessageAdapter

from src.core.types import TMessage, TResponse


class BaseLLMProvider(Generic[TMessage, TResponse], ABC):
    """
    Classe abstraite pour tous les providers LLM
    """

    def __init__(
            self, 
            model_name: str, 
            temperature: float,
            max_tokens: int,
            client: ClientWrapper[TMessage, TResponse],
            adapter: MessageAdapter[TMessage, TResponse]
        ) -> None:
        """
        Initialise les paramètres communs à tous les providers
        
        Args:
            model_name: Nom du modèle/deployment
            temperature: Température de génération
            max_tokens: Nombre maximum de tokens
            client: Client wrapper configuré
            adapter: Adaptateur de messages
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = client
        self.adapter = adapter

    @abstractmethod
    def generate(self, messages: List[Message]) -> Message:
        pass
    
    @abstractmethod
    def generate_json(self, messages: List[Message]) -> Dict[str, Any]:
        pass

    # @abstractmethod
    # def generate_tool_calls(self, messages: List[Message], tools: List[Dict[str, Any]], temperature: float = 0.0) -> Any:
    #     pass