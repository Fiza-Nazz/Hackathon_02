import pytest
from src.models import User, Task

def test_create_user(session):
    user = User(email="test@example.com", password_hash="hashed_password")
    session.add(user)
    session.commit()
    session.refresh(user)
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.password_hash == "hashed_password"

def test_create_task(session):
    user = User(email="test@example.com", password_hash="hashed_password")
    session.add(user)
    session.commit()
    session.refresh(user)
    
    task = Task(title="Test Task", description="Test Description", user_id=user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    
    assert task.id is not None
    assert task.title == "Test Task"
    assert task.user_id == user.id
    assert task.user.email == "test@example.com"
