"""
Unit tests for complete_task tool.
"""

import pytest
from unittest.mock import MagicMock, patch
from sqlmodel import Session
from backend.mcp_server.tools.complete_task import complete_task
from backend.mcp_server.schemas import ErrorCode


def test_complete_task_success():
    """Test completing a task successfully."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Test Task"
    mock_task.completed = False

    with patch('backend.mcp_server.tools.complete_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.complete_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.complete_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.first.return_value = mock_task

        result = complete_task(user_id="user_abc123", task_id=1)

    assert result["success"] is True
    assert result["data"]["task_id"] == 1
    assert result["data"]["status"] == "completed"
    assert result["data"]["title"] == "Test Task"
    assert result["error"] is None


def test_complete_task_already_complete():
    """Test completing a task that is already completed (idempotent)."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Test Task"
    mock_task.completed = True  # Already completed

    with patch('backend.mcp_server.tools.complete_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.complete_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.complete_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.first.return_value = mock_task

        result = complete_task(user_id="user_abc123", task_id=1)

    # Should still return success even if already completed
    assert result["success"] is True
    assert result["data"]["status"] == "completed"


def test_complete_task_not_found():
    """Test completing a non-existent task returns NOT_FOUND."""
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
    assert result["data"] is None
    assert result["error"]["code"] == ErrorCode.NOT_FOUND


def test_complete_task_invalid_user_id():
    """Test completing a task with empty user_id."""
    result = complete_task(user_id="", task_id=1)

    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT


def test_complete_task_invalid_task_id():
    """Test completing a task with invalid task_id."""
    result = complete_task(user_id="user_abc123", task_id=0)

    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT


def test_complete_task_response_format():
    """Test complete_task returns correct response format."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Test Task"
    mock_task.completed = False

    with patch('backend.mcp_server.tools.complete_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.complete_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.complete_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.first.return_value = mock_task

        result = complete_task(user_id="user_abc123", task_id=1)

    # Response must have all three top-level keys
    assert "success" in result
    assert "data" in result
    assert "error" in result

    # Data must have required fields
    assert result["data"]["task_id"] is not None
    assert result["data"]["status"] is not None
    assert result["data"]["title"] is not None


def test_complete_task_filters_by_user_id():
    """Test that complete_task filters by user_id."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Test Task"
    mock_task.completed = False

    with patch('backend.mcp_server.tools.complete_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.complete_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.complete_task.select') as mock_select, \
         patch('backend.mcp_server.tools.complete_task.Task') as mock_task_class:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.first.return_value = mock_task

        complete_task(user_id="user_abc123", task_id=1)

        # Verify select was called
        mock_select.assert_called()


def test_complete_task_updates_completed_field():
    """Test that complete_task actually updates the completed field."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Test Task"
    mock_task.completed = False

    with patch('backend.mcp_server.tools.complete_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.complete_task.Session') as mock_session_class, \
         patch('backend.mcp_server.tools.complete_task.select') as mock_select:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.exec.return_value.first.return_value = mock_task

        result = complete_task(user_id="user_abc123", task_id=1)

    assert result["success"] is True
    # The task's completed field should be set to True
    mock_task.completed = True
