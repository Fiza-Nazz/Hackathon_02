"""
MCP Server for Task Management.

This server exposes 5 task management tools via the Model Context Protocol:
- add_task: Create a new task
- list_tasks: List tasks with optional status filter
- complete_task: Mark a task as completed
- delete_task: Delete a task
- update_task: Update task title/description
"""

from mcp.server import Server
from mcp.types import Tool, TextContent

# Server instance
server = Server("task-management-mcp")

# Tool imports (will be added after implementation)
# from .tools import add_task, list_tasks, complete_task, delete_task, update_task


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Return list of available MCP tools."""
    return [
        Tool(
            name="add_task",
            description="Create a new task for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User identifier"},
                    "title": {"type": "string", "description": "Task title (1-200 chars)"},
                    "description": {"type": "string", "description": "Optional task description (0-1000 chars)"}
                },
                "required": ["user_id", "title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="List all tasks for a user with optional status filter",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User identifier"},
                    "status": {"type": "string", "enum": ["all", "pending", "completed"], "default": "all"}
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User identifier"},
                    "task_id": {"type": "integer", "description": "Task ID"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a task",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User identifier"},
                    "task_id": {"type": "integer", "description": "Task ID"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="update_task",
            description="Update task title and/or description",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User identifier"},
                    "task_id": {"type": "integer", "description": "Task ID"},
                    "title": {"type": "string", "description": "New task title (1-200 chars)"},
                    "description": {"type": "string", "description": "New task description (0-1000 chars)"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Route tool calls to appropriate handler.

    Args:
        name: Tool name
        arguments: Tool arguments

    Returns:
        List of TextContent with tool result
    """
    tool_map = {
        "add_task": "add_task",
        "list_tasks": "list_tasks",
        "complete_task": "complete_task",
        "delete_task": "delete_task",
        "update_task": "update_task",
    }

    if name not in tool_map:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    # Import and call the tool
    try:
        from .tools import add_task, list_tasks, complete_task, delete_task, update_task

        handlers = {
            "add_task": add_task,
            "list_tasks": list_tasks,
            "complete_task": complete_task,
            "delete_task": delete_task,
            "update_task": update_task,
        }

        handler = handlers[name]

        # Check if handler is async or sync
        import inspect
        if inspect.iscoroutinefunction(handler):
            result = await handler(**arguments)
        else:
            result = handler(**arguments)

        return [TextContent(type="text", text=str(result))]

    except ImportError:
        return [TextContent(type="text", text=f"Tool {name} not yet implemented")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error in {name}: {str(e)}")]


def create_conversation(user_id: str) -> dict:
    """
    Helper function to create a new conversation.

    This will be used by the future chat endpoint to initialize conversations.

    Args:
        user_id: User identifier

    Returns:
        Dict with conversation_id and created timestamp
    """
    from backend.models.conversation import Conversation
    from backend.db import engine
    from sqlmodel import Session

    with Session(engine) as session:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return {
            "conversation_id": conversation.id,
            "created_at": conversation.created_at.isoformat()
        }


if __name__ == "__main__":
    import asyncio
    asyncio.run(server.run())
