#!/usr/bin/env python3
"""
Console interface for the AI-Native Todo Application.
Provides a command-line interface for users to interact with their todo list.
"""

import sys
from typing import Optional
from src.services.task_service import TaskService
from src.lib.storage import InMemoryStorage
from src.models.task import Task
from src.config import Config


class TodoApp:
    """
    Main application class that handles the CLI interface for the todo application.
    """

    def __init__(self):
        self.storage = InMemoryStorage()
        self.service = TaskService(self.storage)
        self.running = True

    def display_menu(self):
        """Display the main menu options."""
        print("\n" + "="*50)
        print("AI-Native Todo Application")
        print("="*50)
        print("1. Create a new task")
        print("2. View all tasks")
        print("3. Update a task")
        print("4. Delete a task")
        print("5. Mark task as complete/incomplete")
        print("6. View completed tasks")
        print("7. View pending tasks")
        print("8. Help")
        print("9. Exit")
        print("="*50)

    def get_user_choice(self) -> str:
        """Get user's menu choice."""
        try:
            choice = input("Enter your choice (1-9): ").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            sys.exit(0)

    def create_task(self):
        """Create a new task."""
        print("\n--- Create New Task ---")

        title = input("Enter task title (required): ").strip()
        if not title:
            print("Error: Title is required!")
            return

        description_input = input("Enter task description (optional, press Enter to skip): ").strip()
        description = description_input if description_input else None

        try:
            task = self.service.create_task(title, description)
            print(f"✓ Task created successfully!")
            print(f"  ID: {task.id}")
            print(f"  Title: {task.title}")
            if task.description:
                print(f"  Description: {task.description}")
            print(f"  Status: {'Completed' if task.completed else 'Pending'}")
        except ValueError as e:
            print(f"Error creating task: {e}")

    def view_all_tasks(self):
        """View all tasks."""
        print("\n--- All Tasks ---")
        tasks = self.service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        for task in tasks:
            status = "✓" if task.completed else "○"
            print(f"[{status}] {task.id}. {task.title}")
            if task.description:
                print(f"      Description: {task.description}")
        print(f"\nTotal tasks: {len(tasks)}")

    def update_task(self):
        """Update an existing task."""
        print("\n--- Update Task ---")

        try:
            task_id = int(input("Enter task ID to update: "))
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return

        # Check if task exists
        existing_task = self.service.get_task(task_id)
        if not existing_task:
            print(f"Error: Task with ID {task_id} does not exist.")
            return

        print(f"Current task: {existing_task.title}")
        if existing_task.description:
            print(f"Current description: {existing_task.description}")

        new_title = input(f"Enter new title (or press Enter to keep '{existing_task.title}'): ").strip()
        new_title = new_title if new_title else None  # Use None to keep existing

        new_description = input(f"Enter new description (or press Enter to keep existing): ").strip()
        if new_description == "":
            new_description = None  # Use None to keep existing or set to None if currently None

        try:
            updated_task = self.service.update_task(task_id, new_title, new_description)
            print("✓ Task updated successfully!")
            print(f"  ID: {updated_task.id}")
            print(f"  Title: {updated_task.title}")
            if updated_task.description:
                print(f"  Description: {updated_task.description}")
            print(f"  Status: {'Completed' if updated_task.completed else 'Pending'}")
        except ValueError as e:
            print(f"Error updating task: {e}")

    def delete_task(self):
        """Delete a task."""
        print("\n--- Delete Task ---")

        try:
            task_id = int(input("Enter task ID to delete: "))
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return

        # Check if task exists
        existing_task = self.service.get_task(task_id)
        if not existing_task:
            print(f"Error: Task with ID {task_id} does not exist.")
            return

        print(f"Task to delete: {existing_task.title}")
        confirm = input("Are you sure you want to delete this task? (y/N): ").strip().lower()

        if confirm in ['y', 'yes']:
            success = self.service.delete_task(task_id)
            if success:
                print("✓ Task deleted successfully!")
            else:
                print("Error: Failed to delete task.")
        else:
            print("Deletion cancelled.")

    def toggle_task_completion(self):
        """Toggle task completion status."""
        print("\n--- Toggle Task Completion ---")

        try:
            task_id = int(input("Enter task ID to toggle: "))
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return

        task = self.service.get_task(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} does not exist.")
            return

        print(f"Current status for '{task.title}': {'Completed' if task.completed else 'Pending'}")

        updated_task = self.service.toggle_completion(task_id)
        if updated_task:
            new_status = "Completed" if updated_task.completed else "Pending"
            print(f"✓ Task status updated to: {new_status}")
        else:
            print("Error: Failed to update task status.")

    def view_completed_tasks(self):
        """View completed tasks."""
        print("\n--- Completed Tasks ---")
        completed_tasks = self.service.get_completed_tasks()

        if not completed_tasks:
            print("No completed tasks found.")
            return

        for task in completed_tasks:
            print(f"[✓] {task.id}. {task.title}")
            if task.description:
                print(f"      Description: {task.description}")
        print(f"\nTotal completed tasks: {len(completed_tasks)}")

    def view_pending_tasks(self):
        """View pending tasks."""
        print("\n--- Pending Tasks ---")
        pending_tasks = self.service.get_pending_tasks()

        if not pending_tasks:
            print("No pending tasks found.")
            return

        for task in pending_tasks:
            print(f"[○] {task.id}. {task.title}")
            if task.description:
                print(f"      Description: {task.description}")
        print(f"\nTotal pending tasks: {len(pending_tasks)}")

    def show_help(self):
        """Show help information."""
        print("\n--- Help ---")
        print("This is the AI-Native Todo Application.")
        print("You can create, view, update, delete, and manage your tasks.")
        print("\nCommands:")
        print("1. Create a new task - Add a task with a title and optional description")
        print("2. View all tasks - See all your tasks with their status")
        print("3. Update a task - Modify the title or description of an existing task")
        print("4. Delete a task - Remove a task from your list")
        print("5. Mark task as complete/incomplete - Toggle the completion status")
        print("6. View completed tasks - See only tasks that are marked as complete")
        print("7. View pending tasks - See only tasks that are not completed")
        print("8. Help - Show this help message")
        print("9. Exit - Close the application")

    def run(self):
        """Run the main application loop."""
        print(f"Welcome to {Config.APP_NAME} v{Config.APP_VERSION}!")
        print("Type 'help' or select option 8 for help.")

        while self.running:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == '1':
                self.create_task()
            elif choice == '2':
                self.view_all_tasks()
            elif choice == '3':
                self.update_task()
            elif choice == '4':
                self.delete_task()
            elif choice == '5':
                self.toggle_task_completion()
            elif choice == '6':
                self.view_completed_tasks()
            elif choice == '7':
                self.view_pending_tasks()
            elif choice == '8':
                self.show_help()
            elif choice == '9':
                print("Thank you for using the AI-Native Todo Application!")
                self.running = False
            else:
                print("Invalid choice. Please enter a number between 1 and 9.")
                print("Type 'help' or select option 8 for help.")


def main():
    """Main entry point for the application."""
    app = TodoApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()