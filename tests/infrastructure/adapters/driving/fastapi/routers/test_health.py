
from fastapi import status
from fastapi.testclient import TestClient

def test_health_check_returns_200(client: TestClient):
    """
    Verifies that the system is up and running.
    """
    response = client.get("/health")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}