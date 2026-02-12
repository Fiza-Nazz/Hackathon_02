"""
MCP Tool: set_priority

Sets the priority of a task (high, medium, low).
"""

from typing import Dict, Any
from backend.mcp_server.schemas import success_response, error_response, ErrorCode

def set_priority(user_id: str, task_id: int, priority: str, auth_token: str = None) -> Dict[str, Any]:
    """
    Set task priority.

    Args:
        user_id: User identifier
        task_id: Task ID to update
        priority: Priority level (high, medium, low)

    Returns:
        Dict with success, data, or error
    """
    if priority not in ["high", "medium", "low"]:
        return error_response(
            ErrorCode.INVALID_INPUT,
            "Priority must be 'high', 'medium', or 'low'"
        )

    try:
        from backend.db import get_engine
        from backend.models import Task
        from sqlmodel import Session, select
        
        with Session(get_engine()) as session:
            stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            task = session.exec(stmt).first()
            
            if not task:
                return error_response(ErrorCode.NOT_FOUND, "Task not found")
            
            old_priority = task.priority
            task.priority = priority
            session.add(task)
            session.commit()
            
            return success_response({
                "task_id": task_id,
                "old_priority": old_priority,
                "new_priority": priority,
                "status": "priority_updated"
            })

    except Exception as e:
        return error_response(ErrorCode.DATABASE_ERROR, f"Priority update failed: {str(e)}")