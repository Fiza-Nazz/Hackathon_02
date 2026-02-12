"""
MCP Tool: add_tags

Adds tags to a task.
"""

from typing import Dict, Any
from backend.mcp_server.schemas import success_response, error_response, ErrorCode

def add_tags(user_id: str, task_id: int, tags: str, auth_token: str = None) -> Dict[str, Any]:
    """
    Add tags to a task.

    Args:
        user_id: User identifier
        task_id: Task ID to tag
        tags: Comma-separated tag names

    Returns:
        Dict with success, data, or error
    """
    if not tags or not tags.strip():
        return error_response(ErrorCode.INVALID_INPUT, "Tags cannot be empty")

    tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
    
    if not tag_list:
        return error_response(ErrorCode.INVALID_INPUT, "No valid tags provided")

    try:
        from backend.db import get_engine
        from backend.models import Task, TaskTag, Tag
        from sqlmodel import Session, select
        
        with Session(get_engine()) as session:
            # Verify task exists and belongs to user
            stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            task = session.exec(stmt).first()
            
            if not task:
                return error_response(ErrorCode.NOT_FOUND, "Task not found")
            
            added_tags = []
            for tag_name in tag_list:
                # Check if tag relationship already exists
                existing = session.exec(
                    select(TaskTag).where(TaskTag.task_id == task_id, TaskTag.tag_name == tag_name)
                ).first()
                
                if not existing:
                    # Create tag if it doesn't exist
                    tag_query = select(Tag).where(Tag.name == tag_name, Tag.user_id == user_id)
                    existing_tag = session.exec(tag_query).first()
                    if not existing_tag:
                        new_tag = Tag(name=tag_name, user_id=user_id)
                        session.add(new_tag)
                    
                    # Create task-tag relationship
                    task_tag = TaskTag(task_id=task_id, tag_name=tag_name)
                    session.add(task_tag)
                    added_tags.append(tag_name)
            
            session.commit()
            
            return success_response({
                "task_id": task_id,
                "added_tags": added_tags,
                "status": "tags_added"
            })

    except Exception as e:
        return error_response(ErrorCode.DATABASE_ERROR, f"Tag addition failed: {str(e)}")