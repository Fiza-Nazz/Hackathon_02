"""
Integration test for MCP tool coordination.

Tests the full workflow: add, list, complete, update, delete tasks.
"""

import pytest
from sqlmodel import Session, create_engine, select
from backend.models.task import Task
from backend.mcp_server.tools.add_task import add_task
from backend.mcp_server.tools.list_tasks import list_tasks
from backend.mcp_server.tools.complete_task import complete_task
from backend.mcp_server.tools.delete_task import delete_task
from backend.mcp_server.tools.update_task import update_task


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


def test_full_workflow_add_list_complete_update_delete(session, test_engine):
    """Test complete workflow: add, list, complete, update, delete."""
    from unittest.mock import patch

    user_id = "user_abc123"

    # Step 1: Add tasks
    with patch('backend.mcp_server.tools.add_task.get_engine', return_value=test_engine):
        task1_result = add_task(
            user_id=user_id,
            title="Buy groceries",
            description="Milk, eggs, bread"
        )

        task2_result = add_task(
            user_id=user_id,
            title="Call mom",
            description="Ask about weekend plans"
        )

        task3_result = add_task(
            user_id=user_id,
            title="Finish project"
        )

    assert task1_result["success"] is True
    assert task2_result["success"] is True
    assert task3_result["success"] is True

    task1_id = task1_result["data"]["task_id"]
    task2_id = task2_result["data"]["task_id"]
    task3_id = task3_result["data"]["task_id"]

    # Step 2: List all tasks
    with patch('backend.mcp_server.tools.list_tasks.get_engine', return_value=test_engine):
        list_result = list_tasks(user_id=user_id)

    assert list_result["success"] is True
    assert list_result["data"]["total"] == 3
    assert len(list_result["data"]["tasks"]) == 3

    # Step 3: List pending tasks only
    with patch('backend.mcp_server.tools.list_tasks.get_engine', return_value=test_engine):
        pending_result = list_tasks(user_id=user_id, status="pending")

    assert pending_result["success"] is True
    assert pending_result["data"]["total"] == 3
    assert all(task["completed"] is False for task in pending_result["data"]["tasks"])

    # Step 4: Complete first task
    with patch('backend.mcp_server.tools.complete_task.get_engine', return_value=test_engine):
        complete_result = complete_task(user_id=user_id, task_id=task1_id)

    assert complete_result["success"] is True
    assert complete_result["data"]["status"] == "completed"

    # Step 5: List completed tasks
    with patch('backend.mcp_server.tools.list_tasks.get_engine', return_value=test_engine):
        completed_result = list_tasks(user_id=user_id, status="completed")

    assert completed_result["success"] is True
    assert completed_result["data"]["total"] == 1
    assert completed_result["data"]["tasks"][0]["title"] == "Buy groceries"

    # Step 6: Update second task
    with patch('backend.mcp_server.tools.update_task.get_engine', return_value=test_engine):
        update_result = update_task(
            user_id=user_id,
            task_id=task2_id,
            title="Call mom about weekend",
            description="Ask about Saturday plans"
        )

    assert update_result["success"] is True
    assert update_result["data"]["status"] == "updated"

    # Step 7: Verify update in database
    task = session.get(Task, task2_id)
    assert task.title == "Call mom about weekend"
    assert task.description == "Ask about Saturday plans"

    # Step 8: Delete third task
    with patch('backend.mcp_server.tools.delete_task.get_engine', return_value=test_engine):
        delete_result = delete_task(user_id=user_id, task_id=task3_id)

    assert delete_result["success"] is True
    assert delete_result["data"]["status"] == "deleted"

    # Step 9: Verify deletion in database
    deleted_task = session.get(Task, task3_id)
    assert deleted_task is None

    # Step 10: List remaining tasks
    with patch('backend.mcp_server.tools.list_tasks.get_engine', return_value=test_engine):
        final_list_result = list_tasks(user_id=user_id)

    assert final_list_result["success"] is True
    assert final_list_result["data"]["total"] == 2


def test_multiple_users_isolated_workflow(session, test_engine):
    """Test that workflows for multiple users remain isolated."""
    from unittest.mock import patch

    user1_id = "user_abc123"
    user2_id = "user_xyz456"

    # User 1 adds tasks
    with patch('backend.mcp_server.tools.add_task.get_engine', return_value=test_engine):
        user1_task1 = add_task(user_id=user1_id, title="User1 Task 1")
        user1_task2 = add_task(user_id=user1_id, title="User1 Task 2")

    # User 2 adds tasks
    with patch('backend.mcp_server.tools.add_task.get_engine', return_value=test_engine):
        user2_task1 = add_task(user_id=user2_id, title="User2 Task 1")
        user2_task2 = add_task(user_id=user2_id, title="User2 Task 2")

    # User 1 completes one of their tasks
    with patch('backend.mcp_server.tools.complete_task.get_engine', return_value=test_engine):
        complete_result = complete_task(
            user_id=user1_id,
            task_id=user1_task1["data"]["task_id"]
        )

    assert complete_result["success"] is True

    # User 1 lists their tasks
    with patch('backend.mcp_server.tools.list_tasks.get_engine', return_value=test_engine):
        user1_list = list_tasks(user_id=user1_id)

    assert user1_list["success"] is True
    assert user1_list["data"]["total"] == 2

    # User 2 lists their tasks
    with patch('backend.mcp_server.tools.list_tasks.get_engine', return_value=test_engine):
        user2_list = list_tasks(user_id=user2_id)

    assert user2_list["success"] is True
    assert user2_list["data"]["total"] == 2
    # User 2's tasks should all be pending
    assert all(task["completed"] is False for task in user2_list["data"]["tasks"])

    # User 2 tries to complete User 1's task (should fail)
    with patch('backend.mcp_server.tools.complete_task.get_engine', return_value=test_engine):
        cross_user_result = complete_task(
            user_id=user2_id,
            task_id=user1_task2["data"]["task_id"]
        )

    assert cross_user_result["success"] is False


def test_idempotent_complete_task(session, test_engine):
    """Test that completing a task twice is idempotent."""
    from unittest.mock import patch

    user_id = "user_abc123"

    # Add task
    with patch('backend.mcp_server.tools.add_task.get_engine', return_value=test_engine):
        task_result = add_task(
            user_id=user_id,
            title="Test task"
        )

    task_id = task_result["data"]["task_id"]

    # Complete task first time
    with patch('backend.mcp_server.tools.complete_task.get_engine', return_value=test_engine):
        complete_result1 = complete_task(user_id=user_id, task_id=task_id)

    assert complete_result1["success"] is True
    assert complete_result1["data"]["status"] == "completed"

    # Complete task second time (should still succeed)
    with patch('backend.mcp_server.tools.complete_task.get_engine', return_value=test_engine):
        complete_result2 = complete_task(user_id=user_id, task_id=task_id)

    assert complete_result2["success"] is True
    assert complete_result2["data"]["status"] == "completed"


def test_update_preserves_completion_status(session, test_engine):
    """Test that updating a task doesn't change its completion status."""
    from unittest.mock import patch

    user_id = "user_abc123"

    # Add task
    with patch('backend.mcp_server.tools.add_task.get_engine', return_value=test_engine):
        task_result = add_task(
            user_id=user_id,
            title="Original title"
        )

    task_id = task_result["data"]["task_id"]

    # Complete task
    with patch('backend.mcp_server.tools.complete_task.get_engine', return_value=test_engine):
        complete_result = complete_task(user_id=user_id, task_id=task_id)

    assert complete_result["success"] is True

    # Update task (title only)
    with patch('backend.mcp_server.tools.update_task.get_engine', return_value=test_engine):
        update_result = update_task(
            user_id=user_id,
            task_id=task_id,
            title="Updated title"
        )

    assert update_result["success"] is True

    # Verify task is still completed
    task = session.get(Task, task_id)
    assert task.completed is True
    assert task.title == "Updated title"


def test_empty_list_handles_gracefully(session, test_engine):
    """Test that listing tasks when none exist returns empty list."""
    from unittest.mock import patch

    user_id = "new_user"

    # List tasks for user with no tasks
    with patch('backend.mcp_server.tools.list_tasks.get_engine', return_value=test_engine):
        list_result = list_tasks(user_id=user_id)

    assert list_result["success"] is True
    assert list_result["data"]["total"] == 0
    assert len(list_result["data"]["tasks"]) == 0
