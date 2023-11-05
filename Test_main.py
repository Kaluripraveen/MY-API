import pytest
from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)

@pytest.fixture
def new_user_data():
    return {
        "email": "tes@example.com",
        "password": "password23",
        "username": "testuser",
        "full_name": "Test User"
    }

@pytest.fixture
def existing_user_data():
    return {
        "email": "tes@example.com",
        "password": "password23"
    }

@pytest.fixture
def invalid_user_data():
    return {
        "email": "tes@example.com"
        # Missing password, username, and full_name
    }

def test_register_user(new_user_data):
    response = client.post("/register", json=new_user_data)
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

def test_register_existing_user(new_user_data):
    # Register the user first
    client.post("/register", json=new_user_data)

    # Try to register the same user again
    response = client.post("/register", json=new_user_data)
    assert response.status_code == 200  
    assert "already exists" in response.json()["error"]

def test_register_invalid_user(invalid_user_data):
    response = client.post("/register", json=invalid_user_data)
    assert response.status_code == 422 

def test_login_user(existing_user_data):
    # Register the user first
    client.post("/register", json=existing_user_data)

    # Login with valid credentials
    response = client.post("/login", json=existing_user_data)
    assert response.status_code == 200
    assert "custom_token" in response.json()