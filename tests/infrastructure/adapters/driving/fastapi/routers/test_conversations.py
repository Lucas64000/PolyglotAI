
from collections.abc import Callable
from uuid import uuid4
from fastapi import status
from fastapi.testclient import TestClient

from src.core.domain.entities import Conversation, Student
from src.core.domain.value_objects import Status

from src.infrastructure.adapters.driven import InMemoryConversationRepository

def test_create_conversation_should_return_201(
    client: TestClient,
    make_student: Callable[..., Student]
) -> None:
    student = make_student()
    
    payload = {
        "student_id": str(student.id),
        "native_lang": "en",
        "target_lang": "fr"
    }

    response = client.post("/api/conversations", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "conversation_id" in data

def test_create_conversation_invalid_lang_should_return_400(
    client: TestClient,
    make_student: Callable[..., Student],
) -> None:
    student = make_student()

    payload = {
        "student_id": str(student.id),
        "native_lang": "zzz", # Invalid ISO code
        "target_lang": "fr"
    }
    response = client.post("/api/conversations", json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    error = response.json()
    assert error["type"] == "error:business-rule-violation"

async def test_list_conversations_should_filter_by_student(
    client: TestClient,
    mock_db: InMemoryConversationRepository,
    make_conversation: Callable[..., Conversation],
    make_student: Callable[..., Student],
) -> None:
    # Populate DB with 2 conversations for different students
    student1 = make_student()
    student2 = make_student()
    
    conv1 = make_conversation(student_id=student1.id)
    conv2 = make_conversation(student_id=student2.id)
    
    await mock_db.save(conv1)
    await mock_db.save(conv2)

    # Filter for Student 1
    response = client.get(f"/api/conversations?student_id={student1.id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["conversation_id"] == str(conv1.id)

async def test_get_conversation_should_return_details(
    client: TestClient, 
    mock_db: InMemoryConversationRepository,
    make_conversation: Callable[..., Conversation]
) -> None:
    conv = make_conversation()
    await mock_db.save(conv)

    response = client.get(
        f"/api/conversations/{conv.id}",
        params={"student_id": str(conv.student_id)}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["conversation_id"] == str(conv.id)

def test_get_unknown_conversation_should_return_404(client: TestClient) -> None:
    response = client.get(
        f"/api/conversations/{uuid4()}",
        params={"student_id": str(uuid4())} 
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    error = response.json()
    assert error["type"] == "error:resource-not-found"

async def test_delete_conversation_should_return_204(
    client: TestClient, 
    mock_db: InMemoryConversationRepository,
    make_conversation: Callable[..., Conversation]
):
    conv = make_conversation()
    await mock_db.save(conv)

    response = client.delete(
        f"/api/conversations/{conv.id}", 
        params={"student_id": str(conv.student_id)}
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    conv_removed = await mock_db.get_by_id(conv.id)
    assert conv_removed.status == Status.DELETED