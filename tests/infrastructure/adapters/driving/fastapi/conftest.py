
import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from typing import Generator

from src.infrastructure.adapters.driving.fastapi.main import app
from src.infrastructure.adapters.driven import InMemoryConversationRepository
from src.infrastructure.adapters.driving.fastapi.dependencies import (
    get_in_memory_db, 
    get_chat_provider,
)

@pytest.fixture
def mock_db() -> InMemoryConversationRepository:
    """
    Creates a fresh in-memory database for each test.
    """
    return InMemoryConversationRepository()

@pytest.fixture
def mock_chat_provider() -> AsyncMock:
    """
    Mocks the LLM provider to avoid real API calls and ensure determinism.
    """
    mock = AsyncMock()
    mock.get_teacher_response.return_value = "Mocked Teacher Response"
    return mock

@pytest.fixture
def client(mock_db: InMemoryConversationRepository, mock_chat_provider: AsyncMock) -> Generator[TestClient, None, None]:
    """
    Configures the TestClient with dependency overrides.
    
    CRITICAL: We override the Singletons (get_in_memory_db, get_chat_provider)
    so that the entire dependency tree uses our test doubles.
    """
    app.dependency_overrides[get_in_memory_db] = lambda: mock_db
    app.dependency_overrides[get_chat_provider] = lambda: mock_chat_provider
    
    # Yield Client
    with TestClient(app) as c:
        yield c
        
    # Cleanup (Reset overrides)
    app.dependency_overrides = {}