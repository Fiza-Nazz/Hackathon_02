"""
Configuration management for the Todo Application.
"""

import os
from typing import Optional


class Config:
    """
    Configuration class to manage application settings.
    """

    # Application settings
    APP_NAME = "AI-Native Todo Application"
    APP_VERSION = "0.1.0"

    # Storage settings
    MAX_TASK_TITLE_LENGTH = 255
    MAX_TASK_DESCRIPTION_LENGTH = 1000

    # Performance settings
    MAX_TASKS_DISPLAY = 100  # Maximum number of tasks to display at once

    # Error handling settings
    ENABLE_DETAILED_ERRORS = os.getenv('ENABLE_DETAILED_ERRORS', 'False').lower() == 'true'

    @staticmethod
    def get_env_var(key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get environment variable with optional default value.
        """
        return os.getenv(key, default)

    @staticmethod
    def is_production() -> bool:
        """
        Check if running in production environment.
        """
        env = os.getenv('TODO_ENV', 'development').lower()
        return env in ['production', 'prod']

    @staticmethod
    def get_max_display_tasks() -> int:
        """
        Get maximum number of tasks to display at once.
        """
        try:
            return int(os.getenv('MAX_TASKS_DISPLAY', Config.MAX_TASKS_DISPLAY))
        except ValueError:
            return Config.MAX_TASKS_DISPLAY