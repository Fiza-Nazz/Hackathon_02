import os
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select, delete
from openai import AsyncOpenAI

from ..database.database import get_session, engine
from ..models import Task, User, Conversation, Message
from .mcp_server import call_tool
from .deps import get_current_user

router = APIRouter()

# --- AI CONFIG ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ACTIVE_KEY = OPENAI_API_KEY or GROQ_API_KEY

client = None
if ACTIVE_KEY:
    if ACTIVE_KEY.startswith("gsk_"):
        client = AsyncOpenAI(base_url="https://api.groq.com/openai/v1", api_key=ACTIVE_KEY)
    else:
        client = AsyncOpenAI(api_key=ACTIVE_KEY)

# Tool definitions for OpenAI
AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task on the dashboard.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Retrieve all tasks from the dashboard.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["all", "pending", "completed"]}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as done using its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer"}
                },
                "required": ["task_id"]
            }
        }
    }
]

class OpenAI_MCP_Agent:
    def __init__(self, user_id: str):
        self.user_id = user_id

    async def run(self, message: str, history: List[Dict[str, str]]):
        if not client: return "Error: Neural Link Key missing. Please check configuration."

        fiza_bio = (
            "**Fiza Nazz** - Visionary Full-Stack & Agentic AI Developer | Karachi, Pakistan\n"
            "Contact: +92-3123632197 | LinkedIn: fiza-nazz-765241355 | GitHub: Fiza-Nazz\n"
            "Portfolio: https://nextjs-portfolio-tau-black.vercel.app/\n"
        )

        messages = [{"role": "system", "content": f"""STRICT IDENTITY:
You are ELITE NEURAL COMMANDER v4.0, a sophisticated AI Agent built by Fiza Nazz.
Creator Info: {fiza_bio}

RULES:
1. ONLY use official tool_calls.
2. NO text tags like <function>.
3. Give professional, natural language responses.
4. Match user's language (Roman Urdu/English/Urdu Script).
"""}]
        messages.extend(history[-8:])
        messages.append({"role": "user", "content": message})

        try:
            model = "llama-3.3-70b-versatile" if ACTIVE_KEY.startswith("gsk_") else "gpt-4"
            
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                tools=AGENT_TOOLS,
                tool_choice="auto"
            )

            assistant_msg = response.choices[0].message
            if assistant_msg.tool_calls:
                messages.append(assistant_msg)
                for tc in assistant_msg.tool_calls:
                    args = json.loads(tc.function.arguments)
                    args["user_id"] = self.user_id
                    
                    mcp_res = await call_tool(tc.function.name, args)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "name": tc.function.name,
                        "content": mcp_res[0].text
                    })
                
                final_response = await client.chat.completions.create(
                    model=model,
                    messages=messages
                )
                return final_response.choices[0].message.content
            
            return assistant_msg.content
        except Exception as e:
            return f"Neural Disruption: {str(e)}"

class ChatMessageRequest(BaseModel):
    message: Optional[str] = None
    text: Optional[str] = None
    user_id: Optional[str] = None
    language: str = "en"

    @property
    def content(self) -> str:
        return self.message or self.text or ""

@router.post("/message")
async def handle_chat_message(request: Request, body: ChatMessageRequest, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    user_id = str(current_user.id)
    msg_content = body.content
    print(f"DEBUG: Chat request from user {user_id}, content: {msg_content[:20]}...")
    
    if not msg_content:
        return {"content": "Neural Link established. How can I assist you?"}

    conv = session.exec(select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())).first()
    if not conv or (datetime.utcnow() - conv.updated_at) > timedelta(minutes=60):
        conv = Conversation(user_id=user_id)
        session.add(conv)
        session.commit()
        session.refresh(conv)

    history_objs = session.exec(select(Message).where(Message.conversation_id == conv.id).order_by(Message.created_at.asc())).all()
    history = [{"role": m.role, "content": m.content} for m in history_objs]
    
    agent = OpenAI_MCP_Agent(user_id)
    response_text = await agent.run(msg_content, history)

    session.add(Message(conversation_id=conv.id, user_id=user_id, role="user", content=msg_content))
    session.add(Message(conversation_id=conv.id, user_id=user_id, role="assistant", content=response_text))
    conv.updated_at = datetime.utcnow()
    session.add(conv)
    session.commit()
    
    return {"content": response_text, "conversation_id": conv.id}


@router.post("/{user_id}/chat")
async def handle_chat(user_id: str, body: ChatMessageRequest, session: Session = Depends(get_session)):
    # Keep this for backward compatibility or direct calls
    msg_content = body.content
    conv = session.exec(select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())).first()
    if not conv or (datetime.utcnow() - conv.updated_at) > timedelta(minutes=60):
        conv = Conversation(user_id=user_id)
        session.add(conv)
        session.commit()
        session.refresh(conv)

    history_objs = session.exec(select(Message).where(Message.conversation_id == conv.id).order_by(Message.created_at.asc())).all()
    history = [{"role": m.role, "content": m.content} for m in history_objs]
    
    agent = OpenAI_MCP_Agent(user_id)
    response_text = await agent.run(msg_content, history)

    session.add(Message(conversation_id=conv.id, user_id=user_id, role="user", content=msg_content))
    session.add(Message(conversation_id=conv.id, user_id=user_id, role="assistant", content=response_text))
    conv.updated_at = datetime.utcnow()
    session.add(conv)
    session.commit()
    
    return {"content": response_text, "conversation_id": conv.id}

@router.get("/history")
async def get_chat_history(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    user_id = str(current_user.id)
    conv = session.exec(select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())).first()
    if not conv: return []
    msgs = session.exec(select(Message).where(Message.conversation_id == conv.id).order_by(Message.created_at.asc())).all()
    return [{"role": m.role, "content": m.content} for m in msgs]

@router.delete("/history")
async def clear_chat_history(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    user_id = str(current_user.id)
    session.execute(delete(Message).where(Message.user_id == user_id))
    session.execute(delete(Conversation).where(Conversation.user_id == user_id))
    session.commit()
    return {"success": True}

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
