from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlmodel import Session, select, or_, and_, func
from typing import List, Optional
from ..models import (
    Task, TaskCreate, TaskRead, TaskUpdate, User, TaskTag, Tag, Reminder,
    TaskFilter, TaskSort, RecurringTaskCreate, ReminderCreate, TagCreate, TagRead,
    TaskPriority, RecurringPattern, AuditLog
)
from ..database.database import get_session
from ..api.deps import get_current_user
from ..events.publisher import get_publisher
from ..dapr.client import DaprEventPublisher, get_dapr_client
from datetime import datetime, timedelta
import json


router = APIRouter()


@router.get("/", response_model=List[TaskRead])
async def read_tasks(
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    # Filtering parameters
    priority: Optional[TaskPriority] = None,
    completed: Optional[bool] = None,
    tags: Optional[str] = Query(None, description="Comma-separated tag names"),
    due_date_from: Optional[datetime] = None,
    due_date_to: Optional[datetime] = None,
    search: Optional[str] = None,
    category: Optional[str] = None,
    # Sorting parameter
    sort_by: TaskSort = TaskSort.CREATED_DESC,
    session: Session = Depends(get_session)
):
    """
    Retrieve tasks with advanced filtering and sorting.
    """
    print(f"DEBUG: read_tasks triggered for User: {current_user.id}")
    try:
        # Build base query
        query = select(Task).where(Task.user_id == current_user.id)
        
        # Apply filters
        if priority:
            query = query.where(Task.priority == priority)
        
        if completed is not None:
            query = query.where(Task.completed == completed)
        
        if due_date_from:
            query = query.where(Task.due_date >= due_date_from)
        
        if due_date_to:
            query = query.where(Task.due_date <= due_date_to)
        
        if category:
            query = query.where(Task.category == category)
        
        if search:
            search_term = f"%{search}%"
            query = query.where(
                or_(
                    Task.title.ilike(search_term),
                    Task.description.ilike(search_term)
                )
            )
        
        # Apply tag filter if provided
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",")]
            # Join with task_tags to filter by tags
            query = query.join(TaskTag).where(TaskTag.tag_name.in_(tag_list))
        
        # Apply sorting
        if sort_by == TaskSort.CREATED_ASC:
            query = query.order_by(Task.created_at.asc())
        elif sort_by == TaskSort.CREATED_DESC:
            query = query.order_by(Task.created_at.desc())
        elif sort_by == TaskSort.DUE_DATE_ASC:
            query = query.order_by(Task.due_date.asc().nulls_last())
        elif sort_by == TaskSort.DUE_DATE_DESC:
            query = query.order_by(Task.due_date.desc().nulls_last())
        elif sort_by == TaskSort.PRIORITY_ASC:
            query = query.order_by(Task.priority.asc())
        elif sort_by == TaskSort.PRIORITY_DESC:
            query = query.order_by(Task.priority.desc())
        elif sort_by == TaskSort.TITLE_ASC:
            query = query.order_by(Task.title.asc())
        elif sort_by == TaskSort.TITLE_DESC:
            query = query.order_by(Task.title.desc())
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        tasks = session.exec(query).all()
        
        # Load tags for each task
        result = []
        for task in tasks:
            task_dict = task.model_dump()
            # Get tags for this task
            tag_query = select(TaskTag.tag_name).where(TaskTag.task_id == task.id)
            task_tags = session.exec(tag_query).all()
            task_dict['tags'] = task_tags
            result.append(TaskRead(**task_dict))
        
        print(f"DEBUG: Found {len(result)} tasks")
        return result
        
    except Exception as e:
        import traceback
        err_detail = f"System Link Error: {str(e)}\n{traceback.format_exc()}"
        print(f"CRITICAL ERROR in read_tasks: {err_detail}")
        raise HTTPException(
            status_code=500, 
            detail=f"Neural Log Failure: {str(e)}"
        )


@router.post("/", response_model=TaskRead)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task with advanced features.
    """
    try:
        # Create the task
        db_task = Task(
            title=task.title,
            description=task.description,
            completed=task.completed,
            priority=task.priority,
            category=task.category,
            due_date=task.due_date,
            is_recurring=task.is_recurring,
            recurring_pattern=task.recurring_pattern,
            recurring_interval=task.recurring_interval,
            parent_task_id=task.parent_task_id,
            user_id=current_user.id
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        
        # Add tags if provided
        if task.tags:
            for tag_name in task.tags:
                # Create tag if it doesn't exist
                tag_query = select(Tag).where(Tag.name == tag_name, Tag.user_id == current_user.id)
                existing_tag = session.exec(tag_query).first()
                if not existing_tag:
                    new_tag = Tag(name=tag_name, user_id=current_user.id)
                    session.add(new_tag)
                
                # Create task-tag relationship
                task_tag = TaskTag(task_id=db_task.id, tag_name=tag_name)
                session.add(task_tag)
        
        # Create reminder if due date is set
        if task.due_date:
            # Create reminder 1 hour before due date
            remind_at = task.due_date - timedelta(hours=1)
            
            # Create reminder record in database
            reminder = Reminder(
                task_id=db_task.id,
                user_id=current_user.id,
                remind_at=remind_at,
                message=f"Task '{task.title}' is due in 1 hour"
            )
            session.add(reminder)
            
            # Schedule reminder using Dapr Jobs API for exact timing
            try:
                dapr_publisher = DaprEventPublisher()
                dapr_success = await dapr_publisher.schedule_reminder_job(
                    reminder_id=db_task.id,  # Using task_id as reminder_id for simplicity
                    remind_at=remind_at,
                    task_id=db_task.id,
                    user_id=current_user.id,
                    message=f"Task '{task.title}' is due in 1 hour"
                )
                
                if not dapr_success:
                    print(f"Failed to schedule Dapr job for reminder {db_task.id}")
            except Exception as e:
                print(f"Failed to schedule Dapr reminder job: {e}")
        
        session.commit()
        
        # Publish task created event (Dapr + fallback)
        try:
            # Try Dapr first
            dapr_publisher = DaprEventPublisher()
            dapr_success = await dapr_publisher.publish_task_created(
                task_id=db_task.id,
                user_id=current_user.id,
                task_data={
                    "title": task.title,
                    "description": task.description,
                    "priority": task.priority,
                    "category": task.category,
                    "tags": task.tags or [],
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "is_recurring": task.is_recurring
                }
            )
            
            if not dapr_success:
                # Fallback to direct event publisher
                publisher = await get_publisher()
                await publisher.publish_task_created(
                    task_id=db_task.id,
                    user_id=current_user.id,
                    task_data={
                        "title": task.title,
                        "description": task.description,
                        "priority": task.priority,
                        "category": task.category,
                        "tags": task.tags or [],
                        "due_date": task.due_date.isoformat() if task.due_date else None,
                        "is_recurring": task.is_recurring
                    }
                )
        except Exception as e:
            print(f"Failed to publish task created event: {e}")
        
        # Log the event
        audit_log = AuditLog(
            event_type="task.created",
            aggregate_id=str(db_task.id),
            user_id=current_user.id,
            event_data=json.dumps({
                "task_id": db_task.id,
                "title": task.title,
                "priority": task.priority,
                "tags": task.tags or []
            })
        )
        session.add(audit_log)
        session.commit()
        
        # Return task with tags
        task_dict = db_task.model_dump()
        task_dict['tags'] = task.tags or []
        return TaskRead(**task_dict)
        
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Task creation error: {str(e)}")


@router.post("/recurring", response_model=TaskRead)
def create_recurring_task(
    task: RecurringTaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new recurring task.
    """
    try:
        db_task = Task(
            title=task.title,
            description=task.description,
            priority=task.priority,
            category=task.category,
            due_date=task.due_date,
            is_recurring=True,
            recurring_pattern=task.recurring_pattern,
            recurring_interval=task.recurring_interval,
            user_id=current_user.id
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        
        # Add tags
        if task.tags:
            for tag_name in task.tags:
                task_tag = TaskTag(task_id=db_task.id, tag_name=tag_name)
                session.add(task_tag)
        
        session.commit()
        
        task_dict = db_task.model_dump()
        task_dict['tags'] = task.tags or []
        return TaskRead(**task_dict)
        
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Recurring task creation error: {str(e)}")


@router.get("/search")
async def search_tasks(
    q: str = Query(..., min_length=1, description="Search query"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Full-text search across tasks.
    """
    try:
        search_term = f"%{q}%"
        query = select(Task).where(
            and_(
                Task.user_id == current_user.id,
                or_(
                    Task.title.ilike(search_term),
                    Task.description.ilike(search_term),
                    Task.category.ilike(search_term)
                )
            )
        ).order_by(Task.created_at.desc())
        
        tasks = session.exec(query).all()
        
        # Add tags to results
        result = []
        for task in tasks:
            task_dict = task.model_dump()
            tag_query = select(TaskTag.tag_name).where(TaskTag.task_id == task.id)
            task_tags = session.exec(tag_query).all()
            task_dict['tags'] = task_tags
            result.append(task_dict)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@router.put("/{task_id}/priority")
async def update_task_priority(
    task_id: int,
    priority: TaskPriority,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update task priority.
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    db_task = session.exec(statement).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    old_priority = db_task.priority
    db_task.priority = priority
    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    session.commit()
    
    # Publish task priority changed event
    try:
        publisher = await get_publisher()
        await publisher.publish_task_priority_changed(
            task_id=task_id,
            user_id=current_user.id,
            old_priority=old_priority,
            new_priority=priority,
            title=db_task.title
        )
    except Exception as e:
        print(f"Failed to publish priority changed event: {e}")
    
    # Log the event
    audit_log = AuditLog(
        event_type="task.priority_updated",
        aggregate_id=str(task_id),
        user_id=current_user.id,
        event_data=json.dumps({
            "task_id": task_id,
            "old_priority": old_priority,
            "new_priority": priority
        })
    )
    session.add(audit_log)
    session.commit()
    
    return {"message": "Priority updated successfully", "priority": priority}


@router.post("/{task_id}/tags")
def add_task_tags(
    task_id: int,
    tags: List[str],
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Add tags to a task.
    """
    # Verify task exists and belongs to user
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    db_task = session.exec(statement).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    added_tags = []
    for tag_name in tags:
        # Check if tag relationship already exists
        existing = session.exec(
            select(TaskTag).where(TaskTag.task_id == task_id, TaskTag.tag_name == tag_name)
        ).first()
        
        if not existing:
            # Create tag if it doesn't exist
            tag_query = select(Tag).where(Tag.name == tag_name, Tag.user_id == current_user.id)
            existing_tag = session.exec(tag_query).first()
            if not existing_tag:
                new_tag = Tag(name=tag_name, user_id=current_user.id)
                session.add(new_tag)
            
            # Create task-tag relationship
            task_tag = TaskTag(task_id=task_id, tag_name=tag_name)
            session.add(task_tag)
            added_tags.append(tag_name)
    
    session.commit()
    return {"message": f"Added {len(added_tags)} tags", "added_tags": added_tags}


@router.delete("/{task_id}/tags/{tag_name}")
def remove_task_tag(
    task_id: int,
    tag_name: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Remove a tag from a task.
    """
    # Verify task belongs to user
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    db_task = session.exec(statement).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Remove tag relationship
    tag_rel = session.exec(
        select(TaskTag).where(TaskTag.task_id == task_id, TaskTag.tag_name == tag_name)
    ).first()
    
    if tag_rel:
        session.delete(tag_rel)
        session.commit()
        return {"message": "Tag removed successfully"}
    else:
        raise HTTPException(status_code=404, detail="Tag not found on this task")


@router.put("/{task_id}/due-date")
def update_task_due_date(
    task_id: int,
    due_date: Optional[datetime],
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update task due date and create/update reminder.
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    db_task = session.exec(statement).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    old_due_date = db_task.due_date
    db_task.due_date = due_date
    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    
    # Handle reminders
    if due_date:
        # Remove existing reminders
        existing_reminders = session.exec(
            select(Reminder).where(Reminder.task_id == task_id)
        ).all()
        for reminder in existing_reminders:
            session.delete(reminder)

        # Create new reminder (1 hour before due date)
        remind_at = due_date - timedelta(hours=1)
        if remind_at > datetime.utcnow():
            reminder = Reminder(
                task_id=task_id,
                user_id=current_user.id,
                remind_at=remind_at,
                message=f"Task '{db_task.title}' is due in 1 hour"
            )
            session.add(reminder)
            
            # Schedule reminder using Dapr Jobs API for exact timing
            try:
                dapr_publisher = DaprEventPublisher()
                dapr_success = await dapr_publisher.schedule_reminder_job(
                    reminder_id=task_id,
                    remind_at=remind_at,
                    task_id=task_id,
                    user_id=current_user.id,
                    message=f"Task '{db_task.title}' is due in 1 hour"
                )
                
                if not dapr_success:
                    print(f"Failed to schedule Dapr job for reminder {task_id}")
            except Exception as e:
                print(f"Failed to schedule Dapr reminder job: {e}")

    session.commit()
    
    return {
        "message": "Due date updated successfully", 
        "old_due_date": old_due_date,
        "new_due_date": due_date
    }


@router.get("/overdue")
def get_overdue_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all overdue tasks for the current user.
    """
    now = datetime.utcnow()
    query = select(Task).where(
        and_(
            Task.user_id == current_user.id,
            Task.due_date < now,
            Task.completed == False
        )
    ).order_by(Task.due_date.asc())
    
    overdue_tasks = session.exec(query).all()
    
    result = []
    for task in overdue_tasks:
        task_dict = task.model_dump()
        tag_query = select(TaskTag.tag_name).where(TaskTag.task_id == task.id)
        task_tags = session.exec(tag_query).all()
        task_dict['tags'] = task_tags
        result.append(task_dict)
    
    return result


# Existing endpoints (updated to work with new schema)
@router.delete("/delete-all")
async def delete_all_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete ALL tasks for the current authenticated user.
    """
    try:
        statement = select(Task).where(Task.user_id == current_user.id)
        tasks = session.exec(statement).all()
        
        count = len(tasks)
        for task in tasks:
            session.delete(task)
        
        session.commit()
        return {"message": f"Deleted {count} task(s)", "deleted_count": count}
            
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Wipe Error: {str(e)}")


@router.get("/{task_id}", response_model=TaskRead)
def read_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    task = session.exec(statement).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Add tags
    task_dict = task.model_dump()
    tag_query = select(TaskTag.tag_name).where(TaskTag.task_id == task.id)
    task_tags = session.exec(tag_query).all()
    task_dict['tags'] = task_tags
    
    return TaskRead(**task_dict)


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID.
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    db_task = session.exec(statement).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task fields if they are provided
    update_data = task_update.model_dump(exclude_unset=True)
    tags_to_update = update_data.pop('tags', None)
    
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    
    # Update tags if provided
    if tags_to_update is not None:
        # Remove existing tags
        existing_tags = session.exec(
            select(TaskTag).where(TaskTag.task_id == task_id)
        ).all()
        for tag in existing_tags:
            session.delete(tag)
        
        # Add new tags
        for tag_name in tags_to_update:
            task_tag = TaskTag(task_id=task_id, tag_name=tag_name)
            session.add(task_tag)
    
    session.commit()
    session.refresh(db_task)
    
    # Return with tags
    task_dict = db_task.model_dump()
    if tags_to_update is not None:
        task_dict['tags'] = tags_to_update
    else:
        tag_query = select(TaskTag.tag_name).where(TaskTag.task_id == task_id)
        task_tags = session.exec(tag_query).all()
        task_dict['tags'] = task_tags
    
    return TaskRead(**task_dict)


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID.
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    db_task = session.exec(statement).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(db_task)
    session.commit()
    
    # Log the event
    audit_log = AuditLog(
        event_type="task.deleted",
        aggregate_id=str(task_id),
        user_id=current_user.id,
        event_data=json.dumps({"task_id": task_id, "title": db_task.title})
    )
    session.add(audit_log)
    session.commit()
    
    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/complete", response_model=TaskRead)
async def toggle_task_completion(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task.
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    db_task = session.exec(statement).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Toggle completion status
    old_status = db_task.completed
    db_task.completed = not db_task.completed
    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    session.commit()
    
    # Publish task completion event
    try:
        publisher = await get_publisher()
        await publisher.publish_task_completed(
            task_id=task_id,
            user_id=current_user.id,
            task_data={
                "title": db_task.title,
                "completed_at": datetime.utcnow().isoformat(),
                "was_overdue": db_task.due_date and db_task.due_date < datetime.utcnow() if db_task.due_date else False
            }
        )
    except Exception as e:
        print(f"Failed to publish task completed event: {e}")
    
    # Log the event
    audit_log = AuditLog(
        event_type="task.completed" if db_task.completed else "task.uncompleted",
        aggregate_id=str(task_id),
        user_id=current_user.id,
        event_data=json.dumps({
            "task_id": task_id,
            "old_status": old_status,
            "new_status": db_task.completed
        })
    )
    session.add(audit_log)
    session.commit()
    
    # Return with tags
    task_dict = db_task.model_dump()
    tag_query = select(TaskTag.tag_name).where(TaskTag.task_id == task_id)
    task_tags = session.exec(tag_query).all()
    task_dict['tags'] = task_tags
    
    return TaskRead(**task_dict)