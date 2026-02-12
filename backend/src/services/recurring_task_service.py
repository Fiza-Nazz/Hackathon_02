"""
Recurring Task Service - Handles automatic creation of recurring tasks
"""

import logging
from datetime import datetime, timedelta
from typing import Optional
from enum import Enum

logger = logging.getLogger(__name__)


class RecurrencePattern(str, Enum):
    """Recurrence patterns for tasks"""
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class RecurringTaskService:
    """Service for managing recurring tasks"""
    
    @staticmethod
    def calculate_next_due_date(
        current_due_date: datetime,
        pattern: RecurrencePattern
    ) -> datetime:
        """Calculate next due date based on recurrence pattern"""
        
        if pattern == RecurrencePattern.DAILY:
            return current_due_date + timedelta(days=1)
        
        elif pattern == RecurrencePattern.WEEKLY:
            return current_due_date + timedelta(weeks=1)
        
        elif pattern == RecurrencePattern.BIWEEKLY:
            return current_due_date + timedelta(weeks=2)
        
        elif pattern == RecurrencePattern.MONTHLY:
            # Handle month-end edge cases
            if current_due_date.month == 12:
                return current_due_date.replace(year=current_due_date.year + 1, month=1)
            else:
                return current_due_date.replace(month=current_due_date.month + 1)
        
        elif pattern == RecurrencePattern.QUARTERLY:
            # Add 3 months
            month = current_due_date.month + 3
            year = current_due_date.year
            if month > 12:
                month -= 12
                year += 1
            return current_due_date.replace(year=year, month=month)
        
        elif pattern == RecurrencePattern.YEARLY:
            return current_due_date.replace(year=current_due_date.year + 1)
        
        else:
            logger.warning(f"⚠️ Unknown recurrence pattern: {pattern}")
            return current_due_date + timedelta(days=1)
    
    @staticmethod
    def should_create_next_occurrence(
        current_due_date: datetime,
        pattern: RecurrencePattern,
        last_created_date: Optional[datetime] = None
    ) -> bool:
        """Check if next occurrence should be created"""
        
        next_due_date = RecurringTaskService.calculate_next_due_date(current_due_date, pattern)
        
        # Create next occurrence if it's in the future
        if next_due_date > datetime.utcnow():
            return True
        
        return False
    
    @staticmethod
    def get_recurrence_description(pattern: RecurrencePattern) -> str:
        """Get human-readable description of recurrence pattern"""
        descriptions = {
            RecurrencePattern.DAILY: "Every day",
            RecurrencePattern.WEEKLY: "Every week",
            RecurrencePattern.BIWEEKLY: "Every 2 weeks",
            RecurrencePattern.MONTHLY: "Every month",
            RecurrencePattern.QUARTERLY: "Every 3 months",
            RecurrencePattern.YEARLY: "Every year",
        }
        return descriptions.get(pattern, "Unknown pattern")


class RecurringTaskProcessor:
    """Process recurring tasks and create new occurrences"""
    
    def __init__(self):
        self.service = RecurringTaskService()
    
    async def process_completed_task(
        self,
        task_id: int,
        task_title: str,
        user_id: str,
        current_due_date: datetime,
        recurrence_pattern: Optional[str] = None
    ) -> Optional[dict]:
        """Process completed task and create next occurrence if recurring"""
        
        if not recurrence_pattern:
            logger.debug(f"Task {task_id} is not recurring")
            return None
        
        try:
            pattern = RecurrencePattern(recurrence_pattern)
        except ValueError:
            logger.error(f"❌ Invalid recurrence pattern: {recurrence_pattern}")
            return None
        
        # Calculate next due date
        next_due_date = self.service.calculate_next_due_date(current_due_date, pattern)
        
        # Create new task data
        new_task_data = {
            "title": task_title,
            "user_id": user_id,
            "due_date": next_due_date,
            "is_recurring": True,
            "recurring_pattern": recurrence_pattern,
            "parent_task_id": task_id,
            "description": f"Recurring: {self.service.get_recurrence_description(pattern)}"
        }
        
        logger.info(f"✅ Created next occurrence for recurring task {task_id}")
        logger.info(f"   Next due date: {next_due_date}")
        
        return new_task_data
    
    async def get_upcoming_recurring_tasks(
        self,
        user_id: str,
        days_ahead: int = 7
    ) -> list:
        """Get upcoming recurring tasks for a user"""
        # This would query the database for recurring tasks
        # Implementation depends on database setup
        logger.info(f"Fetching upcoming recurring tasks for user {user_id} (next {days_ahead} days)")
        return []


# Global recurring task service instance
_recurring_task_service: Optional[RecurringTaskProcessor] = None


def get_recurring_task_service() -> RecurringTaskProcessor:
    """Get or create recurring task service instance"""
    global _recurring_task_service
    if _recurring_task_service is None:
        _recurring_task_service = RecurringTaskProcessor()
    return _recurring_task_service
