"""
Unit tests for delete_task tool.
"""

import pytest
from unittest.mock import MagicMock, patch
from sqlmodel import Session
from backend.mcp_server.tools.delete_task import delete_task
from backend.mcp_server.schemas import ErrorCode


def test_delete_task_success():
    """Test deleting a task successfully."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Test Task"

    with patch('backend.mcp_server.tools.delete_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.delete_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.delete_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.first.return_value = mock_task

        result = delete_task(user_id="user_abc123", task_id=1)

    assert result["success"] is True
    assert result["data"]["task_id"] == 1
    assert result["data"]["status"] == "deleted"
    assert result["data"]["title"] == "Test Task"
    assert result["error"] is None


def test_delete_task_not_found():
    """Test deleting a non-existent task returns NOT_FOUND."""
    with patch('backend.mcp_server.tools.delete_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.delete_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.delete_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.first.return_value = None

        result = delete_task(user_id="user_abc123", task_id=999)

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"]["code"] == ErrorCode.NOT_FOUND


def test_delete_task_ownership_verification():
    """Test that delete_task verifies task ownership via user_id."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Test Task"
    mock_task.user_id = "user_abc123"

    with patch('backend.mcp_server.tools.delete_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.delete_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.delete_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False

        # Return None when user_id doesn't match (ownership verification via query filter)
        mock_session.exec.return_value.first.return_value = None

        # Try to delete with different user_id
        result = delete_task(user_id="user_xyz456", task_id=1)

    # Should return NOT_FOUND because user doesn't own the task
    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.NOT_FOUND


def test_delete_task_invalid_user_id():
    """Test deleting a task with empty user_id."""
    result = delete_task(user_id="", task_id=1)

    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT


def test_delete_task_invalid_task_id():
    """Test deleting a task with invalid task_id."""
    result = delete_task(user_id="user_abc123", task_id=0)

    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT


def test_delete_task_response_format():
    """Test delete_task returns correct response format."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Test Task"

    with patch('backend.mcp_server.tools.delete_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.delete_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.delete_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.first.return_value = mock_task

        result = delete_task(user_id="user_abc123", task_id=1)

    # Response must have all three top-level keys
    assert "success" in result
    assert "data" in result
    assert "error" in result

    # Data must have required fields
    assert result["data"]["task_id"] is not None
    assert result["data"]["status"] is not None
    assert result["data"]["title"] is not None


def test_delete_task_filters_by_user_id():
    """Test that delete_task filters by user_id."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Test Task"

    with patch('backend.mcp_server.tools.delete_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.delete_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.delete_task.select') as mock_select, \
         patch('backend.mcp_server.tools.delete_task.Task') as mock_task_class:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.first.return_value = mock_task

        delete_task(user_id="user_abc123", task_id=1)

        # Verify select was called
        mock_select.assert_called()


def test_delete_task_returns_title():
    """Test that delete_task retrieves and returns the task title."""
    mock_task = MagicMock()
    mock_task.id = 42
    mock_task.title = "Important Meeting"

    with patch('backend.mcp_server.tools.delete_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.delete_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.delete_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.first.return_value = mock_task

        result = delete_task(user_id="user_abc123", task_id=42)

    assert result["success"] is True
    assert result["data"]["title"] == "Important Meeting"
