from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from pydantic import validator


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: int = Field(default=1, description="1: Low, 2: Medium, 3: High")
    category: Optional[str] = Field(default="General", max_length=50)

    @validator('title')
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError('Title is required and cannot be empty')
        return v.strip()

    @validator('description')
    def validate_description(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description must be 1000 characters or less')
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        if v not in [1, 2, 3]:
            return 1
        return v


class Task(TaskBase, table=True):
    """
    Task model representing a todo item with a unique ID, title (required),
    description (optional), completion status (boolean), and user ID (foreign key).
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="auth_user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to User
    user: Optional["User"] = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    """
    pass


class TaskRead(TaskBase):
    """
    Schema for reading task data.
    """
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """
    Schema for updating a task.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[int] = None
    category: Optional[str] = None