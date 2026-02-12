from .user import User, UserCreate, UserRead, Account, Verification
from .task import (
    Task, TaskCreate, TaskRead, TaskUpdate, TaskTag, Tag, Reminder, AuditLog,
    TaskPriority, RecurringPattern, TaskFilter, TaskSort, RecurringTaskCreate, 
    ReminderCreate, TagCreate, TagRead
)
from .session import AuthSession
from .chatbot import Conversation, Message

# Ensure all models are registered with SQLModel
__all__ = [
    "User", "UserCreate", "UserRead", "Account", "Verification", 
    "Task", "TaskCreate", "TaskRead", "TaskUpdate", "TaskTag", "Tag", "Reminder", "AuditLog",
    "TaskPriority", "RecurringPattern", "TaskFilter", "TaskSort", "RecurringTaskCreate", 
    "ReminderCreate", "TagCreate", "TagRead",
    "AuthSession", "Conversation", "Message"
]
