"""
MCP Tool: delete_all_tasks

Deletes all tasks for the current user.
"""

from typing import Dict, Any
import requests
import os
from backend.mcp_server.schemas import success_response, error_response, ErrorCode

MAIN_BACKEND_URL = os.getenv("MAIN_BACKEND_URL", "http://127.0.0.1:8000")

def delete_all_tasks(user_id: str, auth_token: str = None) -> Dict[str, Any]:
    """
    Delete all tasks for the current user.
    """
    if not auth_token:
        return error_response(ErrorCode.INVALID_INPUT, "Authentication token required")

    try:
        response = requests.delete(
            f"{MAIN_BACKEND_URL}/api/tasks/delete-all",
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=5
        )
        
        if response.status_code == 200:
            return success_response(response.json())
        else:
            return error_response(
                ErrorCode.DATABASE_ERROR,
                f"Backend API error: {response.status_code} - {response.text}"
            )

    except Exception as e:
        return error_response(ErrorCode.DATABASE_ERROR, str(e))
