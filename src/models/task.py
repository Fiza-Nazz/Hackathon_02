"""
Task model representing a todo item with ID, title, description, and completion status.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """
    Represents a todo item with a unique ID, title (required), description (optional),
    and completion status (boolean).
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self):
        """Validate the task after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Title is required and cannot be empty")

        if len(self.title) > 255:
            raise ValueError("Title must be 255 characters or less")

        if self.description and len(self.description) > 1000:
            raise ValueError("Description must be 1000 characters or less")

    def __str__(self):
        """String representation of the task."""
        status = "X" if self.completed else "O"
        return f"[{status}] {self.id}. {self.title}"

    def __repr__(self):
        """Developer-friendly representation of the task."""
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', completed={self.completed})"