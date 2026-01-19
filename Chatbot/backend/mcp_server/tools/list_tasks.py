"""
MCP Tool: list_tasks

Lists tasks for a user with optional status filtering.
"""

from typing import Dict, Any
import requests
import os
from backend.mcp_server.schemas import ListTasksInput, success_response, error_response, ErrorCode

MAIN_BACKEND_URL = os.getenv("MAIN_BACKEND_URL", "http://127.0.0.1:8000")
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

    # Query tasks via main backend API
    try:
        response = requests.get(
            f"{MAIN_BACKEND_URL}/api/tasks/",
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=5
        )
        
        if response.status_code == 200:
            all_tasks = response.json()
            
            # Apply status filter
            if status == "pending":
                tasks_data = [t for t in all_tasks if not t.get("completed", False)]
            elif status == "completed":
                tasks_data = [t for t in all_tasks if t.get("completed", False)]
            else:
                tasks_data = all_tasks

            return success_response({
                "tasks": tasks_data,
                "total": len(tasks_data)
            })
        else:
            return error_response(
                ErrorCode.DATABASE_ERROR,
                f"Backend API error: {response.status_code}"
            )

    except Exception as e:
        print(f"API error in list_tasks: {e}")

        return error_response(
            ErrorCode.DATABASE_ERROR,
            "Failed to retrieve tasks"
        )
