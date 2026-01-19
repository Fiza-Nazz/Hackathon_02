"""
MCP Tool: complete_task

Marks a task as completed for a user.
"""

from typing import Dict, Any
import requests
import os
from backend.mcp_server.schemas import CompleteTaskInput, success_response, error_response, ErrorCode

MAIN_BACKEND_URL = os.getenv("MAIN_BACKEND_URL", "http://127.0.0.1:8000")


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

    # Complete task via main backend API
    try:
        response = requests.patch(
            f"{MAIN_BACKEND_URL}/api/tasks/{task_id}/complete",
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=5
        )
        
        if response.status_code == 200:
            task_data = response.json()
            return success_response({
                "task_id": task_data.get("id"),
                "status": "completed",
                "title": task_data.get("title")
            })
        elif response.status_code == 404:
            return error_response(
                ErrorCode.NOT_FOUND,
                "Task not found"
            )
        else:
            return error_response(
                ErrorCode.DATABASE_ERROR,
                f"Backend API error: {response.status_code}"
            )

    except Exception as e:
        print(f"API error in complete_task: {e}")

        return error_response(
            ErrorCode.DATABASE_ERROR,
            "Failed to complete task"
        )
