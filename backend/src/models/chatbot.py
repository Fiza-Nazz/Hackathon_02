from datetime import datetime
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, ForeignKey, JSON, Text as sa_Text

if TYPE_CHECKING:
    from .user import User

class Conversation(SQLModel, table=True):
    """
    Conversation model for storing chat sessions.
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(sa_column=Column(String, ForeignKey("auth_user.id"), index=True))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")
    user: Optional["User"] = Relationship(back_populates="conversations")

class Message(SQLModel, table=True):
    """
    Message model for storing chat messages.
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(index=True, foreign_key="conversations.id")
    user_id: str = Field(sa_column=Column(String, ForeignKey("auth_user.id"), index=True))
    role: str = Field(max_length=20)
    content: str = Field(sa_column=Column("content", sa_Text))
    tool_calls: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
