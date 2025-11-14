from typing import List, Dict, Any
from src.utils.config import get_config
from openai import AzureOpenAI

class AzureFoundryLLM:
    def __init__(self, api_version: str | None = None, api_key: str | None = None, 
                 model: str | None = None, max_tokens: int | None = None):
        config = get_config()
        self.api_version = api_version if api_version else config.api_version
        self.endpoint = str(config.azure_endpoint)
        self.api_key = api_key if api_key else config.azure_api_key
        self.model = model if model else config.llm_model
        self.max_tokens = max_tokens if max_tokens else config.llm_max_tokens

        self.client = AzureOpenAI(
            api_version=self.api_version,
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
        )

    def generate(self, messages: List[Dict[str, str]], system_prompt: str="You are helpful", temperature: float = 0.7) -> str:
        system_message = [{"role": "system", "content": system_prompt}]
        all_messages: Any = system_message + messages

        response: Any = self.client.chat.completions.create(
            messages=all_messages,
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=temperature,
            )

        return response.choices[0].message.content

    def generate_json(self, messages: List[Dict[str, str]], system_prompt: str="You are helpful", temperature: float = 0.7) -> Dict[str, str]:
        system_message = [{"role": "system",
                       "content": f"{system_prompt}. Please respond strictly in JSON format."}]
        all_messages: Any = system_message + messages

        response: Any = self.client.chat.completions.create(
            messages=all_messages,
            max_tokens=self.max_tokens,
            temperature=temperature,
            model=self.model,
            response_format={"type": "json_object"},
            )

        return response.choices[0].message.content
    
    def generate_tool_call(self, messages: List[Dict[str, str]], tools: List[Dict[str, Any]], 
                           system_prompt: str = "You are a routing agent.", temperature: float = 0.7) -> Any:
        """Génère une réponse en utilisant la fonctionnalité Function/Tool Calling."""
        
        system_message = [{"role": "system", "content": system_prompt}]
        all_messages: Any = system_message + messages

        response: Any = self.client.chat.completions.create(
            messages=all_messages,
            max_tokens=self.max_tokens,
            temperature=temperature,
            model=self.model,
            tools=tools,
            tool_choice="auto",
        )
        return response.choices[0].message.tool_calls