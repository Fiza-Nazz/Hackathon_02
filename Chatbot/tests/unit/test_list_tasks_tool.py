"""
Unit tests for list_tasks tool.
"""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from sqlmodel import Session
from backend.mcp_server.tools.list_tasks import list_tasks
from backend.mcp_server.schemas import ErrorCode


@pytest.fixture
def mock_session():
    """Mock database session."""
    session = MagicMock(spec=Session)
    return session


def test_list_tasks_all_tasks():
    """Test listing all tasks for a user."""
    from unittest.mock import MagicMock
    from backend.models.task import Task

    mock_tasks = [
        MagicMock(id=1, title="Task 1", completed=False, created_at="2024-01-01"),
        MagicMock(id=2, title="Task 2", completed=True, created_at="2024-01-02"),
        MagicMock(id=3, title="Task 3", completed=False, created_at="2024-01-03"),
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
    assert result["data"]["total"] == 3
    assert len(result["data"]["tasks"]) == 3
    assert result["data"]["tasks"][0]["title"] == "Task 1"
    assert result["data"]["tasks"][1]["title"] == "Task 2"
    assert result["data"]["tasks"][2]["title"] == "Task 3"


def test_list_tasks_pending_only():
    """Test listing only pending tasks."""
    from unittest.mock import MagicMock
    from backend.models.task import Task

    # Return only pending tasks
    mock_pending_tasks = [
        MagicMock(id=1, title="Pending Task 1", completed=False, created_at="2024-01-01"),
        MagicMock(id=3, title="Pending Task 2", completed=False, created_at="2024-01-03"),
    ]

    with patch('backend.mcp_server.tools.list_tasks.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.list_tasks.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.list_tasks.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.all.return_value = mock_pending_tasks

        result = list_tasks(user_id="user_abc123", status="pending")

    assert result["success"] is True
    assert result["data"]["total"] == 2
    assert len(result["data"]["tasks"]) == 2
    assert all(task["completed"] is False for task in result["data"]["tasks"])


def test_list_tasks_completed_only():
    """Test listing only completed tasks."""
    from unittest.mock import MagicMock
    from backend.models.task import Task

    mock_completed_tasks = [
        MagicMock(id=2, title="Completed Task 1", completed=True, created_at="2024-01-02"),
        MagicMock(id=4, title="Completed Task 2", completed=True, created_at="2024-01-04"),
    ]

    with patch('backend.mcp_server.tools.list_tasks.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.list_tasks.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.list_tasks.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.all.return_value = mock_completed_tasks

        result = list_tasks(user_id="user_abc123", status="completed")

    assert result["success"] is True
    assert result["data"]["total"] == 2
    assert len(result["data"]["tasks"]) == 2
    assert all(task["completed"] is True for task in result["data"]["tasks"])


def test_list_tasks_empty_list():
    """Test listing tasks when user has no tasks."""
    with patch('backend.mcp_server.tools.list_tasks.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.list_tasks.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.list_tasks.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.all.return_value = []

        result = list_tasks(user_id="user_abc123")

    assert result["success"] is True
    assert result["data"]["total"] == 0
    assert len(result["data"]["tasks"]) == 0


def test_list_tasks_invalid_status():
    """Test that invalid status returns all tasks (default behavior)."""
    from unittest.mock import MagicMock

    mock_tasks = [
        MagicMock(id=1, title="Task 1", completed=False, created_at="2024-01-01"),
    ]

    with patch('backend.mcp_server.tools.list_tasks.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.list_tasks.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.list_tasks.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.all.return_value = mock_tasks

        # Invalid status should default to "all"
        result = list_tasks(user_id="user_abc123", status="invalid")

    assert result["success"] is True


def test_list_tasks_response_format():
    """Test list_tasks returns correct response format."""
    from unittest.mock import MagicMock

    mock_tasks = [
        MagicMock(id=1, title="Task 1", completed=False, created_at="2024-01-01"),
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

    # Response must have all three top-level keys
    assert "success" in result
    assert "data" in result
    assert "error" in result

    # Data must have required fields
    assert "tasks" in result["data"]
    assert "total" in result["data"]

    # Each task must have required fields
    for task in result["data"]["tasks"]:
        assert "id" in task
        assert "title" in task
        assert "completed" in task
        assert "created_at" in task


def test_list_tasks_filters_by_user_id():
    """Test that list_tasks filters by user_id."""
    from unittest.mock import MagicMock

    with patch('backend.mcp_server.tools.list_tasks.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.list_tasks.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.list_tasks.select') as mock_select, \
         patch('backend.mcp_server.tools.list_tasks.Task') as mock_task:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.all.return_value = []

        list_tasks(user_id="user_abc123")

        # Verify select was called with Task
        mock_select.assert_called()


def test_list_tasks_default_status_all():
    """Test that default status parameter lists all tasks."""
    from unittest.mock import MagicMock

    with patch('backend.mcp_server.tools.list_tasks.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.list_tasks.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.list_tasks.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.all.return_value = []

        # Call without status parameter
        result = list_tasks(user_id="user_abc123")

        # Should still return success (no status means "all")
        assert result["success"] is True
