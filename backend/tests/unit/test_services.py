import pytest
from src.models import User, UserCreate, TaskCreate, TaskUpdate
from src.services.user_service import UserService
from src.services.auth_service import AuthUtils
from src.services.task_service import TaskService

def test_user_registration(session):
    user_in = UserCreate(email="service_test@example.com", password="password123")
    user_read = UserService.create_user(session, user_in)
    
    assert user_read.email == "service_test@example.com"
    
    # Query the user from DB to verify hash
    user = session.get(User, user_read.id)
    assert AuthUtils.verify_password("password123", user.password_hash)

def test_authenticate_user(session):
    user_in = UserCreate(email="auth_test@example.com", password="password123")
    UserService.create_user(session, user_in)
    
    user = AuthUtils.authenticate_user(session, "auth_test@example.com", "password123")
    assert user is not None
    assert user.email == "auth_test@example.com"
    
    # Test wrong password
    user = AuthUtils.authenticate_user(session, "auth_test@example.com", "wrong")
    assert user is None

def test_task_operations(session):
    # Setup user
    user_in = UserCreate(email="task_user@example.com", password="password123")
    user_read = UserService.create_user(session, user_in)
    
    # Create task
    task_in = TaskCreate(title="Test Task", description="Some description")
    task = TaskService.create_task(session, task_in, user_read.id)
    assert task.title == "Test Task"
    assert task.user_id == user_read.id
    
    # Get tasks
    tasks = TaskService.get_user_tasks(session, user_read.id)
    assert len(tasks) == 1
    assert tasks[0].id == task.id
    
    # Update task
    task_update = TaskUpdate(title="Updated Title", completed=True)
    updated_task = TaskService.update_task(session, task.id, task_update, user_read.id)
    assert updated_task.title == "Updated Title"
    assert updated_task.completed is True
    
    # Toggle completion
    toggled_task = TaskService.toggle_task_completion(session, task.id, user_read.id)
    assert toggled_task.completed is False
    
    # Delete task
    success = TaskService.delete_task(session, task.id, user_read.id)
    assert success is True
    assert len(TaskService.get_user_tasks(session, user_read.id)) == 0
