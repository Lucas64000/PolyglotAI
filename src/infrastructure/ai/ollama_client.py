
from openai import AsyncOpenAI
from .base_openai_client import BaseOpenAIClient

class OllamaClient(BaseOpenAIClient):

    def __init__(self, base_url: str, model_name: str):
        self.base_url = base_url
        super().__init__(model_name)

    def _create_client(self) -> AsyncOpenAI:
        return AsyncOpenAI(
            base_url=self.base_url,
            api_key="ollama"
        )
