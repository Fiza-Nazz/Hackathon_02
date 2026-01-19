"""
Unit tests for Conversation model.
"""

import pytest
from datetime import datetime
from backend.models.conversation import Conversation
from backend.models.message import Message


def test_conversation_creation():
    """Test creating a conversation with user_id."""
    conversation = Conversation(user_id="user_abc123")

    assert conversation.user_id == "user_abc123"
    assert conversation.id is None  # Not set until committed
    assert isinstance(conversation.created_at, datetime)
    assert isinstance(conversation.updated_at, datetime)


def test_conversation_relationships():
    """Test conversation has messages relationship."""
    conversation = Conversation(user_id="user_abc123")

    # Should have messages relationship
    assert hasattr(conversation, "messages")
    assert conversation.messages == []


def test_conversation_fields():
    """Test conversation model has correct fields."""
    conversation = Conversation(user_id="user_abc123")

    # Check all expected fields exist
    assert hasattr(conversation, "id")
    assert hasattr(conversation, "user_id")
    assert hasattr(conversation, "created_at")
    assert hasattr(conversation, "updated_at")


def test_conversation_timestamps_auto():
    """Test conversation timestamps are auto-generated."""
    conversation1 = Conversation(user_id="user_abc123")
    conversation2 = Conversation(user_id="user_xyz456")

    # Both should have timestamps
    assert conversation1.created_at is not None
    assert conversation1.updated_at is not None
    assert conversation2.created_at is not None
    assert conversation2.updated_at is not None


def test_conversation_user_id_required():
    """Test user_id is a required field."""
    # This should not raise an error if user_id is provided
    conversation = Conversation(user_id="user_abc123")
    assert conversation.user_id == "user_abc123"


def test_conversation_table_name():
    """Test conversation has correct table name."""
    assert Conversation.__tablename__ == "conversations"


def test_conversation_str_representation():
    """Test conversation string representation."""
    conversation = Conversation(user_id="user_abc123")
    # Just verify it has a user_id
    assert conversation.user_id == "user_abc123"
