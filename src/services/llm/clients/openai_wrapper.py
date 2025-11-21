
from abc import ABC, abstractmethod

from typing import List
from openai import OpenAI, AzureOpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletion
from .client_interface import ClientWrapper
from .config.config_interface import ClientConfig

class OpenAIClientWrapper(ClientWrapper[ChatCompletionMessageParam, ChatCompletion], ABC):
    """Wrapper pour les clients compatibles OpenAI (Azure, OpenAI, Ollama, Grok, etc.)."""
    
    client: OpenAI | AzureOpenAI

    @abstractmethod
    def __init__(self, config: ClientConfig):
        pass

    def generate(
        self, 
        messages: List[ChatCompletionMessageParam], 
        model_name: str, 
        max_tokens: int, 
        temperature: float
    ) -> ChatCompletion:
        return self.client.chat.completions.create(
            model=model_name,   
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )

    def generate_json(
        self, 
        messages: List[ChatCompletionMessageParam], 
        model_name: str, 
        max_tokens: int, 
        temperature: float
    ) -> ChatCompletion:
        return self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            response_format={"type": "json_object"}
        )
