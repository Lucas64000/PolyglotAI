
from openai import OpenAI
from .openai_wrapper import OpenAIClientWrapper
from .config.ollama_config import OllamaClientConfig

class OllamaClientWrapper(OpenAIClientWrapper):
    """Wrapper pour Ollama OpenAI."""
    
    def __init__(self, config: OllamaClientConfig):
        self.config = config
        self.client = OpenAI(**config.to_sdk_kwargs())

