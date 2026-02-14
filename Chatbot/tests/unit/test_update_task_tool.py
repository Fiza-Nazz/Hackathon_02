"""
Unit tests for update_task tool.
"""

import pytest
from unittest.mock import MagicMock, patch
from sqlmodel import Session
from backend.mcp_server.tools.update_task import update_task
from backend.mcp_server.schemas import ErrorCode


def test_update_task_title_only():
    """Test updating only the task title."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Old Title"
    mock_task.description = "Original description"
    mock_task.completed = False

    with patch('backend.mcp_server.tools.update_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.update_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.update_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.first.return_value = mock_task

        result = update_task(user_id="user_abc123", task_id=1, title="New Title")

    assert result["success"] is True
    assert result["data"]["task_id"] == 1
    assert result["data"]["status"] == "updated"
    assert result["data"]["title"] == "New Title"
    assert result["error"] is None


def test_update_task_description_only():
    """Test updating only the task description."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Task Title"
    mock_task.description = "Old description"
    mock_task.completed = False

    with patch('backend.mcp_server.tools.update_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.update_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.update_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.first.return_value = mock_task

        result = update_task(user_id="user_abc123", task_id=1, description="New description")

    assert result["success"] is True
    assert result["data"]["task_id"] == 1
    assert result["data"]["status"] == "updated"


def test_update_task_both_fields():
    """Test updating both title and description."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Old Title"
    mock_task.description = "Old description"
    mock_task.completed = False

    with patch('backend.mcp_server.tools.update_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.update_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.update_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.first.return_value = mock_task

        result = update_task(
            user_id="user_abc123",
            task_id=1,
            title="New Title",
            description="New description"
        )

    assert result["success"] is True
    assert result["data"]["task_id"] == 1


def test_update_task_neither_field():
    """Test updating with neither title nor description returns error."""
    result = update_task(user_id="user_abc123", task_id=1)

    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT
    assert "at least one" in result["error"]["message"].lower()


def test_update_task_not_found():
    """Test updating a non-existent task returns NOT_FOUND."""
    with patch('backend.mcp_server.tools.update_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.update_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.update_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.first.return_value = None

        result = update_task(user_id="user_abc123", task_id=999, title="New Title")

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"]["code"] == ErrorCode.NOT_FOUND


def test_update_task_invalid_title_length():
    """Test updating with title that exceeds 200 characters."""
    result = update_task(
        user_id="user_abc123",
        task_id=1,
        title="A" * 201
    )

    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT


def test_update_task_invalid_description_length():
    """Test updating with description that exceeds 1000 characters."""
    result = update_task(
        user_id="user_abc123",
        task_id=1,
        description="A" * 1001
    )

    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT


def test_update_task_invalid_user_id():
    """Test updating a task with empty user_id."""
    result = update_task(user_id="", task_id=1, title="New Title")

    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT


def test_update_task_invalid_task_id():
    """Test updating a task with invalid task_id."""
    result = update_task(user_id="user_abc123", task_id=0, title="New Title")

    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT


def test_update_task_response_format():
    """Test update_task returns correct response format."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Task Title"
    mock_task.description = "Description"
    mock_task.completed = False

    with patch('backend.mcp_server.tools.update_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.update_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.update_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.first.return_value = mock_task

        result = update_task(user_id="user_abc123", task_id=1, title="New Title")

    # Response must have all three top-level keys
    assert "success" in result
    assert "data" in result
    assert "error" in result

    # Data must have required fields
    assert result["data"]["task_id"] is not None
    assert result["data"]["status"] is not None
    assert result["data"]["title"] is not None


def test_update_task_filters_by_user_id():
    """Test that update_task filters by user_id."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Task Title"
    mock_task.user_id = "user_abc123"

    with patch('backend.mcp_server.tools.update_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.update_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.update_task.select') as mock_select, \
         patch('backend.mcp_server.tools.update_task.Task') as mock_task_class:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.first.return_value = mock_task

        update_task(user_id="user_abc123", task_id=1, title="New Title")

        # Verify select was called
        mock_select.assert_called()


def test_update_task_whitespace_only_title():
    """Test updating with title that contains only whitespace."""
    result = update_task(
        user_id="user_abc123",
        task_id=1,
        title="   "
    )

    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT


def test_update_task_empty_title():
    """Test updating with empty string title."""
    result = update_task(
        user_id="user_abc123",
        task_id=1,
        title=""
    )

    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT
