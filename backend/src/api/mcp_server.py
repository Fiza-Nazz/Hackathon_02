from mcp.server import Server
from mcp.types import Tool, TextContent
import json
from sqlmodel import Session, select
from ..database.database import engine
from ..models import Task

# Create MCP Server instance
server = Server("todo-mcp-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="add_task",
            description="Create a new task on the dashboard.",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["user_id", "title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="Retrieve tasks from the dashboard.",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "status": {"type": "string", "enum": ["all", "pending", "completed"]}
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed.",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"}
                },
                "required": ["user_id", "task_id"]
            }
        )
    ]

async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    with Session(engine) as session:
        user_id = arguments.get("user_id")
        
        if name == "add_task":
            task = Task(title=arguments["title"], description=arguments.get("description", ""), user_id=user_id)
            session.add(task)
            session.commit()
            session.refresh(task)
            return [TextContent(type="text", text=f"Task '{task.title}' created with ID {task.id}")]
            
        elif name == "list_tasks":
            stmt = select(Task).where(Task.user_id == user_id)
            status = arguments.get("status", "all")
            if status == "pending":
                stmt = stmt.where(Task.completed == False)
            elif status == "completed":
                stmt = stmt.where(Task.completed == True)
            
            tasks = session.exec(stmt).all()
            result = [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks]
            return [TextContent(type="text", text=json.dumps(result))]
            
        elif name == "complete_task":
            task_id = arguments["task_id"]
            stmt = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
            task = session.exec(stmt).first()
            if task:
                task.completed = True
                session.add(task)
                session.commit()
                return [TextContent(type="text", text=f"Task {task_id} marked as complete")]
            return [TextContent(type="text", text="Task not found")]
            
    return [TextContent(type="text", text="Tool execution failed")]
