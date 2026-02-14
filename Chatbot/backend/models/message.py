"""
Message model for Chatbot.

Represents a single message in a conversation (user or AI assistant).
"""

from datetime import datetime
from typing import Optional, Dict, Any, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import JSON, Text as sa_Text, ForeignKey, String

if TYPE_CHECKING:
    from .conversation import Conversation


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
