"""
Event schemas for Phase 5 Event-Driven Architecture
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


class BaseEvent(BaseModel):
    """Base event schema for all events"""
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: str
    aggregate_id: str
    user_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: int = 1
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TaskEventData(BaseModel):
    """Base task event data"""
    task_id: int
    title: str
    user_id: str


class TaskCreatedEvent(BaseEvent):
    """Task created event"""
    event_type: str = "task.created"
    data: Dict[str, Any]
    
    class Data(TaskEventData):
        description: Optional[str] = None
        priority: str = "medium"
        category: str = "General"
        tags: List[str] = Field(default_factory=list)
        due_date: Optional[datetime] = None
        is_recurring: bool = False
        recurring_pattern: Optional[str] = None


class TaskUpdatedEvent(BaseEvent):
    """Task updated event"""
    event_type: str = "task.updated"
    data: Dict[str, Any]
    
    class Data(TaskEventData):
        old_values: Dict[str, Any]
        new_values: Dict[str, Any]
        updated_fields: List[str]


class TaskCompletedEvent(BaseEvent):
    """Task completed event"""
    event_type: str = "task.completed"
    data: Dict[str, Any]
    
    class Data(TaskEventData):
        completed_at: datetime
        was_overdue: bool = False
        completion_time_minutes: Optional[int] = None


class TaskDeletedEvent(BaseEvent):
    """Task deleted event"""
    event_type: str = "task.deleted"
    data: Dict[str, Any]
    
    class Data(TaskEventData):
        deleted_at: datetime
        was_completed: bool


class TaskPriorityChangedEvent(BaseEvent):
    """Task priority changed event"""
    event_type: str = "task.priority_changed"
    data: Dict[str, Any]
    
    class Data(TaskEventData):
        old_priority: str
        new_priority: str
        changed_by: str


class TaskTagsUpdatedEvent(BaseEvent):
    """Task tags updated event"""
    event_type: str = "task.tags_updated"
    data: Dict[str, Any]
    
    class Data(TaskEventData):
        added_tags: List[str] = Field(default_factory=list)
        removed_tags: List[str] = Field(default_factory=list)
        current_tags: List[str] = Field(default_factory=list)


class TaskDueDateSetEvent(BaseEvent):
    """Task due date set event"""
    event_type: str = "task.due_date_set"
    data: Dict[str, Any]
    
    class Data(TaskEventData):
        old_due_date: Optional[datetime] = None
        new_due_date: datetime
        reminder_created: bool = False


class TaskOverdueEvent(BaseEvent):
    """Task became overdue event"""
    event_type: str = "task.overdue"
    data: Dict[str, Any]
    
    class Data(TaskEventData):
        due_date: datetime
        overdue_minutes: int
        priority: str


class ReminderTriggeredEvent(BaseEvent):
    """Reminder triggered event"""
    event_type: str = "reminder.triggered"
    data: Dict[str, Any]
    
    class Data(BaseModel):
        reminder_id: int
        task_id: int
        user_id: str
        reminder_type: str
        message: str
        scheduled_at: datetime
        triggered_at: datetime


class RecurringTaskCreatedEvent(BaseEvent):
    """Recurring task instance created event"""
    event_type: str = "recurring_task.created"
    data: Dict[str, Any]
    
    class Data(TaskEventData):
        parent_task_id: int
        recurring_pattern: str
        occurrence_number: int
        next_due_date: Optional[datetime] = None


# Event type mapping for easy access
EVENT_TYPES = {
    "task.created": TaskCreatedEvent,
    "task.updated": TaskUpdatedEvent,
    "task.completed": TaskCompletedEvent,
    "task.deleted": TaskDeletedEvent,
    "task.priority_changed": TaskPriorityChangedEvent,
    "task.tags_updated": TaskTagsUpdatedEvent,
    "task.due_date_set": TaskDueDateSetEvent,
    "task.overdue": TaskOverdueEvent,
    "reminder.triggered": ReminderTriggeredEvent,
    "recurring_task.created": RecurringTaskCreatedEvent,
}


def create_event(event_type: str, aggregate_id: str, user_id: str, data: Dict[str, Any], **kwargs) -> BaseEvent:
    """Factory function to create events"""
    event_class = EVENT_TYPES.get(event_type, BaseEvent)
    return event_class(
        event_type=event_type,
        aggregate_id=aggregate_id,
        user_id=user_id,
        data=data,
        **kwargs
    )