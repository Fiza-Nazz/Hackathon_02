"""
MCP Tool: add_task

Creates a new task for a user with title and optional description.
"""

from typing import Dict, Any
import requests
import os
from backend.mcp_server.schemas import AddTaskInput, success_response, error_response, ErrorCode

MAIN_BACKEND_URL = os.getenv("MAIN_BACKEND_URL", "http://localhost:8001")
print(f"DEBUG: add_task using backend: {MAIN_BACKEND_URL}")


def add_task(user_id: str, title: str, description: str = None, priority: str = "medium", tags: str = None, due_date: str = None, auth_token: str = None) -> Dict[str, Any]:
    """
    Create a new task for a user with advanced features.

    Args:
        user_id: User identifier (String)
        title: Task title (1-255 characters, required)
        description: Optional task description (0-1000 characters)
        priority: Task priority (low, medium, high)
        tags: Comma-separated tags
        due_date: Due date in ISO format (YYYY-MM-DD HH:MM:SS)

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

    # Create task directly via SQLModel (Neural Link Tier)
    try:
        from backend.db import get_engine
        from backend.models import Task, TaskTag
        from sqlmodel import Session
        from datetime import datetime
        
        # Parse due date if provided
        due_date_obj = None
        if due_date:
            try:
                due_date_obj = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            except:
                pass
        
        # Parse tags
        tag_list = []
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        
        with Session(get_engine()) as session:
            db_task = Task(
                title=title,
                description=description or "",
                completed=False,
                priority=priority,
                category="General",
                due_date=due_date_obj,
                user_id=user_id
            )
            session.add(db_task)
            session.commit()
            session.refresh(db_task)
            
            # Add tags if provided
            for tag_name in tag_list:
                task_tag = TaskTag(task_id=db_task.id, tag_name=tag_name)
                session.add(task_tag)
            
            session.commit()
            
            return success_response({
                "task_id": db_task.id,
                "status": "created",
                "title": db_task.title,
                "priority": db_task.priority,
                "tags": tag_list,
                "due_date": due_date_obj.isoformat() if due_date_obj else None
            })

    except Exception as e:
        import traceback
        print(f"DEBUG: add_task failed for user_id={user_id}")
        print(traceback.format_exc())

        return error_response(
            ErrorCode.DATABASE_ERROR, 
            f"Neural Link Failure: {str(e)}"
        )

