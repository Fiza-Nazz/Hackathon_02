"""
Integration tests for message persistence.
"""

import pytest
from sqlmodel import Session, create_engine
from datetime import datetime, timedelta
from backend.models.conversation import Conversation
from backend.models.message import Message


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


def test_message_persistence_across_sessions(session, test_engine):
    """Test messages persist across different sessions."""
    # Create conversation and messages in session 1
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

    # Start new session and verify messages exist
    with Session(test_engine) as new_session:
        from sqlmodel import select
        messages = new_session.exec(select(Message).where(
            Message.conversation_id == conv_id
        )).all()

        assert len(messages) == 3
        assert messages[0].content == "Message 1"
        assert messages[1].content == "Message 2"
        assert messages[2].content == "Message 3"


def test_cross_session_retrieval_chronological(session, test_engine):
    """Test messages maintain chronological order across sessions."""
    # Setup: Create conversation and messages
    conversation = Conversation(user_id="user_abc123")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    conv_id = conversation.id
    base_time = datetime.utcnow()

    # Add messages with specific timestamps
    for i in range(3):
        message = Message(
            conversation_id=conv_id,
            user_id="user_abc123",
            role="user",
            content=f"Message {i+1}"
        )
        message.created_at = base_time + timedelta(seconds=i * 10)
        session.add(message)

    session.commit()

    # New session: Retrieve and verify order
    with Session(test_engine) as new_session:
        from sqlmodel import select
        messages = new_session.exec(
            select(Message).where(
                Message.conversation_id == conv_id
            ).order_by(Message.created_at)
        ).all()

        assert len(messages) == 3

        # Verify content and timestamps in order
        for i, message in enumerate(messages):
            assert message.content == f"Message {i+1}"
            assert message.created_at == base_time + timedelta(seconds=i * 10)


def test_user_isolation_in_messages(session, test_engine):
    """Test messages are isolated by user_id."""
    # Create conversations for different users
    user1_conv = Conversation(user_id="user_abc123")
    user2_conv = Conversation(user_id="user_xyz456")
    session.add(user1_conv)
    session.add(user2_conv)
    session.commit()
    session.refresh(user1_conv)
    session.refresh(user2_conv)

    # Add messages for user1
    msg1 = Message(
        conversation_id=user1_conv.id,
        user_id="user_abc123",
        role="user",
        content="User1 message"
    )
    session.add(msg1)

    # Add messages for user2
    msg2 = Message(
        conversation_id=user2_conv.id,
        user_id="user_xyz456",
        role="user",
        content="User2 message"
    )
    session.add(msg2)

    session.commit()

    # Verify isolation
    with Session(test_engine) as new_session:
        from sqlmodel import select
        user1_messages = new_session.exec(select(Message).where(
            Message.user_id == "user_abc123"
        )).all()
        user2_messages = new_session.exec(select(Message).where(
            Message.user_id == "user_xyz456"
        )).all()

        assert len(user1_messages) == 1
        assert len(user2_messages) == 1
        assert user1_messages[0].content == "User1 message"
        assert user2_messages[0].content == "User2 message"


def test_message_survives_server_restart_simulation(session, test_engine):
    """Test messages survive simulated server restart (session close/reopen)."""
    # Create conversation and messages
    conversation = Conversation(user_id="user_abc123")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    conv_id = conversation.id

    for i in range(5):
        message = Message(
            conversation_id=conv_id,
            user_id="user_abc123",
            role="user" if i % 2 == 0 else "assistant",
            content=f"Message {i+1}"
        )
        session.add(message)

    session.commit()

    # Simulate server restart: close and reopen session
    session.close()

    # New session
    with Session(test_engine) as new_session:
        from sqlmodel import select
        messages = new_session.exec(
            select(Message).where(
                Message.conversation_id == conv_id
            ).order_by(Message.created_at)
        ).all()

        # Verify all messages survived
        assert len(messages) == 5
        for i, message in enumerate(messages):
            assert message.content == f"Message {i+1}"


def test_message_tool_calls_persistence(session, test_engine):
    """Test tool_calls JSONB data persists correctly."""
    # Create conversation
    conversation = Conversation(user_id="user_abc123")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    # Create message with tool calls
    tool_calls = {
        "name": "add_task",
        "parameters": {"title": "Buy groceries", "description": "Milk, eggs"},
        "result": {"task_id": 42, "status": "created"}
    }

    message = Message(
        conversation_id=conversation.id,
        user_id="user_abc123",
        role="assistant",
        content="I've created that task for you.",
        tool_calls=tool_calls
    )

    session.add(message)
    session.commit()

    # Retrieve and verify tool_calls
    with Session(test_engine) as new_session:
        retrieved = new_session.get(Message, message.id)
        assert retrieved is not None
        assert retrieved.tool_calls is not None
        assert retrieved.tool_calls["name"] == "add_task"
        assert retrieved.tool_calls["parameters"]["title"] == "Buy groceries"
        assert retrieved.tool_calls["result"]["task_id"] == 42


def test_empty_conversation_start(session):
    """Test a conversation starts empty (no messages yet)."""
    # Create conversation
    conversation = Conversation(user_id="user_abc123")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    # Verify no messages yet
    from sqlmodel import select
    messages = session.exec(select(Message).where(
        Message.conversation_id == conversation.id
    )).all()

    assert len(messages) == 0


def test_message_roles_persist(session, test_engine):
    """Test message roles persist correctly."""
    # Create conversation
    conversation = Conversation(user_id="user_abc123")
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    # Add messages with different roles
    user_msg = Message(
        conversation_id=conversation.id,
        user_id="user_abc123",
        role="user",
        content="User message"
    )
    assistant_msg = Message(
        conversation_id=conversation.id,
        user_id="user_abc123",
        role="assistant",
        content="Assistant response"
    )

    session.add(user_msg)
    session.add(assistant_msg)
    session.commit()

    # Retrieve and verify roles
    with Session(test_engine) as new_session:
        from sqlmodel import select
        messages = new_session.exec(
            select(Message).where(
                Message.conversation_id == conversation.id
            ).order_by(Message.created_at)
        ).all()

        assert len(messages) == 2
        assert messages[0].role == "user"
        assert messages[1].role == "assistant"
