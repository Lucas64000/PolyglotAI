
from openai import AzureOpenAI
from .openai_wrapper import OpenAIClientWrapper
from .config.azure_config import AzureClientConfig

class AzureClientWrapper(OpenAIClientWrapper):
    """Wrapper pour Azure OpenAI."""
    
    def __init__(self, config: AzureClientConfig):
        self.config = config
        self.client = AzureOpenAI(**config.to_sdk_kwargs())

