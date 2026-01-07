from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from ..models import Task, TaskCreate, TaskRead, TaskUpdate, User
from ..database.database import get_session
from ..api.deps import get_current_user
from datetime import datetime


router = APIRouter()


@router.get("/", response_model=List[TaskRead])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve tasks for the current user.
    """
    statement = select(Task).where(Task.user_id == current_user.id).offset(skip).limit(limit)
    tasks = session.exec(statement).all()
    return tasks


@router.post("/", response_model=TaskRead)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the current user.
    """
    # Create task with current user's ID
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        priority=task.priority,
        category=task.category,
        user_id=current_user.id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


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
    return task


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
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)

    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


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
    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/complete", response_model=TaskRead)
def toggle_task_completion(
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
    db_task.completed = not db_task.completed
    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task