from sqlmodel import Session, select
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User
from datetime import datetime


class TaskService:
    """
    Service class for task-related operations.
    """

    @staticmethod
    def create_task(session: Session, task_create: TaskCreate, user_id: int) -> Task:
        """
        Create a new task for the specified user.
        """
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            user_id=user_id
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def get_user_tasks(session: Session, user_id: int) -> List[Task]:
        """
        Get all tasks for the specified user.
        """
        statement = select(Task).where(Task.user_id == user_id)
        return session.exec(statement).all()

    @staticmethod
    def get_task_by_id(session: Session, task_id: int, user_id: int) -> Optional[Task]:
        """
        Get a specific task by its ID for the specified user.
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def update_task(session: Session, task_id: int, task_update: TaskUpdate, user_id: int) -> Optional[Task]:
        """
        Update a specific task for the specified user.
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = session.exec(statement).first()
        if not db_task:
            return None

        # Update task fields if they are provided
        for field, value in task_update.model_dump(exclude_unset=True).items():
            setattr(db_task, field, value)

        db_task.updated_at = datetime.utcnow()
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: int) -> bool:
        """
        Delete a specific task for the specified user.
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = session.exec(statement).first()
        if not db_task:
            return False

        session.delete(db_task)
        session.commit()
        return True

    @staticmethod
    def toggle_task_completion(session: Session, task_id: int, user_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task for the specified user.
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = session.exec(statement).first()
        if not db_task:
            return None

        # Toggle completion status
        db_task.completed = not db_task.completed
        db_task.updated_at = datetime.utcnow()
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task