"""
MCP Tool: delete_all_tasks

Deletes all tasks for the current user.
"""

from typing import Dict, Any
import os
from backend.mcp_server.schemas import success_response, error_response, ErrorCode
from backend.db import get_engine
from backend.models import Task
from sqlmodel import Session, delete

def delete_all_tasks(user_id: str) -> Dict[str, Any]:
    """
    Delete all tasks for the current user.
    """
    # Delete all tasks directly via SQLModel (Neural Link Tier)
    try:
        with Session(get_engine()) as session:
            statement = delete(Task).where(Task.user_id == user_id)
            session.execute(statement)
            session.commit()

            return success_response({
                "status": "all_deleted"
            })

    except Exception as e:
        print(f"Neural Link error in delete_all_tasks: {e}")

        return error_response(
            ErrorCode.DATABASE_ERROR,
            f"Failed to wipe Dashboard via Neural Link: {str(e)}"
        )
