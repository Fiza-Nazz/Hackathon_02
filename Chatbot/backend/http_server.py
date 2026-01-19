"""
ELITE NEURAL COMMANDER - VERSION 3.8.0 (GROQ LIGHTNING)
Built by Fiza Nazz for TODOAI Engine.
Powered by Groq AI - Ultra-fast, Unlimited Free Tier
"""

import sys
from pathlib import Path
import os
import json
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

# --- ADVANCED ENVIRONMENT SYNC ---
current_dir = Path(__file__).resolve().parent
backend_env = current_dir.parent.parent / "backend" / ".env"
load_dotenv(backend_env)

# --- SYSTEM PATH CONFIG ---
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
from sqlmodel import Session, select, delete

# Internal Imports
try:
    from backend.db import init_db, get_engine
    from backend.models import Conversation, Message, Task
    from backend.mcp_server.tools.add_task import add_task
    from backend.mcp_server.tools.list_tasks import list_tasks
    from backend.mcp_server.tools.complete_task import complete_task
    from backend.mcp_server.tools.delete_task import delete_task
    from backend.mcp_server.tools.update_task import update_task
    from backend.mcp_server.tools.delete_all_tasks import delete_all_tasks
except ImportError:
    # Local fallback for direct execution
    from db import init_db, get_engine
    from models import Conversation, Message, Task
    from mcp_server.tools.add_task import add_task
    from mcp_server.tools.list_tasks import list_tasks
    from mcp_server.tools.complete_task import complete_task
    from mcp_server.tools.delete_task import delete_task
    from mcp_server.tools.update_task import update_task
    from mcp_server.tools.delete_all_tasks import delete_all_tasks

# --- ELITE AI ENGINE (GROQ LIGHTNING - UNLIMITED FREE) ---
# Groq provides 30 requests/minute with super-fast inference
AI_MODELS = [
    "llama-3.3-70b-versatile",   # Primary: Groq's latest and most stable model
    "llama-3.1-8b-instant",      # Backup
    "gemma2-9b-it"               # Alternative
]

client = None
api_key = os.getenv("GROQ_API_KEY")  # Changed from OPENAI_API_KEY

try:
    from openai import AsyncOpenAI
    if api_key:
        client = AsyncOpenAI(
            base_url="https://api.groq.com/openai/v1",  # Groq endpoint
            api_key=api_key,
        )
except Exception as e:
    print(f"AI Client Error: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Elite Neural Commander", version="3.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class ChatMessageRequest(BaseModel):
    message: str
    user_id: Optional[str] = "1"
    language: Optional[str] = "en"

# --- AI TOOLS ---
TOOLS = [
    {"type": "function", "function": {"name": "add_task", "description": "Create a new task on the dashboard.", "parameters": {"type": "object", "properties": {"title": {"type": "string", "description": "The exact title of the task."}}, "required": ["title"]}}},
    {"type": "function", "function": {"name": "list_tasks", "description": "Retrieve all tasks from the dashboard.", "parameters": {"type": "object", "properties": {"status": {"type": "string", "enum": ["all", "pending", "completed"], "default": "all"}}}}},
    {"type": "function", "function": {"name": "complete_task", "description": "Mark a specific task as done using its numeric ID.", "parameters": {"type": "object", "properties": {"task_id": {"type": "integer", "description": "The numeric ID of the task."}}, "required": ["task_id"]}}},
    {"type": "function", "function": {"name": "delete_task", "description": "Permanently remove a task using its numeric ID.", "parameters": {"type": "object", "properties": {"task_id": {"type": "integer", "description": "The numeric ID of the task."}}, "required": ["task_id"]}}},
    {"type": "function", "function": {"name": "update_task", "description": "Change the title of an existing task.", "parameters": {"type": "object", "properties": {"task_id": {"type": "integer", "description": "The numeric ID of the task."}, "title": {"type": "string", "description": "The new title."}}, "required": ["task_id", "title"]}}},
    {"type": "function", "function": {"name": "delete_all_tasks", "description": "Wipe all tasks for the current user.", "parameters": {"type": "object", "properties": {}}}}
]

# --- PROFESSIONAL AGENT LOGIC ---
class AgentProcessor:
    def __init__(self, user_id: str, session: Session, language: str = "en", auth_token: str = None):
        self.user_id = str(user_id)
        self.session = session
        self.language = language
        self.auth_token = auth_token
        self.tool_handlers = {
            "add_task": add_task, 
            "list_tasks": list_tasks, 
            "complete_task": complete_task, 
            "delete_task": delete_task, 
            "update_task": update_task,
            "delete_all_tasks": delete_all_tasks
        }

    def _get_elite_welcome(self):
        is_ur = self.language == "ur"
        if is_ur:
            return "👋 **خوش آمدید، میں آپ کا نیورل اسسٹنٹ ہوں۔**\n\nمیں آپ کے تمام ٹاسک اور سوالات کو پروفیشنل طریقے سے مینیج کر سکتا ہوں۔\n\n**آپ مجھ سے کچھ بھی پوچھ سکتے ہیں!**"
        return "👋 **Welcome, Operator.**\n\nI am your **Neural Task Assistant v3.0**. I can manage your tasks and answer any professional or general inquiries with high precision.\n\n**How can I assist you today?**"

    async def _handle_fallback(self, message: str, error: str = ""):
        """Professional Local Sync Logic"""
        msg = message.lower().strip()
        is_ur = self.language == "ur"
        
        # Identity
        if any(w in msg for w in ["who are you", "what is your name", "yourself", "built by", "fiza nazz"]):
            if is_ur: return "🛡️ **نیورل کمانڈر v3.3**\n\nمیں **فضا ناز** (ویژنری فل اسٹیک اور اے آئی ڈویلپر) کا بنایا ہوا ایک پروفیشنل AI ایجنٹ ہوں۔"
            return "🛡️ **NEURAL COMMANDER v3.3**\n\nI am a high-standard AI Agent built by **Fiza Nazz**, a visionary Full-Stack and Agentic AI Developer, to provide expert assistance and manage complex task ecosystems."

        # Quick Task Handler
        if "list" in msg or "show" in msg or "دکھاؤ" in msg:
            res = self.tool_handlers["list_tasks"](user_id=self.user_id, auth_token=self.auth_token)
            if res.get("success"):
                tasks = res["data"]["tasks"]
                if not tasks: return "📭 **No tasks found in your dashboard.**"
                out = "📋 **Active Tasks:**\n\n"
                for t in tasks: out += f"- **ID: {t['id']}** | {t['title']} ({'Done' if t['completed'] else 'Pending'})\n"
                return out

        if is_ur:
            return f"🤖 **نیورل کور (لوکل موڈ)**\n\nمعذرت، اس وقت اے آئی سروس میں تھوڑی دشواری ہے۔ میں آپ کے ٹاسک مینیج کر سکتا ہوں۔\n\n*Error: {error}*"
        return f"🤖 **NEURAL CORE (LOCAL SYNC ACTIVE)**\n\nI am currently operating in high-reliability local mode due to a temporary neural link interruption. I can still manage your tasks (Add, List, Delete).\n\n*Technical Log: {error}*"

    async def process(self, message: str, history: List[Dict[str, str]]):
        # 1. Immediate Greeting Recognition
        low_msg = message.lower().strip()
        if low_msg in ["hi", "hello", "hy", "hey", "how are you", "how are you?", "kaise ho", "kese ho"]:
            return self._get_elite_welcome()

        if not client: return await self._handle_fallback(message, "AI Client Not Initialized")

        # 2. Multi-Model Execution Loop (The "Ultimate Fix")
        last_error = ""
        for model in AI_MODELS:
            try:
                # KNOWLEDGE BASE: FIZA NAZZ PROFESSIONAL PROFILE
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
                # Filter history to remove any previous "failed" generation or raw tags
                clean_history = []
                for h in history[-8:]:
                    if "<function" not in h.get("content", "") and "formula=" not in h.get("content", ""):
                        clean_history.append(h)
                
                messages.extend(clean_history)
                messages.append({"role": "user", "content": message})

                response = await client.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=TOOLS,
                    tool_choice="auto",
                    timeout=25.0,
                    max_tokens=2000  # Groq has generous limits!
                )
                
                resp_msg = response.choices[0].message
                if resp_msg.tool_calls:
                    messages.append(resp_msg)
                    for tc in resp_msg.tool_calls:
                        try:
                            # Parse arguments and add auth context
                            args = json.loads(tc.function.arguments)
                            args['user_id'] = self.user_id
                            args['auth_token'] = self.auth_token
                            
                            handler = self.tool_handlers.get(tc.function.name)
                            if handler:
                                tool_res = handler(**args)
                                # Clean result to only what AI needs
                                messages.append({
                                    "role": "tool", 
                                    "tool_call_id": tc.id, 
                                    "name": tc.function.name, 
                                    "content": json.dumps(tool_res)
                                })
                        except Exception as te:
                            messages.append({
                                "role": "tool", 
                                "tool_call_id": tc.id, 
                                "name": tc.function.name, 
                                "content": json.dumps({"success": False, "error": str(te)})
                            })
                    
                    # Second call to summarize results
                    # Use tools=TOOLS but tool_choice="none" to prevent recursive chaining issues on Groq
                    final_resp = await client.chat.completions.create(
                        model=model, 
                        messages=messages,
                        tools=TOOLS,
                        tool_choice="none", 
                        timeout=25.0
                    )
                    return final_resp.choices[0].message.content or "Task processed."
                
                return resp_msg.content

            except Exception as e:
                last_error = str(e)
                print(f"Model {model} failed: {last_error}")
                if any(err in last_error.lower() for err in ["404", "data policy", "402", "credits", "limit", "429"]):
                    continue # Automatic Failover to next model
                break 

        return await self._handle_fallback(message, last_error)

# --- ENDPOINTS ---
@app.post("/api/chat/message")
async def handle_message(request: Request, body: ChatMessageRequest):
    user_id = body.user_id or "1"
    auth_token = request.headers.get("Authorization", "").replace("Bearer ", "") or None
    
    with Session(get_engine()) as session:
        # Get Latest Conversation
        stmt = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
        conv = session.exec(stmt).first()
        
        if not conv or (datetime.utcnow() - conv.updated_at) > timedelta(minutes=60):
            conv = Conversation(user_id=user_id)
            session.add(conv)
            session.commit()
            session.refresh(conv)

        # Process Response
        hist_stmt = select(Message).where(Message.conversation_id == conv.id).order_by(Message.created_at.asc())
        history = [{"role": m.role, "content": m.content} for m in session.exec(hist_stmt).all()]
        
        processor = AgentProcessor(user_id, session, body.language, auth_token)
        response_text = await processor.process(body.message, history)

        # Save History
        session.add(Message(conversation_id=conv.id, user_id=user_id, role="user", content=body.message))
        session.add(Message(conversation_id=conv.id, user_id=user_id, role="assistant", content=response_text))
        conv.updated_at = datetime.utcnow()
        session.add(conv)
        session.commit()
        
        return {"content": response_text, "conversation_id": conv.id}

@app.get("/api/chat/history/{user_id}")
async def get_history(user_id: str):
    with Session(get_engine()) as session:
        stmt = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
        conv = session.exec(stmt).first()
        if not conv: return []
        stmt_msg = select(Message).where(Message.conversation_id == conv.id).order_by(Message.created_at.asc())
        return [{"role": m.role, "content": m.content} for m in session.exec(stmt_msg).all()]

@app.delete("/api/chat/history/{user_id}")
async def clear_history(user_id: str):
    with Session(get_engine()) as session:
        session.execute(delete(Message).where(Message.user_id == user_id))
        session.execute(delete(Conversation).where(Conversation.user_id == user_id))
        session.commit()
    return {"status": "success"}

@app.get("/health")
def health(): return {"status": "operational", "version": "3.8.0 (Groq Lightning)", "ai_ready": client is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)