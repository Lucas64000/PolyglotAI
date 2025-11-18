
from abc import ABC, abstractmethod

from typing import List, Generic
from src.core.types import TMessage, TResponse
from src.models.conversation_model import Message


class MessageAdapter(Generic[TMessage, TResponse], ABC):
    """
    Interface générique pour les adaptateurs de messages LLM.
    
    Types génériques pour garantir la sécurité de type lors de la conversion entre les Messages métier et le SDK.
    
    Type Parameters:
        TMessage: Type du format de message attendu par le SDK du service
                  (ex: ChatCompletionMessageParam pour OpenAI)
        TResponse: Type de la réponse retournée par le SDK du service
                   (ex: ChatCompletion pour OpenAI)
    """
    
    @abstractmethod
    def to_sdk_format(self, messages: List[Message]) -> List[TMessage]:
        """
        Convertit des Messages métier en format compatible SDK

        Args:
            messages (List[Message]): Liste de Messages métier

        Returns:
            List[TMessage]: Messages convertis au format SDK
        """
        pass

    @abstractmethod
    def from_sdk_response(self, response: TResponse) -> Message:
        """
        Convertit une réponse du SDK en Message métier

        Args:
            response (TResponse): Réponse brute du SDK

        Returns:
            Message: Message métier
        """
        pass
