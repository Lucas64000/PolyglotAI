
from typing import Callable
import pytest
from unittest.mock import AsyncMock, MagicMock
import openai

from src.core.domain.entities import ChatMessage
from src.core.domain.value_objects import Role
from src.core.exceptions import TeacherResponseError

from src.infrastructure.ai import BaseOpenAIClient

class MockOpenAIClient(BaseOpenAIClient):
    """Testable implementation of BaseOpenAIClient for unit tests."""
    
    from openai import AsyncOpenAI, AsyncAzureOpenAI
    
    def __init__(self, model_name: str, client: AsyncOpenAI | AsyncAzureOpenAI):
        """Initialize with a mock client for testing."""
        super().__init__(model_name)
        self._test_client = client

    def _create_client(self) -> AsyncOpenAI | AsyncAzureOpenAI:
        """Return the injected mock client."""
        return self._test_client

@pytest.fixture
def openai_client_mock() -> AsyncMock:
    """Mock AsyncOpenAI client."""
    return AsyncMock()

@pytest.fixture
def base_openai_client(openai_client_mock: AsyncMock):
    """Fixture providing a MockOpenAIClient with mocked dependencies."""
    return MockOpenAIClient(
        model_name="gpt-test",
        client=openai_client_mock,
    )

class TestBaseOpenAIClientFormat:
    
    async def test_should_format_messages_for_openai(
        self, 
        base_openai_client: AsyncMock,
        openai_client_mock: AsyncMock,
        make_chat_message: Callable[..., ChatMessage]
    ) -> None:
        mock_message = MagicMock()
        mock_message.content = "Teacher response"

        mock_choice = MagicMock()
        mock_choice.message = mock_message

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        openai_client_mock.chat.completions.create.return_value = mock_response

        messages: list[ChatMessage] = [
            make_chat_message(role=Role.STUDENT, content="Student message"),
            make_chat_message(role=Role.TEACHER, content="Teacher message"),
            make_chat_message(role=Role.STUDENT, content="Student question"),
        ]
        system_prompt = "You're a useful teacher."

        _ = await base_openai_client.generate(messages=messages, system_prompt=system_prompt)

        openai_client_mock.chat.completions.create.assert_called_once()
        kwargs = openai_client_mock.chat.completions.create.call_args.kwargs

        assert kwargs["model"] == "gpt-test"
        
        formatted_messages = kwargs["messages"]

        assert formatted_messages[0]["role"] == "system"
        assert formatted_messages[0]["content"] == system_prompt

        assert formatted_messages[1]["role"] == "user"
        assert formatted_messages[1]["content"] == "Student message"

        assert formatted_messages[2]["role"] == "assistant"
        assert formatted_messages[2]["content"] == "Teacher message"

        assert formatted_messages[-1]["role"] == "user"
        assert formatted_messages[-1]["content"] == "Student question"

    @pytest.mark.parametrize("invalid_content", [
        None,           
        "",             
        "   ",          
        "\n\t",         
    ])
    async def test_should_raise_on_invalid_content(
        self,
        base_openai_client: AsyncMock,
        openai_client_mock: AsyncMock,
        make_chat_message: Callable[..., ChatMessage],
        invalid_content: str | None
    ) -> None:
        mock_message = MagicMock()
        mock_message.content = invalid_content

        mock_choice = MagicMock()
        mock_choice.message = mock_message

        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        openai_client_mock.chat.completions.create.return_value = mock_response
        
        with pytest.raises(TeacherResponseError, match="empty response"):
            await base_openai_client.generate(messages=[], system_prompt="Sys")
        
    mock_response_500 = MagicMock()
    mock_response_500.status_code = 500
    @pytest.mark.parametrize("openai_error, expected_match", [
        (
            openai.RateLimitError(message="", response=MagicMock(), body=None), 
            "The teacher is currently busy"
        ),
        (
            openai.AuthenticationError(message="", response=MagicMock(), body=None), 
            r"Teacher service configuration error \(Auth\)"
        ),
        (
            openai.PermissionDeniedError(message="", response=MagicMock(), body=None), 
            "Access denied to the learning service"
        ),
        (
            openai.APIConnectionError(message="", request=MagicMock()), 
            "The teacher service is currently unavailable"
        ),
        (
            openai.APIStatusError(message="", response=mock_response_500, body=None), 
            r"Teacher service encountered an error \(500\)"
        ),
    ])
    async def test_should_map_openai_exceptions_to_domain_error(
        self,
        base_openai_client: AsyncMock,
        openai_client_mock: AsyncMock,
        openai_error: Exception,
        expected_match: str
    ) -> None:
        openai_client_mock.chat.completions.create.side_effect = openai_error

        with pytest.raises(TeacherResponseError, match=expected_match):
            await base_openai_client.generate(messages=[], system_prompt="Sys")