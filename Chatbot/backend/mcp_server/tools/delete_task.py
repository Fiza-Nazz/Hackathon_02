"""
MCP Tool: delete_task

Deletes a task for a user.
"""

from typing import Dict, Any
import requests
import os
from backend.mcp_server.schemas import DeleteTaskInput, success_response, error_response, ErrorCode

MAIN_BACKEND_URL = os.getenv("MAIN_BACKEND_URL", "http://localhost:8001")


def delete_task(user_id: str, task_id: int, auth_token: str = None) -> Dict[str, Any]:
    """
    Delete a task for a user.

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
    
    # Ensure user_id is a string for consistent handling
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

    # Delete task directly via SQLModel (Neural Link Tier)
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

            session.delete(db_task)
            session.commit()
            
            return success_response({
                "task_id": task_id,
                "status": "deleted"
            })

    except Exception as e:
        print(f"Neural Link error in delete_task: {e}")

        return error_response(
            ErrorCode.DATABASE_ERROR,
            f"Failed to delete task via Neural Link: {str(e)}"
        )
