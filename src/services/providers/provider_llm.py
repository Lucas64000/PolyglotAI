"""
Abstraction du service des LLMs 
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

from src.models.conversation_model import Message

class ProviderLLM(ABC):
    def __init__(
            self, 
            model_name: str, 
            max_tokens: int,
            temperature: float,
        ) -> None:
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature

    @abstractmethod
    def generate(self, messages: List[Message]) -> Message:
        pass
    
    @abstractmethod
    def generate_json(self, messages: List[Message]) -> Dict[str, Any]:
        pass

    # @abstractmethod
    # def generate_tool_calls(self, messages: List[Message], tools: List[Dict[str, Any]], temperature: float = 0.0) -> Any:
    #     pass