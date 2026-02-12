"""
Event Handlers for Phase V Features
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any
from .event_bus import Event, TaskEvents, ReminderEvents

async def handle_task_created(event: Event):
    """Handle task creation events"""
    if event.event_type != TaskEvents.CREATED:
        return
    
    print(f"🎯 Handling task created: {event.data.get('title', 'Unknown')}")
    
    # Check if task has due date - schedule reminder
    if event.data.get('due_date'):
        due_date = datetime.fromisoformat(event.data['due_date'].replace('Z', '+00:00'))
        
        # Schedule reminder 1 hour before due date
        remind_at = due_date - timedelta(hours=1)
        
        if remind_at > datetime.utcnow():
            print(f"⏰ Scheduling reminder for task {event.aggregate_id} at {remind_at}")
            # In a real system, this would use a job scheduler
            # For demo, we'll just log it
    
    # Check if task is recurring
    if event.data.get('recurring_pattern'):
        print(f"🔄 Task {event.aggregate_id} is recurring: {event.data['recurring_pattern']}")

async def handle_task_completed(event: Event):
    """Handle task completion events"""
    if event.event_type != TaskEvents.COMPLETED:
        return
    
    print(f"✅ Handling task completed: {event.data.get('title', 'Unknown')}")
    
    # Check if task is recurring - create next occurrence
    if event.data.get('recurring_pattern'):
        pattern = event.data['recurring_pattern']
        print(f"🔄 Creating next occurrence for recurring task: {pattern}")
        
        # Calculate next due date based on pattern
        next_due_date = calculate_next_due_date(
            datetime.utcnow(), 
            pattern
        )
        
        print(f"📅 Next occurrence scheduled for: {next_due_date}")
        
        # In a real system, this would create a new task
        # For demo, we'll just log it

async def handle_reminder_due(event: Event):
    """Handle reminder due events"""
    if event.event_type != ReminderEvents.SCHEDULED:
        return
    
    print(f"🔔 Processing reminder for task: {event.data.get('title', 'Unknown')}")
    
    # In a real system, this would send email/push notification
    # For demo, we'll simulate notification
    await send_notification(
        user_id=event.user_id,
        title=event.data.get('title', 'Task Reminder'),
        message=f"Task '{event.data.get('title')}' is due soon!"
    )

def calculate_next_due_date(current_date: datetime, pattern: str) -> datetime:
    """Calculate next due date based on recurring pattern"""
    if pattern == 'daily':
        return current_date + timedelta(days=1)
    elif pattern == 'weekly':
        return current_date + timedelta(weeks=1)
    elif pattern == 'monthly':
        return current_date + timedelta(days=30)  # Simplified
    elif pattern == 'yearly':
        return current_date + timedelta(days=365)  # Simplified
    else:
        return current_date + timedelta(days=1)  # Default to daily

async def send_notification(user_id: str, title: str, message: str):
    """Send notification to user"""
    print(f"📧 NOTIFICATION for user {user_id}:")
    print(f"   Title: {title}")
    print(f"   Message: {message}")
    
    # In a real system, this would:
    # 1. Send email via SMTP
    # 2. Send push notification
    # 3. Store in notification table
    
    # For demo, we'll just simulate delay
    await asyncio.sleep(0.1)