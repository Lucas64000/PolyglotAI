
from src.infrastructure.adapters.driven import LLMTeacherAdapter
from src.infrastructure.ai import OllamaClient
from src.infrastructure.ai.config import OllamaConfig

class TestOllama:

    async def test_ollama_config(self) -> None:
        config = OllamaConfig()

        ollama_client = OllamaClient(
            base_url=config.openai_compatible_url,
            model_name=config.model
        )

        teacher = LLMTeacherAdapter(client=ollama_client)

        assert isinstance(teacher, LLMTeacherAdapter)

    async def test_should_configure_ollama_client_correctly(self) -> None:
        config = OllamaConfig()
        
        ollama_client = OllamaClient(
            base_url=config.openai_compatible_url,
            model_name=config.model
        )
        
        assert str(ollama_client.client.base_url) == f"{config.base_url}/v1/" 