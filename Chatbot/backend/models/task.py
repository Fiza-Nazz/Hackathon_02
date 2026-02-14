"""
Task model for SQLModel.

Represents a todo item managed by the user.
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .user import User


from sqlalchemy import Column, String, ForeignKey

class Task(SQLModel, table=True):
    # ...
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(sa_column=Column(String, ForeignKey("auth_user.id"), index=True))
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    priority: int = Field(default=1)
    category: Optional[str] = Field(default="General", max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="tasks")
