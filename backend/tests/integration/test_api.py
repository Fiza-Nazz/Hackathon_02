import pytest
from src.models import UserCreate

def test_registration_and_login_flow(client):
    # Register
    response = client.post(
        "/api/auth/register",
        json={"email": "api_test@example.com", "password": "password123"}
    )
    if response.status_code != 200:
        print(f"Registration failed: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "api_test@example.com"
    
    # Login
    response = client.post(
        "/api/auth/login",
        json={"email": "api_test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    token = token_data["access_token"]
    
    # Authorized access
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/tasks/", headers=headers)
    assert response.status_code == 200
    assert response.json() == []

def test_task_api_crud(client):
    # Register & Login
    client.post(
        "/api/auth/register",
        json={"email": "crud_test@example.com", "password": "password123"}
    )
    login_resp = client.post(
        "/api/auth/login",
        json={"email": "crud_test@example.com", "password": "password123"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create
    response = client.post(
        "/api/tasks/",
        json={"title": "API Task", "description": "API Desc"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    task_id = data["id"]
    
    # Read
    response = client.get(f"/api/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "API Task"
    
    # Update
    response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Updated API Task", "completed": True},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated API Task"
    
    # Toggle
    response = client.patch(f"/api/tasks/{task_id}/complete", headers=headers)
    assert response.status_code == 200
    assert response.json()["completed"] is False
    
    # Delete
    response = client.delete(f"/api/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    
    # Verify deletion
    response = client.get(f"/api/tasks/{task_id}", headers=headers)
    assert response.status_code == 404

def test_multi_user_isolation(client):
    # User 1
    client.post("/api/auth/register", json={"email": "u1@test.com", "password": "p1"})
    login1 = client.post("/api/auth/login", json={"email": "u1@test.com", "password": "p1"})
    token1 = login1.json()["access_token"]
    
    # User 2
    client.post("/api/auth/register", json={"email": "u2@test.com", "password": "p2"})
    login2 = client.post("/api/auth/login", json={"email": "u2@test.com", "password": "p2"})
    token2 = login2.json()["access_token"]
    
    # User 1 creates a task
    res = client.post("/api/tasks/", json={"title": "U1 Task"}, headers={"Authorization": f"Bearer {token1}"})
    assert res.status_code == 200
    task_id = res.json()["id"]
    
    # User 2 tries to access User 1's task
    res = client.get(f"/api/tasks/{task_id}", headers={"Authorization": f"Bearer {token2}"})
    assert res.status_code == 404
    
    # User 2 tries to delete User 1's task
    res = client.delete(f"/api/tasks/{task_id}", headers={"Authorization": f"Bearer {token2}"})
    assert res.status_code == 404
