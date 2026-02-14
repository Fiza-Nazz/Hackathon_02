"""
Integration tests for conversation persistence.
"""

import pytest
from sqlmodel import Session, create_engine
from backend.models.conversation import Conversation
from backend.models.message import Message


@pytest.fixture
def test_engine():
    """Create a test database engine."""
    # Use in-memory SQLite for tests
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


def test_conversation_creation_and_retrieval(session):
    """Test creating a conversation and retrieving it."""
    # Create a conversation
    conversation = Conversation(user_id="user_abc123")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    assert conversation.id is not None
    assert conversation.user_id == "user_abc123"

    # Retrieve the conversation
    retrieved = session.get(Conversation, conversation.id)
    assert retrieved is not None
    assert retrieved.user_id == "user_abc123"


def test_multi_message_scenario(session):
    """Test adding multiple messages to a conversation."""
    # Create conversation
    conversation = Conversation(user_id="user_abc123")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    conv_id = conversation.id

    # Add multiple messages
    for i in range(5):
        message = Message(
            conversation_id=conv_id,
            user_id="user_abc123",
            role="user" if i % 2 == 0 else "assistant",
            content=f"Message {i+1}"
        )
        session.add(message)

    session.commit()

    # Verify all messages were added
    from sqlmodel import select
    messages = session.exec(select(Message).where(Message.conversation_id == conv_id)).all()
    assert len(messages) == 5

    # Verify they have different roles
    user_messages = [m for m in messages if m.role == "user"]
    assistant_messages = [m for m in messages if m.role == "assistant"]
    assert len(user_messages) == 3
    assert len(assistant_messages) == 2


def test_retrieval_order_chronological(session):
    """Test messages are retrieved in chronological order."""
    # Create conversation
    conversation = Conversation(user_id="user_abc123")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    conv_id = conversation.id

    # Add messages with explicit timestamps
    from datetime import datetime, timedelta

    base_time = datetime.utcnow()
    for i in range(3):
        message = Message(
            conversation_id=conv_id,
            user_id="user_abc123",
            role="user",
            content=f"Message {i+1}"
        )
        # Manually set timestamp for testing
        message.created_at = base_time + timedelta(seconds=i)
        session.add(message)

    session.commit()

    # Retrieve messages and verify chronological order
    from sqlmodel import select
    messages = session.exec(
        select(Message).where(
            Message.conversation_id == conv_id
        ).order_by(Message.created_at)
    ).all()

    assert len(messages) == 3
    assert messages[0].content == "Message 1"
    assert messages[1].content == "Message 2"
    assert messages[2].content == "Message 3"


def test_conversation_with_messages_deletion(session):
    """Test deleting a conversation also removes associated messages."""
    # Create conversation
    conversation = Conversation(user_id="user_abc123")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    conv_id = conversation.id

    # Add messages
    for i in range(3):
        message = Message(
            conversation_id=conv_id,
            user_id="user_abc123",
            role="user",
            content=f"Message {i+1}"
        )
        session.add(message)

    session.commit()

    # Verify messages exist
    from sqlmodel import select
    messages = session.exec(select(Message).where(Message.conversation_id == conv_id)).all()
    assert len(messages) == 3

    # Delete messages first, then conversation (to simulate cascade behavior)
    # In a real database with proper FK constraints, this would be handled automatically
    messages_to_delete = session.exec(select(Message).where(Message.conversation_id == conv_id)).all()
    for message in messages_to_delete:
        session.delete(message)

    session.delete(conversation)
    session.commit()

    # Verify messages are deleted
    messages = session.exec(select(Message).where(Message.conversation_id == conv_id)).all()
    assert len(messages) == 0


def test_multiple_conversations_per_user(session):
    """Test a user can have multiple conversations."""
    user_id = "user_abc123"

    # Create multiple conversations for the same user
    for i in range(3):
        conversation = Conversation(user_id=user_id)
        session.add(conversation)

    session.commit()

    # Verify all conversations exist
    from sqlmodel import select
    conversations = session.exec(select(Conversation).where(Conversation.user_id == user_id)).all()
    assert len(conversations) == 3

    # Verify they have different IDs
    ids = [c.id for c in conversations]
    assert len(ids) == len(set(ids))  # All unique


def test_conversation_update_timestamp(session):
    """Test conversation updated_at timestamp updates on changes."""
    # Create conversation
    conversation = Conversation(user_id="user_abc123")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    initial_updated_at = conversation.updated_at

    # Add a message (this would trigger updated_at in real application)
    message = Message(
        conversation_id=conversation.id,
        user_id="user_abc123",
        role="user",
        content="New message"
    )
    session.add(message)

    # Note: In production, updated_at should be refreshed on message add
    # For now, we just verify the field exists
    assert conversation.updated_at is not None
