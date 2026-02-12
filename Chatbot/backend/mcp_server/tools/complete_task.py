"""
MCP Tool: complete_task

Marks a task as completed for a user.
"""

from typing import Dict, Any
import requests
import os
from backend.mcp_server.schemas import CompleteTaskInput, success_response, error_response, ErrorCode

MAIN_BACKEND_URL = os.getenv("MAIN_BACKEND_URL", "http://localhost:8001")


def complete_task(user_id: str, task_id: int, auth_token: str = None) -> Dict[str, Any]:
    """
    Mark a task as completed for a user.

    Args:
        user_id: User identifier from JWT token
        task_id: Task identifier

    Returns:
        Dict with success, data, or error
    """
    # Validate input
    if user_id is None:
        return error_response(
            ErrorCode.INVALID_INPUT,
            "User ID is required"
        )

    user_id = str(user_id).strip()
    
    if not user_id:
        return error_response(
            ErrorCode.INVALID_INPUT,
            "User ID is required"
        )

    if not task_id or task_id <= 0:
        return error_response(
            ErrorCode.INVALID_INPUT,
            "Task ID must be a positive integer"
        )

    # Update task directly via SQLModel (Neural Link Tier)
    try:
        from backend.db import get_engine
        from backend.models import Task
        from sqlmodel import Session, select
        
        with Session(get_engine()) as session:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()
            
            if not db_task:
                return error_response(
                    ErrorCode.NOT_FOUND,
                    "Task not found on Dashboard"
                )

            db_task.completed = True
            session.add(db_task)
            session.commit()
            session.refresh(db_task)
            
            return success_response({
                "task_id": db_task.id,
                "status": "completed",
                "title": db_task.title
            })

    except Exception as e:
        print(f"Neural Link error in complete_task: {e}")

        return error_response(
            ErrorCode.DATABASE_ERROR,
            f"Failed to complete task via Neural Link: {str(e)}"
        )
