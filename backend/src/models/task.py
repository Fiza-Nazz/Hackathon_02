from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship
from pydantic import validator


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RecurringPattern(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    category: Optional[str] = Field(default="General", max_length=50)
    due_date: Optional[datetime] = Field(default=None)
    is_recurring: bool = Field(default=False)
    recurring_pattern: Optional[RecurringPattern] = Field(default=None)
    recurring_interval: int = Field(default=1, ge=1)
    parent_task_id: Optional[int] = Field(default=None, foreign_key="tasks.id")

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

    @validator('recurring_pattern')
    def validate_recurring_pattern(cls, v, values):
        if values.get('is_recurring') and not v:
            raise ValueError('Recurring pattern is required for recurring tasks')
        return v


class Task(TaskBase, table=True):
    """
    Task model representing a todo item with advanced features.
    """
    __tablename__ = "tasks"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="auth_user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="tasks")
    tags: List["TaskTag"] = Relationship(back_populates="task")
    reminders: List["Reminder"] = Relationship(back_populates="task")
    parent_task: Optional["Task"] = Relationship(
        back_populates="child_tasks",
        sa_relationship_kwargs={"remote_side": "Task.id"}
    )
    child_tasks: List["Task"] = Relationship(back_populates="parent_task")


class TaskTag(SQLModel, table=True):
    """
    Many-to-many relationship between tasks and tags.
    """
    __tablename__ = "task_tags"
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="tasks.id")
    tag_name: str = Field(max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    task: Optional[Task] = Relationship(back_populates="tags")
    tag: Optional["Tag"] = Relationship(back_populates="task_tags")


class Tag(SQLModel, table=True):
    """
    Tag model for categorizing tasks.
    """
    __tablename__ = "tags"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True)
    color: str = Field(default="#3B82F6", max_length=7)
    user_id: str = Field(foreign_key="auth_user.id")
    usage_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    task_tags: List[TaskTag] = Relationship(back_populates="tag")


class Reminder(SQLModel, table=True):
    """
    Reminder model for scheduled notifications.
    """
    __tablename__ = "reminders"
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="tasks.id")
    user_id: str = Field(foreign_key="auth_user.id")
    remind_at: datetime
    reminder_type: str = Field(default="due_date")
    status: str = Field(default="pending")
    message: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    task: Optional[Task] = Relationship(back_populates="reminders")


class AuditLog(SQLModel, table=True):
    """
    Audit log for tracking all task operations.
    """
    __tablename__ = "audit_log"
    id: Optional[int] = Field(default=None, primary_key=True)
    event_type: str = Field(max_length=50)
    aggregate_id: str = Field(max_length=255)
    user_id: str = Field(max_length=255)
    event_data: str = Field(description="JSON string of event data")
    correlation_id: Optional[str] = Field(default=None)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# API Schemas
class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    """
    tags: Optional[List[str]] = Field(default=[])


class TaskRead(TaskBase):
    """
    Schema for reading task data.
    """
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
    tags: List[str] = Field(default=[])


class TaskUpdate(SQLModel):
    """
    Schema for updating a task.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[TaskPriority] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurring_pattern: Optional[RecurringPattern] = None
    recurring_interval: Optional[int] = None
    tags: Optional[List[str]] = None


class TaskFilter(SQLModel):
    """
    Schema for filtering tasks.
    """
    priority: Optional[TaskPriority] = None
    completed: Optional[bool] = None
    tags: Optional[List[str]] = None
    due_date_from: Optional[datetime] = None
    due_date_to: Optional[datetime] = None
    search: Optional[str] = None
    category: Optional[str] = None


class TaskSort(str, Enum):
    CREATED_ASC = "created_asc"
    CREATED_DESC = "created_desc"
    DUE_DATE_ASC = "due_date_asc"
    DUE_DATE_DESC = "due_date_desc"
    PRIORITY_ASC = "priority_asc"
    PRIORITY_DESC = "priority_desc"
    TITLE_ASC = "title_asc"
    TITLE_DESC = "title_desc"


class RecurringTaskCreate(SQLModel):
    """
    Schema for creating recurring tasks.
    """
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    category: Optional[str] = "General"
    due_date: datetime
    recurring_pattern: RecurringPattern
    recurring_interval: int = 1
    tags: Optional[List[str]] = Field(default=[])


class ReminderCreate(SQLModel):
    """
    Schema for creating reminders.
    """
    task_id: int
    remind_at: datetime
    reminder_type: str = "due_date"
    message: Optional[str] = None


class TagCreate(SQLModel):
    """
    Schema for creating tags.
    """
    name: str = Field(min_length=1, max_length=50)
    color: str = Field(default="#3B82F6", regex=r"^#[0-9A-Fa-f]{6}$")


class TagRead(SQLModel):
    """
    Schema for reading tag data.
    """
    id: int
    name: str
    color: str
    usage_count: int
    created_at: datetime