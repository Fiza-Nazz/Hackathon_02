"""
MCP Tool: add_task

Creates a new task for a user with title and optional description.
"""

from typing import Dict, Any
import requests
import os
from backend.mcp_server.schemas import AddTaskInput, success_response, error_response, ErrorCode

MAIN_BACKEND_URL = os.getenv("MAIN_BACKEND_URL", "http://127.0.0.1:8000")
print(f"DEBUG: add_task using backend: {MAIN_BACKEND_URL}")


def add_task(user_id: str, title: str, description: str = None, auth_token: str = None) -> Dict[str, Any]:
    """
    Create a new task for a user.

    Args:
        user_id: User identifier (String)
        title: Task title (1-255 characters, required)
        description: Optional task description (0-1000 characters)

    Returns:
        Dict with success, data, or error
    """
    # Validate input
    if not user_id and user_id != 0:
        return error_response(
            ErrorCode.INVALID_INPUT,
            "User ID is required"
        )

    if not title or not title.strip():
        return error_response(
            ErrorCode.INVALID_INPUT,
            "Title must be between 1 and 200 characters"
        )

    title = title.strip()

    if len(title) > 200:
        return error_response(
            ErrorCode.INVALID_INPUT,
            "Title exceeds 200 character limit"
        )

    if description is not None:
        description = description.strip()
        if len(description) > 1000:
            return error_response(
                ErrorCode.INVALID_INPUT,
                "Description exceeds 1000 character limit"
            )

    # Create task via main backend API
    try:
        payload = {
            "title": title,
            "description": description or "",
            "completed": False,
            "priority": 1,
            "category": "General"
        }
        
        response = requests.post(
            f"{MAIN_BACKEND_URL}/api/tasks/",
            json=payload,
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=5
        )
        
        if response.status_code == 201 or response.status_code == 200:
            task_data = response.json()
            return success_response({
                "task_id": task_data.get("id"),
                "status": "created",
                "title": task_data.get("title")
            })
        else:
            return error_response(
                ErrorCode.DATABASE_ERROR,
                f"Backend API error: {response.status_code} - {response.text}"
            )

    except Exception as e:
        import traceback
        print(f"DEBUG: add_task failed for user_id={user_id}")
        print(traceback.format_exc())

        return error_response(
            ErrorCode.DATABASE_ERROR,
            f"API request error: {str(e)}"
        )
