"""
Base OpenAI Client

Provides a base implementation for OpenAI-compatible chat models.

This abstract base class handles:
- Message format conversion from domain entities to OpenAI SDK format
- API call execution and response parsing
- Error handling: maps OpenAI-specific exceptions to domain exceptions
- Response validation

Subclasses must implement:
- _create_client(): Returns the appropriate AsyncOpenAI or AsyncAzureOpenAI client

Error Mapping Strategy:
    OpenAI exceptions are caught and converted to TeacherResponseError with domain-focused
    messages. This ensures the core domain layer remains pure and doesn't depend on
    infrastructure details.
"""
from abc import ABC, abstractmethod

from src.core.domain import ChatMessage, Role
from src.core.exceptions import TeacherResponseError

import openai
from openai import AsyncOpenAI, AsyncAzureOpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
)

class BaseOpenAIClient(ABC):
    """
    Base class for OpenAI-compatible chat models.
    
    Provides shared implementation for:
    - Message conversion
    - API calls
    - Response parsing
    
    Subclasses must implement _create_client() 
    to provide the appropriate client.
    """
    def __init__(self, model_name: str):
        
        self._model_name = model_name
        self._client: AsyncOpenAI | AsyncAzureOpenAI | None = None

    @property
    def model(self) -> str:
        """Get the model name."""
        return self._model_name

    @property
    def client(self) -> AsyncOpenAI | AsyncAzureOpenAI:
        """Get or create the client (lazy initialization)."""
        if self._client is None:
            self._client = self._create_client()
        return self._client

    @abstractmethod
    def _create_client(self) -> AsyncOpenAI | AsyncAzureOpenAI:
        """
        Create the appropriate async client.
        
        Must be implemented by subclasses.
        """
        ...

    def _convert_to_openai_format(
        self, 
        messages: tuple[ChatMessage, ...],
        system_prompt: str
    ) -> list[ChatCompletionMessageParam]:
        """
        Convert domain messages to OpenAI SDK format.
        
        Args:
            messages: List of ChatMessage entities
            system_prompt: 
            
        Returns:
            List of ChatCompletionMessageParam for OpenAI SDK
        """
        sdk_messages: list[ChatCompletionMessageParam] = []
        sdk_messages.append(ChatCompletionSystemMessageParam(role="system", content=system_prompt))

        for msg in messages:
            role = msg.role
            content = msg.content
            
            if role == Role.STUDENT:
                sdk_messages.append(ChatCompletionUserMessageParam(role="user", content=content))
            else:
                sdk_messages.append(ChatCompletionAssistantMessageParam(role="assistant", content=content))
            
        return sdk_messages

    async def generate(
            self, 
            messages: tuple[ChatMessage, ...],
            system_prompt: str = "You're an helpful assistant."
        ) -> str:
        """
        Generates a response using the LLM provider.
        """
        formatted_messages = self._convert_to_openai_format(messages, system_prompt)

        try:
            # API call
            response = await self.client.chat.completions.create(
                messages=formatted_messages, 
                model=self.model,
            )
        except openai.RateLimitError as e:
            raise TeacherResponseError(cause="The teacher is currently busy. Please try again later.") from e
        
        except openai.AuthenticationError as e:
            raise TeacherResponseError(cause="Teacher service configuration error (Auth).") from e
        
        except openai.PermissionDeniedError as e:
            raise TeacherResponseError(cause="Access denied to the learning service.") from e
        
        except openai.APIConnectionError as e:
            raise TeacherResponseError(cause="The teacher service is currently unavailable.") from e

        except openai.APIStatusError as e:
            raise TeacherResponseError(cause=f"Teacher service encountered an error ({e.status_code}).") from e
            
        except Exception as e:
            raise TeacherResponseError(cause=f"An unexpected error occurred.") from e
        
        try:
            content = response.choices[0].message.content
            if content is None or not content.strip():
                 raise TeacherResponseError(cause="The teacher service returned an empty response.")
            return content.strip()
            
        except (AttributeError, IndexError) as e:
            raise TeacherResponseError(cause="Invalid response format from teacher service.") from e