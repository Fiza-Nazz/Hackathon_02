"""
MCP Tool: update_task

Updates a task's title and/or description for a user via the Main Backend API.
"""

from typing import Dict, Any, Optional
import requests
import os
from backend.mcp_server.schemas import UpdateTaskInput, success_response, error_response, ErrorCode

MAIN_BACKEND_URL = os.getenv("MAIN_BACKEND_URL", "http://localhost:8001")


def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    auth_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update a task's title and/or description for a user.

    Args:
        user_id: User identifier (String)
        task_id: Task identifier to update
        title: New task title (optional)
        description: New task description (optional)
        auth_token: Bearer token for authentication

    Returns:
        Dict with success, data, or error
    """
    # Validate input
    if not user_id and user_id != 0:
        return error_response(
            ErrorCode.INVALID_INPUT,
            "User ID is required"
        )

    if not task_id or task_id <= 0:
        return error_response(
            ErrorCode.INVALID_INPUT,
            "Task ID must be a positive integer"
        )

    # At least one field must be provided
    if title is None and description is None:
        return error_response(
            ErrorCode.INVALID_INPUT,
            "At least one field (title or description) must be provided"
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

            if title is not None:
                db_task.title = title
            if description is not None:
                db_task.description = description
                
            session.add(db_task)
            session.commit()
            session.refresh(db_task)
            
            return success_response({
                "task_id": db_task.id,
                "status": "updated",
                "title": db_task.title
            })

    except Exception as e:
        print(f"Neural Link error in update_task: {e}")

        return error_response(
            ErrorCode.DATABASE_ERROR,
            f"Failed to update task via Neural Link: {str(e)}"
        )
