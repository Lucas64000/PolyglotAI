
from typing import List
from openai import AzureOpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletion
from .client_interface import ClientWrapper
from .config.azure_config import AzureClientConfig

class AzureClientWrapper(ClientWrapper[ChatCompletionMessageParam, ChatCompletion]):
    """Wrapper pour Azure OpenAI."""
    
    def __init__(self, config: AzureClientConfig):
        self.config = config
        self.client = AzureOpenAI(**config.to_sdk_kwargs())

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
