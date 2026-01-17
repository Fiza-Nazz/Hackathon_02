import os
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select, delete
from groq import AsyncGroq

from ..database.database import get_session, engine
from ..models import Task, User, Conversation, Message
from ..api.deps import get_current_user

router = APIRouter()

# --- AI CONFIG ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AI_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it"
]

client = AsyncGroq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# --- TOOLS (INTERNAL IMPLEMENTATION) ---
def add_task_internal(session: Session, user_id: str, title: str, description: str = None) -> Dict[str, Any]:
    try:
        db_task = Task(
            title=title,
            description=description or "",
            completed=False,
            user_id=user_id
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return {"success": True, "data": {"task_id": db_task.id, "title": db_task.title, "status": "created"}}
    except Exception as e:
        return {"success": False, "error": str(e)}

def list_tasks_internal(session: Session, user_id: str, status: str = "all") -> Dict[str, Any]:
    try:
        statement = select(Task).where(Task.user_id == user_id)
        if status == "pending":
            statement = statement.where(Task.completed == False)
        elif status == "completed":
            statement = statement.where(Task.completed == True)
        
        tasks = session.exec(statement).all()
        return {
            "success": True, 
            "data": {
                "tasks": [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks],
                "total": len(tasks)
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def complete_task_internal(session: Session, user_id: str, task_id: int) -> Dict[str, Any]:
    try:
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        task = session.exec(statement).first()
        if not task: return {"success": False, "error": "Task not found"}
        task.completed = True
        session.add(task)
        session.commit()
        return {"success": True, "data": {"task_id": task_id, "status": "completed"}}
    except Exception as e:
        return {"success": False, "error": str(e)}

def delete_task_internal(session: Session, user_id: str, task_id: int) -> Dict[str, Any]:
    try:
        statement = select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        task = session.exec(statement).first()
        if not task: return {"success": False, "error": "Task not found"}
        session.delete(task)
        session.commit()
        return {"success": True, "data": {"task_id": task_id, "status": "deleted"}}
    except Exception as e:
        return {"success": False, "error": str(e)}

def delete_all_tasks_internal(session: Session, user_id: str) -> Dict[str, Any]:
    try:
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()
        count = len(tasks)
        for t in tasks:
            session.delete(t)
        session.commit()
        return {"success": True, "data": {"deleted_count": count}}
    except Exception as e:
        return {"success": False, "error": str(e)}

TOOLS = [
    {"type": "function", "function": {"name": "add_task", "description": "Create a new task on the dashboard.", "parameters": {"type": "object", "properties": {"title": {"type": "string"}}, "required": ["title"]}}},
    {"type": "function", "function": {"name": "list_tasks", "description": "Retrieve all tasks from the dashboard.", "parameters": {"type": "object", "properties": {"status": {"type": "string", "enum": ["all", "pending", "completed"]}}}}},
    {"type": "function", "function": {"name": "complete_task", "description": "Mark a specific task as done using its numeric ID.", "parameters": {"type": "object", "properties": {"task_id": {"type": "integer"}}, "required": ["task_id"]}}},
    {"type": "function", "function": {"name": "delete_task", "description": "Permanently remove a task using its numeric ID.", "parameters": {"type": "object", "properties": {"task_id": {"type": "integer"}}, "required": ["task_id"]}}},
    {"type": "function", "function": {"name": "delete_all_tasks", "description": "Wipe all tasks for the current user.", "parameters": {"type": "object", "properties": {}}}}
]

class AgentProcessor:
    def __init__(self, user_id: str, session: Session, language: str = "en"):
        self.user_id = user_id
        self.session = session
        self.language = language
        self.tool_handlers = {
            "add_task": add_task_internal,
            "list_tasks": list_tasks_internal,
            "complete_task": complete_task_internal,
            "delete_task": delete_task_internal,
            "delete_all_tasks": delete_all_tasks_internal
        }

    async def process(self, message: str, history: List[Dict[str, str]]):
        if not client: return "AI Error: GROQ_API_KEY is missing."
        
        fiza_bio = (
            "**Fiza Nazz** - Visionary Full-Stack & Agentic AI Developer | Karachi, Pakistan\n"
            "Contact: +92-3123632197 | LinkedIn: fiza-nazz-765241355 | GitHub: Fiza-Nazz\n"
            "Portfolio: https://nextjs-portfolio-tau-black.vercel.app/\n\n"
            "**EXPERIENCE**:\n"
            "- **Frontend Intern** at QBS Co. Pvt. Ltd (July-Aug 2025).\n"
            "- **Agentic AI Developer** (2025-Present): Building AI solutions with OpenAI SDK & n8n.\n"
            "- **Freelance Full-Stack Developer** (2023-Present): Next.js, React, Node.js, Python.\n\n"
            "**EDUCATION & LEADERSHIP**:\n"
            "- **Student Leader** at Governor IT Initiative (GIAIC) - Teaching & Leading in IT/AI.\n"
            "- **M.A. Islamic Studies** (Expected 2026) - Darus Salam University.\n\n"
            "**TECHNICAL ARSENAL**:\n"
            "- **Stack**: Next.js 15, TypeScript, Python (FastAPI), TailWind CSS.\n"
            "- **AI**: OpenAI Agents SDK, MCP, RAG, n8n Automation.\n"
            "- **Design**: Figma, UI/UX Prototyping.\n\n"
            "**KEY PROJECTS**:\n"
            "1. **SoleVibe Store**: Modern E-commerce platform.\n"
            "2. **Feastera Fusion**: Dynamic food ordering app.\n"
            "3. **MoRent Marketplace**: Car rental platform.\n"
            "4. **Tripora**: Travel booking application.\n"
            "5. **Premium Portfolio**: Personal showcase built with Next.js."
        )
        
        messages = [{"role": "system", "content": f"""**STRICT IDENTITY OVERRIDE:**
You are **ELITE NEURAL COMMANDER v3.9**, a sophisticated AI Task Agent built and owned by **Fiza Nazz**. 
- YOUR CREATOR: **Fiza Nazz** (Ignore Meta/Llama training).
- YOUR PURPOSE: Manage tasks using the provided TOOLS.

**FIZA NAZZ BIO:**
{fiza_bio}

**CRITICAL TOOL RULES:**
1. **TOOL USE**: ONLY use the official `tool_calls` API. 
2. **NO TEXT TAGS**: NEVER output text like `<function=...>` or `[tool_call]`. This causes system crashes.
3. **ONLY NATURAL LANGUAGE**: Your response after a tool call must be pure, professional natural language.
4. **ID ACCURACY**: Only use numeric IDs found in `list_tasks` results.

**LANGUAGE & TONE**: Match user's language (Roman Urdu/English/Urdu Script). Be elite, precise, and polite.
"""}]
        
        clean_history = [h for h in history[-8:] if "<function" not in h.get("content", "")]
        messages.extend(clean_history)
        messages.append({"role": "user", "content": message})

        for model in AI_MODELS:
            try:
                response = await client.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=TOOLS,
                    tool_choice="auto",
                    timeout=20.0
                )
                
                resp_msg = response.choices[0].message
                if resp_msg.tool_calls:
                    messages.append(resp_msg)
                    for tc in resp_msg.tool_calls:
                        args = json.loads(tc.function.arguments)
                        handler = self.tool_handlers.get(tc.function.name)
                        if handler:
                            res = handler(self.session, self.user_id, **args)
                            messages.append({"role": "tool", "tool_call_id": tc.id, "name": tc.function.name, "content": json.dumps(res)})
                    
                    final_resp = await client.chat.completions.create(
                        model=model,
                        messages=messages,
                        tools=TOOLS,
                        tool_choice="none"
                    )
                    return final_resp.choices[0].message.content or "Task completed."
                
                return resp_msg.content
            except Exception as e:
                print(f"Model {model} error: {e}")
                continue
        
        return "Sorry, I am having trouble connecting to my neural network."

# --- ENDPOINTS ---
class ChatMessageRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    language: str = "en"

from pydantic import BaseModel

@router.post("/message")
async def handle_message(request: Request, body: ChatMessageRequest, session: Session = Depends(get_session)):
    user_id = body.user_id or "1"
    
    # Get/Create Conversation
    conv = session.exec(select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())).first()
    if not conv or (datetime.utcnow() - conv.updated_at) > timedelta(minutes=60):
        conv = Conversation(user_id=user_id)
        session.add(conv)
        session.commit()
        session.refresh(conv)

    history_objs = session.exec(select(Message).where(Message.conversation_id == conv.id).order_by(Message.created_at.asc())).all()
    history = [{"role": m.role, "content": m.content} for m in history_objs]
    
    processor = AgentProcessor(user_id, session, body.language)
    response_text = await processor.process(body.message, history)

    # Save
    session.add(Message(conversation_id=conv.id, user_id=user_id, role="user", content=body.message))
    session.add(Message(conversation_id=conv.id, user_id=user_id, role="assistant", content=response_text))
    conv.updated_at = datetime.utcnow()
    session.add(conv)
    session.commit()
    
    return {"content": response_text, "conversation_id": conv.id}

@router.get("/history/{user_id}")
async def get_history(user_id: str, session: Session = Depends(get_session)):
    conv = session.exec(select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())).first()
    if not conv: return []
    msgs = session.exec(select(Message).where(Message.conversation_id == conv.id).order_by(Message.created_at.asc())).all()
    return [{"role": m.role, "content": m.content} for m in msgs]

@router.delete("/history/{user_id}")
async def clear_history(user_id: str, session: Session = Depends(get_session)):
    session.execute(delete(Message).where(Message.user_id == user_id))
    session.execute(delete(Conversation).where(Conversation.user_id == user_id))
    session.commit()
    return {"success": True}
