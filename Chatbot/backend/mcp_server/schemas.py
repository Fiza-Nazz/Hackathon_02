"""
Pydantic schemas for MCP tool inputs and outputs.

All MCP tools use these schemas for validation and consistent response formatting.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ============================================================================
# Error Response Constants
# ============================================================================

class ErrorCode:
    """Standard error codes for MCP tools."""
    INVALID_INPUT = "INVALID_INPUT"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    DATABASE_ERROR = "DATABASE_ERROR"


# ============================================================================
# Tool Input Schemas
# ============================================================================

class AddTaskInput(BaseModel):
    """Input schema for add_task tool."""
    user_id: int = Field(..., description="User identifier (Integer)")
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Optional task description")


class ListTasksInput(BaseModel):
    """Input schema for list_tasks tool."""
    user_id: int = Field(..., description="User identifier (Integer)")
    status: str = Field("all", pattern="^(all|pending|completed)$", description="Filter by completion status")


class CompleteTaskInput(BaseModel):
    """Input schema for complete_task tool."""
    user_id: int = Field(..., description="User identifier (Integer)")
    task_id: int = Field(..., ge=1, description="Task identifier to mark complete")


class DeleteTaskInput(BaseModel):
    """Input schema for delete_task tool."""
    user_id: int = Field(..., description="User identifier (Integer)")
    task_id: int = Field(..., ge=1, description="Task identifier to delete")


class UpdateTaskInput(BaseModel):
    """Input schema for update_task tool."""
    user_id: int = Field(..., description="User identifier (Integer)")
    task_id: int = Field(..., ge=1, description="Task identifier to update")
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="New task title")
    description: Optional[str] = Field(None, max_length=1000, description="New task description")

    # Custom validator to ensure at least one field is provided
    @classmethod
    def validate_update(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if not values.get("title") and not values.get("description"):
            raise ValueError("At least one field (title or description) must be provided")
        return values


# ============================================================================
# Tool Output Schemas
# ============================================================================

class TaskData(BaseModel):
    """Task data returned by tools."""
    id: int
    title: str
    completed: bool
    created_at: str


class AddTaskResponse(BaseModel):
    """Response data for add_task tool."""
    task_id: int
    status: str = "created"
    title: str


class ListTasksResponse(BaseModel):
    """Response data for list_tasks tool."""
    tasks: List[TaskData]
    total: int


class CompleteTaskResponse(BaseModel):
    """Response data for complete_task tool."""
    task_id: int
    status: str = "completed"
    title: str


class DeleteTaskResponse(BaseModel):
    """Response data for delete_task tool."""
    task_id: int
    status: str = "deleted"
    title: str


class UpdateTaskResponse(BaseModel):
    """Response data for update_task tool."""
    task_id: int
    status: str = "updated"
    title: str


# ============================================================================
# Unified Response Schemas
# ============================================================================

class ErrorResponse(BaseModel):
    """Standard error response format."""
    code: str
    message: str


def success_response(data: Any) -> Dict[str, Any]:
    """
    Create a standardized success response.

    Args:
        data: Tool-specific response data

    Returns:
        Dict with success=True and data
    """
    return {
        "success": True,
        "data": data,
        "error": None
    }


def error_response(code: str, message: str) -> Dict[str, Any]:
    """
    Create a standardized error response.

    Args:
        code: Error code from ErrorCode
        message: Human-readable error message

    Returns:
        Dict with success=False and error
    """
    return {
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message
        }
    }
