"""
MCP Tool: update_task

Updates a task's title and/or description for a user via the Main Backend API.
"""

from typing import Dict, Any, Optional
import requests
import os
from backend.mcp_server.schemas import UpdateTaskInput, success_response, error_response, ErrorCode

MAIN_BACKEND_URL = os.getenv("MAIN_BACKEND_URL", "http://127.0.0.1:8000")


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

    # Prepare payload
    payload = {}
    if title is not None:
        payload["title"] = title.strip()
    if description is not None:
        payload["description"] = description.strip()

    # Hit the Main Backend API
    try:
        response = requests.put(
            f"{MAIN_BACKEND_URL}/api/tasks/{task_id}",
            json=payload,
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=5
        )
        
        if response.status_code == 200:
            task_data = response.json()
            return success_response({
                "task_id": task_data.get("id"),
                "status": "updated",
                "title": task_data.get("title")
            })
        elif response.status_code == 404:
            return error_response(ErrorCode.NOT_FOUND, "Task not found")
        else:
            return error_response(
                ErrorCode.DATABASE_ERROR,
                f"Backend API error: {response.status_code}"
            )

    except Exception as e:
        print(f"API error in update_task: {e}")
        return error_response(
            ErrorCode.DATABASE_ERROR,
            "Failed to update task"
        )
