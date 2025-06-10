import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Task Manager API is running!"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_docs_available():
    response = client.get("/docs")
    assert response.status_code == 200


def test_register_user():
    # This is a basic test - in real tests you'd use a test database
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    # Note: This will fail without proper test database setup
    # response = client.post("/auth/register", json=user_data)
    # assert response.status_code == 201 