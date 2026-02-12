"""
MCP Tool: list_tasks

Lists tasks for a user with optional status filtering.
"""

from typing import Dict, Any
import requests
import os
from backend.mcp_server.schemas import ListTasksInput, success_response, error_response, ErrorCode

MAIN_BACKEND_URL = os.getenv("MAIN_BACKEND_URL", "http://localhost:8001")
print(f"DEBUG: list_tasks using backend: {MAIN_BACKEND_URL}")


def list_tasks(user_id: str, status: str = "all", auth_token: str = None) -> Dict[str, Any]:
    """
    List tasks for a user with optional status filtering.

    Args:
        user_id: User identifier (String)
        status: Filter by status ('all', 'pending', 'completed'). Default is 'all'

    Returns:
        Dict with success, data (tasks array), or error
    """
    # Validate input
    if user_id is None:
        return error_response(
            ErrorCode.INVALID_INPUT,
            "User ID is required"
        )
    status = status.strip().lower() if status else "all"

    # Validate status parameter
    valid_statuses = ["all", "pending", "completed"]
    if status not in valid_statuses:
        status = "all"  # Default to 'all' if invalid

    # Query tasks directly via SQLModel (Neural Link Tier)
    try:
        from backend.db import get_engine
        from backend.models import Task
        from sqlmodel import Session, select
        
        with Session(get_engine()) as session:
            statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
            all_tasks = session.exec(statement).all()
            
            # Apply status filter
            if status == "pending":
                tasks_data = [t for t in all_tasks if not t.completed]
            elif status == "completed":
                tasks_data = [t for t in all_tasks if t.completed]
            else:
                tasks_data = all_tasks

            # Format for response
            formatted_tasks = []
            for t in tasks_data:
                formatted_tasks.append({
                    "id": t.id,
                    "title": t.title,
                    "completed": t.completed,
                    "created_at": str(t.created_at)
                })

            return success_response({
                "tasks": formatted_tasks,
                "total": len(formatted_tasks)
            })

    except Exception as e:
        print(f"Neural Link error in list_tasks: {e}")

        return error_response(
            ErrorCode.DATABASE_ERROR,
            f"Failed to retrieve tasks via Neural Link: {str(e)}"
        )
