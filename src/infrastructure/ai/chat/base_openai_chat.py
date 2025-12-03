"""
Base OpenAI Chat Model

Shared implementation for OpenAI-compatible chat models (Azure, OpenAI, Ollama, Grok, etc.).
"""

import json
from abc import ABC, abstractmethod
from typing import Any, cast

from openai import AsyncOpenAI, AsyncAzureOpenAI
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
)
from src.core.domain.entities import ChatMessage
from src.core.exceptions.ai_exceptions import LLMError, LLMResponseError, LLMJSONDecodeError


class BaseOpenAIChatModel(ABC):
    """
    Base class for OpenAI-compatible chat models.
    
    Provides shared implementation for:
    - Message conversion
    - API calls
    - Response parsing
    
    Subclasses must implement _create_client() 
    to provide the appropriate client.
    """
    
    def __init__(
        self,
        model_name: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> None:
        """
        Initialize common parameters.
        
        Args:
            model_name: Model or deployment name
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum response tokens
        """
        self._model_name = model_name
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._client: AsyncOpenAI | AsyncAzureOpenAI | None = None
    
    @property
    def model_name(self) -> str:
        """Get the model name."""
        return self._model_name
    
    @abstractmethod
    def _create_client(self) -> AsyncOpenAI | AsyncAzureOpenAI:
        """
        Create the appropriate async client.
        
        Must be implemented by subclasses.
        """
        ...
    
    @property
    def client(self) -> AsyncOpenAI | AsyncAzureOpenAI:
        """Get or create the client (lazy initialization)."""
        if self._client is None:
            self._client = self._create_client()
        return self._client
    
    def _convert_messages(
        self, messages: list[ChatMessage]
    ) -> list[ChatCompletionMessageParam]:
        """
        Convert domain messages to OpenAI SDK format.
        
        Args:
            messages: List of ChatMessage entities
            
        Returns:
            List of ChatCompletionMessageParam for OpenAI SDK
        """
        sdk_messages: list[ChatCompletionMessageParam] = []
        for msg in messages:
            role = msg.role.value
            content = msg.content
            
            if role == "system":
                sdk_messages.append(ChatCompletionSystemMessageParam(role="system", content=content))
            elif role == "user":
                sdk_messages.append(ChatCompletionUserMessageParam(role="user", content=content))
            elif role == "assistant":
                sdk_messages.append(ChatCompletionAssistantMessageParam(role="assistant", content=content))
            else:
                # Fallback: cast to user message for unknown roles
                sdk_messages.append(ChatCompletionUserMessageParam(role="user", content=content))
        
        return sdk_messages
    
    async def _generate_raw(
        self, 
        messages: list[ChatMessage], 
        **kwargs: Any
    ) -> ChatCompletion:
        """
        Internal method to generate raw API response.
        
        Args:
            messages: Conversation history
            **kwargs: Additional parameters for the API call
            
        Returns:
            Raw ChatCompletion response from OpenAI SDK
            
        Raises:
            LLMError: If API call fails
        """
        sdk_messages = self._convert_messages(messages)
        
        try:
            response = cast(ChatCompletion, await self.client.chat.completions.create(
                model=self._model_name,
                messages=sdk_messages,
                temperature=self._temperature,
                max_tokens=self._max_tokens,
                **kwargs
            ))
        except Exception as e:
            raise LLMError("openai", f"API call failed: {e}", e) from e
        
        return response
    
    async def generate(self, messages: list[ChatMessage]) -> str:
        """
        Generate a text response.
        
        Args:
            messages: Conversation history
            
        Returns:
            Generated text
            
        Raises:
            LLMResponseError: If response is empty
        """
        response = await self._generate_raw(messages)
        
        if not response.choices or not response.choices[0].message.content:
            raise LLMResponseError("openai", "Empty response from LLM")
        
        return response.choices[0].message.content
    
    async def generate_json(self, messages: list[ChatMessage]) -> dict[str, Any]:
        """
        Generate a JSON response.
        
        Args:
            messages: Conversation history
            
        Returns:
            Parsed JSON as dictionary
            
        Raises:
            LLMResponseError: If response is empty
            LLMJSONDecodeError: If response is not valid JSON
        """
        response = await self._generate_raw(messages, response_format={"type": "json_object"})
        
        if not response.choices or not response.choices[0].message.content:
            raise LLMResponseError("openai", "Empty response from LLM")
        
        content = response.choices[0].message.content
        
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise LLMJSONDecodeError("openai", f"Invalid JSON: {e}", content) from e
    
    async def generate_with_metadata(
        self, messages: list[ChatMessage]
    ) -> tuple[str, dict[str, Any]]:
        """
        Generate response with metadata.
        
        Args:
            messages: Conversation history
            
        Returns:
            Tuple of (response_text, metadata)

        Raises:
            LLMResponseError: If response is empty
        """
        response = await self._generate_raw(messages)
        
        if not response.choices or not response.choices[0].message.content:
            raise LLMResponseError("openai", "Empty response from LLM")
        
        content = response.choices[0].message.content
        
        metadata: dict[str, Any] = {
            "id": response.id,
            "model": response.model,
            "finish_reason": response.choices[0].finish_reason,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                "total_tokens": response.usage.total_tokens if response.usage else 0,
            } if response.usage else None,
        }
        
        return content, metadata
