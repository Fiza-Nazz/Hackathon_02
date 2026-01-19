"""
Unit tests for add_task tool.
"""

import pytest
from unittest.mock import MagicMock, patch
from sqlmodel import Session
from backend.mcp_server.tools.add_task import add_task
from backend.mcp_server.schemas import ErrorCode


def test_add_task_valid_input():
    """Test adding a task with valid input."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Buy groceries"
    mock_task.description = "Milk, eggs, bread"
    mock_task.completed = False

    with patch('backend.mcp_server.tools.add_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.add_task.Session') as mock_session_class:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.side_effect = lambda task: setattr(task, 'id', 1)

        result = add_task(
            user_id="user_abc123",
            title="Buy groceries",
            description="Milk, eggs, bread"
        )

        assert result["success"] is True
        assert result["data"]["task_id"] == 1
        assert result["data"]["status"] == "created"
        assert result["data"]["title"] == "Buy groceries"
        assert result["error"] is None


def test_add_task_without_description():
    """Test adding a task without description (optional field)."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Call mom"
    mock_task.description = None
    mock_task.completed = False

    with patch('backend.mcp_server.tools.add_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.add_task.Session') as mock_session_class:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.side_effect = lambda task: setattr(task, 'id', 1)

        result = add_task(
            user_id="user_abc123",
            title="Call mom"
        )

        assert result["success"] is True
        assert result["data"]["status"] == "created"
        assert result["data"]["title"] == "Call mom"


def test_add_task_title_validation_empty():
    """Test add_task rejects empty title."""
    result = add_task(
        user_id="user_abc123",
        title=""
    )

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT
    assert "title" in result["error"]["message"].lower()


def test_add_task_title_validation_too_short():
    """Test add_task rejects title shorter than 1 character."""
    result = add_task(
        user_id="user_abc123",
        title=""
    )

    assert result["success"] is False
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT


def test_add_task_title_validation_too_long():
    """Test add_task rejects title longer than 200 characters."""
    long_title = "A" * 201

    result = add_task(
        user_id="user_abc123",
        title=long_title
    )

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT
    assert "title" in result["error"]["message"].lower()


def test_add_task_description_validation_too_long():
    """Test add_task rejects description longer than 1000 characters."""
    long_desc = "A" * 1001

    result = add_task(
        user_id="user_abc123",
        title="Valid title",
        description=long_desc
    )

    assert result["success"] is False
    assert result["data"] is None
    assert result["error"]["code"] == ErrorCode.INVALID_INPUT


def test_add_task_user_association():
    """Test task is created with correct user association."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "User specific task"
    mock_task.user_id = "user_xyz456"
    mock_task.completed = False

    with patch('backend.mcp_server.tools.add_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.add_task.Session') as mock_session_class:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.side_effect = lambda task: setattr(task, 'id', 1)

        result = add_task(
            user_id="user_xyz456",
            title="User specific task"
        )

        assert result["success"] is True
        # The task should be associated with user_xyz456


def test_add_task_returns_correct_format():
    """Test add_task returns consistent response format."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Test task"
    mock_task.completed = False

    with patch('backend.mcp_server.tools.add_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.add_task.Session') as mock_session_class:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.side_effect = lambda task: setattr(task, 'id', 1)

        result = add_task(
            user_id="user_abc123",
            title="Test task"
        )

        # Response must have all three top-level keys
        assert "success" in result
        assert "data" in result
        assert "error" in result

        # Data must have required fields
        assert result["data"]["task_id"] is not None
        assert result["data"]["status"] is not None
        assert result["data"]["title"] is not None


def test_add_task_special_characters_in_title():
    """Test add_task handles special characters in title."""
    special_title = "Buy groceries! 🛒 (milk, eggs)"

    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = special_title
    mock_task.completed = False

    with patch('backend.mcp_server.tools.add_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.add_task.Session') as mock_session_class:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.side_effect = lambda task: setattr(task, 'id', 1)

        result = add_task(
            user_id="user_abc123",
            title=special_title
        )

        assert result["success"] is True
        assert result["data"]["title"] == special_title


def test_add_task_special_characters_in_description():
    """Test add_task handles special characters in description."""
    special_desc = "Remember to: buy milk 🥛, eggs 🥚, bread 🍞"

    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Shopping list"
    mock_task.description = special_desc
    mock_task.completed = False

    with patch('backend.mcp_server.tools.add_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.add_task.Session') as mock_session_class:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.side_effect = lambda task: setattr(task, 'id', 1)

        result = add_task(
            user_id="user_abc123",
            title="Shopping list",
            description=special_desc
        )

        assert result["success"] is True
        assert result["data"]["title"] == "Shopping list"


def test_add_task_minimal_title():
    """Test add_task accepts minimum title length (1 character)."""
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "A"
    mock_task.completed = False

    with patch('backend.mcp_server.tools.add_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.add_task.Session') as mock_session_class:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.side_effect = lambda task: setattr(task, 'id', 1)

        result = add_task(
            user_id="user_abc123",
            title="A"
        )

        assert result["success"] is True
        assert result["data"]["title"] == "A"


def test_add_task_max_title():
    """Test add_task accepts maximum title length (200 characters)."""
    max_title = "A" * 200

    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = max_title
    mock_task.completed = False

    with patch('backend.mcp_server.tools.add_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.add_task.Session') as mock_session_class:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.side_effect = lambda task: setattr(task, 'id', 1)

        result = add_task(
            user_id="user_abc123",
            title=max_title
        )

        assert result["success"] is True
        assert len(result["data"]["title"]) == 200


def test_add_task_max_description():
    """Test add_task accepts maximum description length (1000 characters)."""
    max_desc = "A" * 1000

    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.title = "Task"
    mock_task.description = max_desc
    mock_task.completed = False

    with patch('backend.mcp_server.tools.add_task.get_engine') as mock_get_engine, \
         patch('backend.mcp_server.tools.add_task.Session') as mock_session_class:
        mock_get_engine.return_value = MagicMock()
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__.return_value = mock_session
        mock_session_class.return_value.__exit__.return_value = False
        mock_session.add.return_value = None
        mock_session.commit.return_value = None
        mock_session.refresh.side_effect = lambda task: setattr(task, 'id', 1)

        result = add_task(
            user_id="user_abc123",
            title="Task",
            description=max_desc
        )

        assert result["success"] is True
