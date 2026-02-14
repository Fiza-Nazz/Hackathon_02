"""
In-memory storage implementation for tasks.
All data is stored in memory only (no persistent storage).
"""

from typing import Dict, Optional
from src.models.task import Task


class InMemoryStorage:
    """
    In-memory storage for tasks using a dictionary with ID as key.
    Provides O(1) lookup by ID and maintains uniqueness of task IDs.
    """

    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1

    def add_task(self, task: Task) -> Task:
        """Insert a new task with auto-generated unique ID."""
        # If the task doesn't have an ID yet, assign one
        if task.id is None or task.id == 0:
            task.id = self._next_id
            self._next_id += 1

        # Ensure ID is unique
        if task.id in self._tasks:
            raise ValueError(f"Task with ID {task.id} already exists")

        self._tasks[task.id] = task
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID."""
        return self._tasks.get(task_id)

    def update_task(self, task_id: int, updated_task: Task) -> Optional[Task]:
        """Update existing task attributes."""
        if task_id not in self._tasks:
            return None

        # Preserve the original ID
        updated_task.id = task_id
        self._tasks[task_id] = updated_task
        return updated_task

    def delete_task(self, task_id: int) -> bool:
        """Remove a task by its ID."""
        if task_id not in self._tasks:
            return False

        del self._tasks[task_id]
        return True

    def list_tasks(self) -> list:
        """Retrieve all tasks in the collection."""
        return list(self._tasks.values())

    def find_tasks(self, **criteria) -> list:
        """Search/filter tasks based on criteria (e.g., completed status)."""
        tasks = self.list_tasks()

        if 'completed' in criteria:
            completed = criteria['completed']
            tasks = [task for task in tasks if task.completed == completed]

        if 'title' in criteria:
            title = criteria['title']
            tasks = [task for task in tasks if title.lower() in task.title.lower()]

        return tasks

    def get_next_id(self) -> int:
        """Allocate and return the next unique ID."""
        next_id = self._next_id
        self._next_id += 1
        return next_id