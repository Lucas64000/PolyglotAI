
from collections.abc import Callable
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from src.core.domain.entities import Student, Conversation
from src.core.domain.value_objects import CreativityLevel, GenerationStyle

from src.infrastructure.adapters.driven import InMemoryConversationRepository
from src.infrastructure.adapters.driving.fastapi.dependencies import (
    get_chat_provider, 
    get_conversation_repository
)

from src.main import app


def test_health_check_returns_200(client: TestClient):
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_conversation_should_return_201(
    client: TestClient,
    make_student: Callable[..., Student]
):
    student: Student = make_student()
    payload = {
        "student_id": str(student.id),
        "native_lang": "fr",
        "target_lang": "en",
    }
    
    response = client.post("/api/conversations", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert "conversation_id" in data

async def test_send_message_should_return_200(
    client: TestClient, 
    make_conversation: Callable[..., Conversation],
    mock_chat: AsyncMock,
):
    shared_repo = InMemoryConversationRepository()
    conversation = make_conversation()
    await shared_repo.save(conversation=conversation)

    app.dependency_overrides[get_conversation_repository] = lambda: shared_repo
    app.dependency_overrides[get_chat_provider] = lambda: mock_chat

    try:
        payload = {
            "student_message": "Hello world",
            "creativity_level": str(CreativityLevel.MODERATE.value), 
            "generation_style": str(GenerationStyle.CONVERSATIONAL.value),
        }

        response = client.post(f"/api/conversations/{conversation.id}/messages", json=payload)

        assert response.status_code == 200
        
        data = response.json()
        assert data["teacher_message"] == "Hello Student!" # mock_chat return value
        
        mock_chat.get_teacher_response.assert_called_once()

    finally:
        app.dependency_overrides = {}