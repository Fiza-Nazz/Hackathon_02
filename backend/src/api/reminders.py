from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import datetime
from ..models import Reminder, ReminderCreate, User, Task
from ..database.database import get_session
from ..api.deps import get_current_user

router = APIRouter()

@router.get("/")
def get_user_reminders(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all reminders for current user."""
    query = select(Reminder).where(Reminder.user_id == current_user.id).order_by(Reminder.remind_at.asc())
    reminders = session.exec(query).all()
    return reminders

@router.post("/")
def create_reminder(
    reminder: ReminderCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new reminder."""
    # Verify task exists and belongs to user
    task = session.exec(
        select(Task).where(Task.id == reminder.task_id, Task.user_id == current_user.id)
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_reminder = Reminder(
        task_id=reminder.task_id,
        user_id=current_user.id,
        remind_at=reminder.remind_at,
        reminder_type=reminder.reminder_type,
        message=reminder.message
    )
    session.add(db_reminder)
    session.commit()
    session.refresh(db_reminder)
    return db_reminder

@router.delete("/{reminder_id}")
def delete_reminder(
    reminder_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a reminder."""
    reminder = session.exec(
        select(Reminder).where(Reminder.id == reminder_id, Reminder.user_id == current_user.id)
    ).first()
    
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    session.delete(reminder)
    session.commit()
    return {"message": "Reminder deleted successfully"}