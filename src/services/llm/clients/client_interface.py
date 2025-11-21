
from abc import ABC, abstractmethod
from typing import List, Generic
from src.core.types import TMessage, TResponse

class ClientWrapper(Generic[TMessage, TResponse], ABC):
    """
    Interface générique pour les Client LLM.
    
    Type Parameters:
        TMessage: Type du format de message attendu par le SDK du service
                  (ex: ChatCompletionMessageParam pour OpenAI)
        TResponse: Type de la réponse retournée par le SDK du service
                   (ex: ChatCompletion pour OpenAI)

    Le service encapsule le client pour éviter toute dépendance
    """

    @abstractmethod
    def generate(self, messages: List[TMessage], model_name: str, max_tokens: int, temperature: float) -> TResponse:
        """
        Génère une réponse LLM.

        Args:
            messages (List[TMessage]): Messages déjà convertis par l'adapter
            model_name (str): nom du modèle 
            max_tokens (int): nombre max de tokens
            temperature (float): température du modèle

        Returns:
            TResponse: réponse brute du SDK
        """
        pass

    @abstractmethod
    def generate_json(self, messages: List[TMessage], model_name: str, max_tokens: int, temperature: float) -> TResponse:
        """
        Génère une réponse LLM au format JSON.

        Args:
            messages (List[TMessage]): Messages déjà convertis par l'adapter
            model_name (str): nom du modèle 
            max_tokens (int): nombre max de tokens
            temperature (float): température du modèle

        Returns:
            TResponse: réponse brute du SDK avec format JSON
        """
        pass
