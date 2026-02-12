"""
MCP Tool: set_due_date

Sets due date for a task.
"""

from typing import Dict, Any
from backend.mcp_server.schemas import success_response, error_response, ErrorCode

def set_due_date(user_id: str, task_id: int, due_date: str, auth_token: str = None) -> Dict[str, Any]:
    """
    Set due date for a task.

    Args:
        user_id: User identifier
        task_id: Task ID to update
        due_date: Due date in ISO format (YYYY-MM-DD HH:MM:SS)

    Returns:
        Dict with success, data, or error
    """
    try:
        from datetime import datetime
        from backend.db import get_engine
        from backend.models import Task, Reminder
        from sqlmodel import Session, select
        
        # Parse due date
        try:
            due_date_obj = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        except:
            return error_response(ErrorCode.INVALID_INPUT, "Invalid date format. Use YYYY-MM-DD HH:MM:SS")
        
        with Session(get_engine()) as session:
            stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            task = session.exec(stmt).first()
            
            if not task:
                return error_response(ErrorCode.NOT_FOUND, "Task not found")
            
            old_due_date = task.due_date
            task.due_date = due_date_obj
            session.add(task)
            
            # Create reminder (1 hour before due date)
            from datetime import timedelta
            remind_at = due_date_obj - timedelta(hours=1)
            if remind_at > datetime.utcnow():
                reminder = Reminder(
                    task_id=task_id,
                    user_id=user_id,
                    remind_at=remind_at,
                    message=f"Task '{task.title}' is due in 1 hour"
                )
                session.add(reminder)
            
            session.commit()
            
            return success_response({
                "task_id": task_id,
                "old_due_date": old_due_date.isoformat() if old_due_date else None,
                "new_due_date": due_date_obj.isoformat(),
                "reminder_set": remind_at > datetime.utcnow(),
                "status": "due_date_updated"
            })

    except Exception as e:
        return error_response(ErrorCode.DATABASE_ERROR, f"Due date update failed: {str(e)}")