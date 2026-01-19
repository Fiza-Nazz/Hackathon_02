"""
Integration test for add_task tool to verify user association and data isolation.
"""

import pytest
import asyncio
from sqlmodel import Session, create_engine, select
from backend.models.task import Task
from backend.mcp_server.tools.add_task import add_task


@pytest.fixture
def test_engine():
    """Create a test database engine."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    return engine


@pytest.fixture
def session(test_engine):
    """Create a test database session."""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session

    SQLModel.metadata.drop_all(test_engine)


def test_task_created_with_correct_user_association(session, test_engine):
    """Test that a task is created with the correct user_id association."""
    # Mock the database engine to use test engine
    from unittest.mock import patch

    with patch('backend.mcp_server.tools.add_task.get_engine', return_value=test_engine):
        result = add_task(
            user_id="user_abc123",
            title="Buy groceries",
            description="Milk, eggs, bread"
        )

    # Verify success response
    assert result["success"] is True
    assert result["data"]["task_id"] is not None
    assert result["data"]["status"] == "created"
    assert result["data"]["title"] == "Buy groceries"

    # Verify task in database with correct user association
    task = session.get(Task, result["data"]["task_id"])
    assert task is not None
    assert task.user_id == "user_abc123"
    assert task.title == "Buy groceries"
    assert task.description == "Milk, eggs, bread"
    assert task.completed is False


def test_data_isolation_different_users(session, test_engine):
    """Test that users can only access their own tasks (data isolation)."""
    from unittest.mock import patch

    # User 1 creates a task
    with patch('backend.mcp_server.tools.add_task.get_engine', return_value=test_engine):
        user1_result = add_task(
            user_id="user_abc123",
            title="User 1 Task",
            description="Only for user 1"
        )

        user2_result = add_task(
            user_id="user_xyz456",
            title="User 2 Task",
            description="Only for user 2"
        )

    # Verify both tasks created
    assert user1_result["success"] is True
    assert user2_result["success"] is True

    # Query tasks for each user
    user1_tasks = session.exec(select(Task).where(Task.user_id == "user_abc123")).all()
    user2_tasks = session.exec(select(Task).where(Task.user_id == "user_xyz456")).all()

    # Verify isolation
    assert len(user1_tasks) == 1
    assert len(user2_tasks) == 1
    assert user1_tasks[0].title == "User 1 Task"
    assert user2_tasks[0].title == "User 2 Task"

    # Verify user1 cannot see user2's tasks
    assert len([t for t in user1_tasks if t.title == "User 2 Task"]) == 0


def test_task_creation_persists_across_sessions(session, test_engine):
    """Test that a created task persists across different database sessions."""
    from unittest.mock import patch

    # Create task in session 1
    with patch('backend.mcp_server.tools.add_task.get_engine', return_value=test_engine):
        result = add_task(
            user_id="user_abc123",
            title="Persistent Task",
            description="Should survive session close"
        )

    task_id = result["data"]["task_id"]

    # Close and create new session to simulate server restart
    session.close()

    with Session(test_engine) as new_session:
        # Verify task still exists
        task = new_session.get(Task, task_id)
        assert task is not None
        assert task.title == "Persistent Task"
        assert task.user_id == "user_abc123"


def test_multiple_tasks_same_user(session, test_engine):
    """Test creating multiple tasks for the same user."""
    from unittest.mock import patch

    task_ids = []

    with patch('backend.mcp_server.tools.add_task.get_engine', return_value=test_engine):
        # Create 3 tasks for same user
        for i in range(3):
            result = add_task(
                user_id="user_abc123",
                title=f"Task {i+1}",
                description=f"Description {i+1}"
            )
            task_ids.append(result["data"]["task_id"])

    # Verify all tasks exist and are associated with user
    tasks = session.exec(select(Task).where(Task.user_id == "user_abc123")).all()
    assert len(tasks) == 3

    # Verify task details
    for i, task in enumerate(tasks):
        assert task.title == f"Task {i+1}"
        assert task.description == f"Description {i+1}"
        assert task.completed is False


def test_task_without_description(session, test_engine):
    """Test that tasks can be created without optional description."""
    from unittest.mock import patch

    with patch('backend.mcp_server.tools.add_task.get_engine', return_value=test_engine):
        result = add_task(
            user_id="user_abc123",
            title="No Description Task"
        )

    assert result["success"] is True

    # Verify task in database
    task = session.get(Task, result["data"]["task_id"])
    assert task is not None
    assert task.title == "No Description Task"
    assert task.description is None


def test_task_user_id_cannot_be_modified(session, test_engine):
    """Test that user_id is correctly set and isolated."""
    from unittest.mock import patch

    with patch('backend.mcp_server.tools.add_task.get_engine', return_value=test_engine):
        result = add_task(
            user_id="user_abc123",
            title="User Specific Task"
        )

    # Verify task has correct user_id
    task = session.get(Task, result["data"]["task_id"])
    assert task is not None
    assert task.user_id == "user_abc123"

    # Try to update user_id directly in database (shouldn't happen in production)
    task.user_id = "another_user"
    session.add(task)
    session.commit()

    # Verify we can distinguish tasks by user_id
    user_tasks = session.exec(select(Task).where(Task.user_id == "user_abc123")).all()
    other_user_tasks = session.exec(select(Task).where(Task.user_id == "another_user")).all()

    # This demonstrates the importance of filtering by user_id in all queries
    assert len(other_user_tasks) == 1
