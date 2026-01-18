"""
TaskService provides business logic for task operations.
Implements the core functionality for creating, reading, updating, and deleting tasks.
"""

import logging
from typing import List, Optional
from src.models.task import Task
from src.lib.storage import InMemoryStorage


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskService:
    """
    Service class that handles all task-related business logic.
    Uses InMemoryStorage for data persistence.
    """

    def __init__(self, storage: InMemoryStorage = None):
        self.storage = storage or InMemoryStorage()

    def create_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Create a new task with the given title and optional description.
        Assigns a unique ID to the task and marks it as incomplete by default.
        """
        logger.info(f"Creating new task with title: '{title}'")

        # Validate title
        if not title or not title.strip():
            error_msg = "Title is required and cannot be empty"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Create a new task with the next available ID
        next_id = self.storage.get_next_id()
        task = Task(id=next_id, title=title.strip(), description=description, completed=False)
        result = self.storage.add_task(task)
        logger.info(f"Task created successfully with ID: {result.id}")
        return result

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.
        Returns None if the task doesn't exist.
        """
        logger.debug(f"Retrieving task with ID: {task_id}")
        task = self.storage.get_task(task_id)
        if task:
            logger.debug(f"Task found: {task.title}")
        else:
            logger.debug(f"Task with ID {task_id} not found")
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in the system.
        Returns an empty list if no tasks exist.
        """
        logger.debug("Retrieving all tasks")
        tasks = self.storage.list_tasks()
        logger.info(f"Retrieved {len(tasks)} tasks")
        return tasks

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task's title and/or description.
        Returns None if the task doesn't exist.
        """
        logger.info(f"Updating task with ID: {task_id}")

        existing_task = self.storage.get_task(task_id)
        if not existing_task:
            logger.warning(f"Attempted to update non-existent task with ID: {task_id}")
            return None

        # Use provided values or keep existing ones
        updated_title = title if title is not None else existing_task.title
        updated_description = description if description is not None else existing_task.description

        logger.debug(f"Updating task: '{existing_task.title}' -> '{updated_title}'")

        # Create updated task with new values
        updated_task = Task(
            id=task_id,
            title=updated_title,
            description=updated_description,
            completed=existing_task.completed
        )

        result = self.storage.update_task(task_id, updated_task)
        if result:
            logger.info(f"Task {task_id} updated successfully")
        return result

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.
        Returns True if the task was deleted, False if it didn't exist.
        """
        logger.info(f"Deleting task with ID: {task_id}")
        success = self.storage.delete_task(task_id)
        if success:
            logger.info(f"Task {task_id} deleted successfully")
        else:
            logger.warning(f"Attempted to delete non-existent task with ID: {task_id}")
        return success

    def toggle_completion(self, task_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task.
        Returns None if the task doesn't exist.
        """
        logger.info(f"Toggling completion status for task with ID: {task_id}")

        existing_task = self.storage.get_task(task_id)
        if not existing_task:
            logger.warning(f"Attempted to toggle completion for non-existent task with ID: {task_id}")
            return None

        new_status = not existing_task.completed
        logger.debug(f"Task {task_id} status changing from {existing_task.completed} to {new_status}")

        # Create updated task with toggled completion status
        updated_task = Task(
            id=task_id,
            title=existing_task.title,
            description=existing_task.description,
            completed=new_status
        )

        result = self.storage.update_task(task_id, updated_task)
        if result:
            logger.info(f"Task {task_id} completion status toggled successfully to {new_status}")
        return result

    def get_completed_tasks(self) -> List[Task]:
        """
        Retrieve all completed tasks.
        """
        return self.storage.find_tasks(completed=True)

    def get_pending_tasks(self) -> List[Task]:
        """
        Retrieve all pending (not completed) tasks.
        """
        return self.storage.find_tasks(completed=False)