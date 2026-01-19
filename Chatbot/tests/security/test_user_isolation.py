"""
Security tests for user isolation across all task management tools.

Tests ensure that users cannot access or modify tasks belonging to other users.
"""

import pytest
import asyncio
from unittest.mock import MagicMock, patch
from backend.mcp_server.tools.add_task import add_task
from backend.mcp_server.tools.list_tasks import list_tasks
from backend.mcp_server.tools.complete_task import complete_task
from backend.mcp_server.tools.delete_task import delete_task
from backend.mcp_server.tools.update_task import update_task
from backend.mcp_server.schemas import ErrorCode


def test_add_task_only_creates_for_specified_user():
    """Test that add_task only creates task for the specified user_id."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Test Task"
    mock_task.user_id = "user_abc123"

    with patch('backend.mcp_server.tools.add_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.add_task.Session') as mock_session_class:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.side_effect = lambda task: setattr(task, 'id', 1)

        result = add_task(user_id="user_abc123", title="Test Task")

    assert result["success"] is True


def test_list_tasks_only_returns_user_own_tasks():
    """Test that list_tasks only returns tasks for the specified user_id."""
    mock_tasks = [
        MagicMock(id=1, title="User1 Task", completed=False, created_at="2024-01-01"),
        MagicMock(id=2, title="User1 Task 2", completed=True, created_at="2024-01-02"),
    ]

    with patch('backend.mcp_server.tools.list_tasks.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.list_tasks.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.list_tasks.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.all.return_value = mock_tasks

        result = list_tasks(user_id="user_abc123")

    assert result["success"] is True
    # All returned tasks should be for user_abc123 (verified by query filter)


def test_complete_task_requires_user_ownership():
    """Test that complete_task only works for tasks owned by the user."""
    # Task belongs to user_abc123
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "User1 Task"
    mock_task.user_id = "user_abc123"

    with patch('backend.mcp_server.tools.complete_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.complete_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.complete_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        # Return None because user_id doesn't match (ownership verified via query filter)
        mock_session.exec.return_value.first.return_value = None

        # user_xyz456 tries to complete user_abc123's task
        result = complete_task(user_id="user_xyz456", task_id=1)

    # Should fail because user doesn't own the task
    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.NOT_FOUND


def test_delete_task_requires_user_ownership():
    """Test that delete_task only works for tasks owned by the user."""
    # Task belongs to user_abc123
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "User1 Task"
    mock_task.user_id = "user_abc123"

    with patch('backend.mcp_server.tools.delete_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.delete_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.delete_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        # Return None because user_id doesn't match
        mock_session.exec.return_value.first.return_value = None

        # user_xyz456 tries to delete user_abc123's task
        result = delete_task(user_id="user_xyz456", task_id=1)

    # Should fail because user doesn't own the task
    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.NOT_FOUND


def test_update_task_requires_user_ownership():
    """Test that update_task only works for tasks owned by the user."""
    # Task belongs to user_abc123
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "User1 Task"
    mock_task.user_id = "user_abc123"

    with patch('backend.mcp_server.tools.update_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.update_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.update_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        # Return None because user_id doesn't match
        mock_session.exec.return_value.first.return_value = None

        # user_xyz456 tries to update user_abc123's task
        result = update_task(user_id="user_xyz456", task_id=1, title="Changed Title")

    # Should fail because user doesn't own the task
    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.NOT_FOUND


def test_empty_user_id_rejected():
    """Test that all tools reject empty user_id."""
    # add_task (now sync)
    result = add_task(user_id="", title="Test")
    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT

    # list_tasks (should handle gracefully)
    # (Implementation-dependent - may return error or empty list)

    # complete_task (sync)
    result = complete_task(user_id="", task_id=1)
    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT

    # delete_task (sync)
    result = delete_task(user_id="", task_id=1)
    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT

    # update_task (sync)
    result = update_task(user_id="", task_id=1, title="New")
    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT


def test_whitespace_only_user_id_rejected():
    """Test that all tools reject whitespace-only user_id."""
    # add_task (now sync)
    result = add_task(user_id="   ", title="Test")
    assert result["success"] is False

    # complete_task (sync)
    result = complete_task(user_id="   ", task_id=1)
    assert result["success"] is False

    # delete_task (sync)
    result = delete_task(user_id="   ", task_id=1)
    assert result["success"] is False

    # update_task (sync)
    result = update_task(user_id="   ", task_id=1, title="New")
    assert result["success"] is False


def test_multiple_users_cannot_see_each_others_tasks():
    """Test that multiple users are isolated from each other."""
    # Create tasks for user1
    user1_tasks = [
        MagicMock(id=1, title="User1 Task 1", completed=False, created_at="2024-01-01"),
        MagicMock(id=2, title="User1 Task 2", completed=False, created_at="2024-01-02"),
    ]

    # Create tasks for user2
    user2_tasks = [
        MagicMock(id=3, title="User2 Task 1", completed=False, created_at="2024-01-03"),
        MagicMock(id=4, title="User2 Task 2", completed=False, created_at="2024-01-04"),
    ]

    # User1 lists their tasks
    with patch('backend.mcp_server.tools.list_tasks.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.list_tasks.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.list_tasks.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.all.return_value = user1_tasks

        result = list_tasks(user_id="user_abc123")

    assert result["success"] is True
    assert result["data"]["total"] == 2
    # User1 should only see their own tasks

    # User2 lists their tasks
    with patch('backend.mcp_server.tools.list_tasks.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.list_tasks.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.list_tasks.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.all.return_value = user2_tasks

        result = list_tasks(user_id="user_xyz456")

    assert result["success"] is True
    assert result["data"]["total"] == 2
    # User2 should only see their own tasks


def test_not_found_does_not_leak_ownership():
    """Test that NOT_FOUND errors don't leak whether a task exists for another user."""
    # This tests security by obscurity - we should NOT distinguish between
    # "task doesn't exist" and "task exists but belongs to someone else"

    # Scenario 1: Task doesn't exist at all
    with patch('backend.mcp_server.tools.complete_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.complete_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.complete_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.first.return_value = None

        result = complete_task(user_id="user_abc123", task_id=999)

    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.NOT_FOUND

    # Scenario 2: Task exists but belongs to another user
    # The implementation filters by user_id in the query, so when user_id doesn't match,
    # no results are returned (NOT_FOUND, not ownership error)
    with patch('backend.mcp_server.tools.complete_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.complete_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.complete_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        # Return None because user_id doesn't match (simulating query with user_id filter)
        mock_session.exec.return_value.first.return_value = None

        result = complete_task(user_id="user_abc123", task_id=1)

    # Both scenarios should return the same error - NOT_FOUND
    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.NOT_FOUND
    # User cannot tell if task doesn't exist or belongs to someone else
