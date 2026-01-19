"""
User model for SQLModel.

Represents application user with authentication (managed by Better Auth).
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .conversation import Conversation
    from .task import Task


class User(SQLModel, table=True):
    __tablename__ = "auth_user"  # Correct table name for Better Auth

    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    emailVerified: bool = Field(default=False)
    name: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversations: list["Conversation"] = Relationship(back_populates="user")
    tasks: list["Task"] = Relationship(back_populates="user")
