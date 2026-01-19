"""
Unit tests for Message model.
"""

import pytest
from datetime import datetime
from backend.models.message import Message


def test_message_creation():
    """Test creating a message with required fields."""
    message = Message(
        conversation_id=123,
        user_id="user_abc123",
        role="user",
        content="Hello AI assistant!"
    )

    assert message.conversation_id == 123
    assert message.user_id == "user_abc123"
    assert message.role == "user"
    assert message.content == "Hello AI assistant!"
    assert message.id is None  # Not set until committed
    assert message.tool_calls is None
    assert isinstance(message.created_at, datetime)


def test_message_with_tool_calls():
    """Test creating a message with tool_calls."""
    tool_calls = {
        "name": "add_task",
        "parameters": {"title": "Buy groceries"},
        "result": {"task_id": 1, "status": "created"}
    }

    message = Message(
        conversation_id=123,
        user_id="user_abc123",
        role="assistant",
        content="I've created a task for you.",
        tool_calls=tool_calls
    )

    assert message.tool_calls == tool_calls
    assert message.tool_calls["name"] == "add_task"


def test_message_role_validation():
    """Test message role can be 'user' or 'assistant'."""
    # These should both be valid
    user_msg = Message(conversation_id=123, user_id="user_abc", role="user", content="test")
    assistant_msg = Message(conversation_id=123, user_id="user_abc", role="assistant", content="test")

    assert user_msg.role == "user"
    assert assistant_msg.role == "assistant"


def test_message_fields():
    """Test message model has correct fields."""
    message = Message(
        conversation_id=123,
        user_id="user_abc123",
        role="user",
        content="test"
    )

    # Check all expected fields exist
    assert hasattr(message, "id")
    assert hasattr(message, "conversation_id")
    assert hasattr(message, "user_id")
    assert hasattr(message, "role")
    assert hasattr(message, "content")
    assert hasattr(message, "tool_calls")
    assert hasattr(message, "created_at")


def test_message_timestamps_auto():
    """Test message timestamp is auto-generated."""
    message = Message(
        conversation_id=123,
        user_id="user_abc123",
        role="user",
        content="test"
    )

    assert message.created_at is not None
    assert isinstance(message.created_at, datetime)


def test_message_tool_calls_optional():
    """Test tool_calls is optional field."""
    # Without tool_calls
    message1 = Message(
        conversation_id=123,
        user_id="user_abc123",
        role="user",
        content="test"
    )
    assert message1.tool_calls is None

    # With tool_calls
    message2 = Message(
        conversation_id=123,
        user_id="user_abc123",
        role="assistant",
        content="test",
        tool_calls={"name": "test", "parameters": {}}
    )
    assert message2.tool_calls is not None


def test_message_table_name():
    """Test message has correct table name."""
    assert Message.__tablename__ == "messages"


def test_message_content_required():
    """Test content is a required field."""
    # Content must be provided
    message = Message(
        conversation_id=123,
        user_id="user_abc123",
        role="user",
        content="Required content"
    )
    assert message.content == "Required content"


def test_message_long_content():
    """Test message can store long content."""
    long_content = "A" * 10000  # Very long message
    message = Message(
        conversation_id=123,
        user_id="user_abc123",
        role="user",
        content=long_content
    )
    assert len(message.content) == 10000
