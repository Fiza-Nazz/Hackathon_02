"""
ELITE NEURAL COMMANDER - VERSION 4.5.0 (NEURAL-SYNC)
Built by Fiza Nazz for TODOAI Engine.
Powered by Groq AI - Ultra-fast, Unlimited Free Tier
"""

import sys
from pathlib import Path
import os
import json
import asyncio
import uuid
import hashlib
import binascii
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext

# --- ADVANCED ENVIRONMENT SYNC ---
current_dir = Path(__file__).resolve().parent
backend_env = current_dir.parent.parent / "backend" / ".env"
load_dotenv(backend_env, override=True)

# --- AUTH SETUP ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET") or "my_ultra_secure_secret_123"
ALGORITHM = "HS256"

def verify_scrypt_password(password: str, stored_hash: str) -> bool:
    """Verify Scrypt hash (used by Better Auth)."""
    try:
        if ":" not in stored_hash: 
            print("DEBUG: Scrypt hash format invalid (no colon)")
            return False
        salt_hex, hash_hex = stored_hash.split(":")
        salt = binascii.unhexlify(salt_hex)
        derived_hash = hashlib.scrypt(password.encode(), salt=salt, n=16384, r=8, p=1, dklen=64)
        result = binascii.hexlify(derived_hash).decode() == hash_hex
        print(f"DEBUG: Scrypt verification result: {result}")
        return result
    except Exception as e: 
        print(f"DEBUG: Scrypt error: {str(e)}")
        return False

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Hybrid verification for Bcrypt and Scrypt."""
    if ":" in hashed_password and len(hashed_password) > 100:
        print("DEBUG: Identifying as Scrypt hash")
        return verify_scrypt_password(plain_password, hashed_password)
    try:
        print("DEBUG: Identifying as Bcrypt/Standard hash")
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e: 
        print(f"DEBUG: Bcrypt/Standard error: {str(e)}")
        return False

# --- SYSTEM PATH CONFIG ---
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
from sqlmodel import Session, select, delete

# Internal Imports
try:
    from backend.db import init_db, get_engine
    from backend.models import Conversation, Message, Task, User, Account
    from backend.mcp_server.tools.add_task import add_task
    from backend.mcp_server.tools.list_tasks import list_tasks
    from backend.mcp_server.tools.complete_task import complete_task
    from backend.mcp_server.tools.uncomplete_task import uncomplete_task
    from backend.mcp_server.tools.delete_task import delete_task
    from backend.mcp_server.tools.update_task import update_task
    from backend.mcp_server.tools.delete_all_tasks import delete_all_tasks
except ImportError:
    # Local fallback for direct execution
    from db import init_db, get_engine
    from models import Conversation, Message, Task, User, Account
    from mcp_server.tools.add_task import add_task
    from mcp_server.tools.list_tasks import list_tasks
    from mcp_server.tools.complete_task import complete_task
    from mcp_server.tools.uncomplete_task import uncomplete_task
    from mcp_server.tools.delete_task import delete_task
    from mcp_server.tools.update_task import update_task
    from mcp_server.tools.delete_all_tasks import delete_all_tasks
    from mcp_server.tools.set_priority import set_priority
    from mcp_server.tools.add_tags import add_tags
    from mcp_server.tools.set_due_date import set_due_date

# --- ELITE AI ENGINE (GROQ LIGHTNING - UNLIMITED FREE) ---
AI_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it"
]

# Import OpenAI client globally
from openai import AsyncOpenAI

def get_ai_client():
    """Get AI client with fresh API key from environment."""
    # Reload .env to get latest key
    chatbot_env = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(chatbot_env, override=True)
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("⚠️ No GROQ_API_KEY found in environment")
        return None
    
    # Strip whitespace just in case
    api_key = api_key.strip()
    
    return AsyncOpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key,
    )

client = get_ai_client()
if client:
    print("✅ AI Client initialized with Groq API")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Elite Neural Commander", version="4.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class ChatMessageRequest(BaseModel):
    message: Optional[str] = None
    messages: Optional[List[Dict[str, str]]] = None # For Vercel AI SDK compatibility
    user_id: Optional[str] = "1"
    language: Optional[str] = "en"

class LoginRequest(BaseModel):
    email: str
    password: str

# --- AI TOOLS ---
TOOLS = [
    {"type": "function", "function": {"name": "add_task", "description": "Create a new task with advanced features.", "parameters": {"type": "object", "properties": {"title": {"type": "string", "description": "The exact title of the task."}, "description": {"type": "string", "description": "Optional task description."}, "priority": {"type": "string", "enum": ["low", "medium", "high"], "default": "medium"}, "tags": {"type": "string", "description": "Comma-separated tags."}, "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD HH:MM:SS format."}}, "required": ["title"]}}},
    {"type": "function", "function": {"name": "list_tasks", "description": "Retrieve all tasks from the dashboard.", "parameters": {"type": "object", "properties": {"status": {"type": "string", "enum": ["all", "pending", "completed"], "default": "all"}}}}},
    {"type": "function", "function": {"name": "complete_task", "description": "Mark a specific task as DONE (completed: true).", "parameters": {"type": "object", "properties": {"task_id": {"type": "integer", "description": "The numeric ID of the task."}}, "required": ["task_id"]}}},
    {"type": "function", "function": {"name": "uncomplete_task", "description": "Mark a task as PENDING (completed: false).", "parameters": {"type": "object", "properties": {"task_id": {"type": "integer", "description": "The numeric ID of the task."}}, "required": ["task_id"]}}},
    {"type": "function", "function": {"name": "delete_task", "description": "Permanently remove a task using its numeric ID.", "parameters": {"type": "object", "properties": {"task_id": {"type": "integer", "description": "The numeric ID of the task."}}, "required": ["task_id"]}}},
    {"type": "function", "function": {"name": "update_task", "description": "Change the title of an existing task.", "parameters": {"type": "object", "properties": {"task_id": {"type": "integer", "description": "The numeric ID of the task."}, "title": {"type": "string", "description": "The new title."}}, "required": ["task_id", "title"]}}},
    {"type": "function", "function": {"name": "delete_all_tasks", "description": "Wipe all tasks for the current user.", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "set_priority", "description": "Set task priority (high, medium, low).", "parameters": {"type": "object", "properties": {"task_id": {"type": "integer", "description": "The numeric ID of the task."}, "priority": {"type": "string", "enum": ["low", "medium", "high"]}}, "required": ["task_id", "priority"]}}},
    {"type": "function", "function": {"name": "add_tags", "description": "Add tags to a task.", "parameters": {"type": "object", "properties": {"task_id": {"type": "integer", "description": "The numeric ID of the task."}, "tags": {"type": "string", "description": "Comma-separated tag names."}}, "required": ["task_id", "tags"]}}},
    {"type": "function", "function": {"name": "set_due_date", "description": "Set due date for a task.", "parameters": {"type": "object", "properties": {"task_id": {"type": "integer", "description": "The numeric ID of the task."}, "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD HH:MM:SS format."}}, "required": ["task_id", "due_date"]}}}
]

# --- PROFESSIONAL AGENT LOGIC (STREAMING) ---
class AgentProcessor:
    def __init__(self, user_id: str, language: str = "en", auth_token: str = None):
        self.user_id = str(user_id)
        self.language = language
        self.auth_token = auth_token
        self.tool_handlers = {
            "add_task": add_task, 
            "list_tasks": list_tasks, 
            "complete_task": complete_task, 
            "uncomplete_task": uncomplete_task,
            "delete_task": delete_task, 
            "update_task": update_task,
            "delete_all_tasks": delete_all_tasks,
            "set_priority": set_priority,
            "add_tags": add_tags,
            "set_due_date": set_due_date
        }

    def _get_elite_welcome(self):
        is_ur = self.language == "ur"
        if is_ur:
            return "👋 **خوش آمدید، میں آپ کا نیورل اسسٹنٹ ہوں۔**\n\nمیں آپ کے تمام ٹاسک اور سوالات کو پروفیشنل طریقے سے مینیج کر سکتا ہوں۔\n\n**آپ مجھ سے کچھ بھی پوچھ سکتے ہیں!**"
        return "👋 **Welcome, Operator.**\n\nI am your **Neural Task Assistant v4.5**. I can manage your tasks and answer any professional or general inquiries with high precision.\n\n**How can I assist you today?**"

    async def _handle_fallback(self, message: str, error: str = ""):
        # Fallback Logic
        msg = message.lower().strip()
        is_ur = self.language == "ur"
        if any(w in msg for w in ["who are you", "name", "yourself", "built by", "fiza nazz"]):
             return "🛡️ **NEURAL COMMANDER v4.0**\n\nI am a high-standard AI Agent built by **Fiza Nazz**."
        
        if is_ur: return "🤖 **سسٹم میں خرابی ہے - براہ کرم دوبارہ کوشش کریں**"
        
        # Professional Error Cleaning - NO ERROR DETAILS SHOWN
        clean_err = "Service temporarily unavailable. Please try again."
        if "401" in error: clean_err = "Authentication issue. Please refresh and try again."
        elif "400" in error: clean_err = "Invalid request format. Please rephrase."
        elif "connection" in error.lower(): clean_err = "Connection issue. Please try again."
        elif "timeout" in error.lower(): clean_err = "Request timed out. Please try again."
        
        return f"⚠️ {clean_err}"

    def _save_interaction(self, session, user_msg, ai_msg):
        try:
            # Refresh session to ensure active
            stmt = select(Conversation).where(Conversation.user_id == self.user_id).order_by(Conversation.updated_at.desc())
            conv = session.exec(stmt).first()
            if not conv:
                conv = Conversation(user_id=self.user_id)
                session.add(conv)
                session.commit()
                session.refresh(conv)
            
            session.add(Message(conversation_id=conv.id, user_id=self.user_id, role="user", content=user_msg))
            session.add(Message(conversation_id=conv.id, user_id=self.user_id, role="assistant", content=ai_msg))
            conv.updated_at = datetime.utcnow()
            session.add(conv)
            session.commit()
        except Exception as e:
            print(f"Failed to save history: {e}")

    async def process_stream(self, message: str, history: List[Dict[str, str]]):
        global client
        full_response = ""
        
        # 1. Greeting
        low_msg = message.lower().strip()
        if low_msg in ["hi", "hello", "hy", "hey", "how are you", "kaise ho"]:
            content = self._get_elite_welcome()
            # Send content directly without JSON wrapping
            yield content
            with Session(get_engine()) as session:
                self._save_interaction(session, message, content)
            return

        # Refresh client
        client = get_ai_client()
        if not client:
             yield "SYSTEM ERROR: Offline Mode - No Client"
             return

        # 2. Logic
        last_error = ""
        success_flag = False
        
        for model in AI_MODELS:
            try:
                # KNOWLEDGE BASE
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
                
                messages = [{"role": "system", "content": f"""You are **ELITE NEURAL COMMANDER v4.5**.
CREATED BY: **Fiza Nazz**.
ROLE: Ultimate Task Synchronization Agent.
BIO: {fiza_bio}

STRICT OPERATIONAL DIRECTIVES (NEURAL SYNC):
1. SYNC FIRST: Always run 'list_tasks' before performing any action (delete, complete, update) to ensure you have the real numeric ID.
2. NO HALLUCINATION: Never guess a numeric ID. If 'list_tasks' returns no tasks, tell the user the dashboard is empty.
3. EXPLICIT COMMANDS: If the user says 'mark done', use 'complete_task'. Even if it looks complete, run the tool anyway to ensure the server is synced.
4. DELETE PROTOCOL: If a user asks to delete, you MUST first find the ID via 'list_tasks'. If you get a 'Database Error', check the numeric ID again.
5. GROQ SAFETY: Never use XML tags like <tool>. Use the Tool Calling API only.
6. RESPONSE: Keep it professional. Use Roman Urdu only if the user does."""}]
                
                # Filter history
                clean_history = [h for h in history[-8:] if "<function" not in h.get("content", "")]
                messages.extend(clean_history)
                messages.append({"role": "user", "content": message})

                # Call 1: Tool Detection (Non-Stream)
                response = await client.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=TOOLS,
                    tool_choice="auto",
                    timeout=25.0
                )
                
                resp_msg = response.choices[0].message
                
                if resp_msg.tool_calls:
                     # Add assistant message
                     messages.append(resp_msg)
                     for tc in resp_msg.tool_calls:
                         try:
                             args = json.loads(tc.function.arguments)
                             args['user_id'] = self.user_id
                             args['auth_token'] = self.auth_token
                             handler = self.tool_handlers.get(tc.function.name)
                             if handler:
                                 tool_res = handler(**args)
                                 messages.append({
                                     "role": "tool", 
                                     "tool_call_id": tc.id, 
                                     "name": tc.function.name, 
                                     "content": json.dumps(tool_res)
                                 })
                         except Exception as te:
                             messages.append({"role": "tool", "tool_call_id": tc.id, "name": tc.function.name, "content": json.dumps({"error": str(te)})})
                     
                     # Call 2: Streaming Final Response
                     stream = await client.chat.completions.create(
                         model=model, 
                         messages=messages,
                         tools=TOOLS,
                         tool_choice="none",
                         stream=True, 
                         timeout=25.0
                     )
                     async for chunk in stream:
                         content = chunk.choices[0].delta.content or ""
                         if content:
                             yield content
                             full_response += content

                else:
                    # No tool call, yield content
                    content = resp_msg.content or ""
                    yield content
                    full_response = content
                
                success_flag = True
                break

            except Exception as e:
                last_error = str(e)
                print(f"Model {model} failed: {last_error}")
                if "401" in last_error:
                    # Invalid Key - Stop retrying models as key is likely issue
                     yield "⚠️ AUTHENTICATION ERROR: Invalid API Key."
                     return
                continue 
        
        if not success_flag:
            err_msg = await self._handle_fallback(message, last_error)
            yield err_msg
            full_response = err_msg

        # Save Interaction
        with Session(get_engine()) as session:
            self._save_interaction(session, message, full_response)

def get_user_id_from_request(request: Request) -> str:
    """
    Ultra-Resilient User ID Retrieval
    1. Try JWT Decode (Chatbot native)
    2. Try Database Session Search (Better Auth native)
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return "1"

    token = auth_header.split(" ")[1].strip()
    
    # Tier 1: JWT Decode
    try:
        if token.count('.') == 2:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get("sub", "1")
    except Exception as e:
        print(f"JWT Decode ignored: {e}")

    # Tier 2: Database Session Search (Failsafe for Better Auth)
    try:
        from backend.models.session import AuthSession
        with Session(get_engine()) as session:
            # Better Auth tokens are often just the session id/token
            stmt = select(AuthSession).where((AuthSession.token == token) | (AuthSession.id == token))
            res = session.exec(stmt).first()
            if res:
                return res.userId
    except Exception as e:
        print(f"Session Search Error: {e}")

    return "1"

@app.post("/api/auth/register")
async def register(body: LoginRequest):
    print(f"DEBUG: Register attempt for email: {body.email}")
    with Session(get_engine()) as session:
        # 1. Check if user exists
        stmt = select(User).where(User.email == body.email)
        existing_user = session.exec(stmt).first()
        if existing_user:
            print(f"DEBUG: Registration failed - user already exists: {body.email}")
            raise HTTPException(status_code=400, detail="User already registered")

        # 2. Create User
        user_id = str(uuid.uuid4())
        new_user = User(
            id=user_id,
            email=body.email,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )
        session.add(new_user)
        print(f"DEBUG: New user record created: {user_id}")

        # 3. Create Account (for password storage)
        hashed_password = pwd_context.hash(body.password)
        new_account = Account(
            id=str(uuid.uuid4()),
            userId=user_id,
            accountId=body.email,
            providerId="credential",
            password=hashed_password,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )
        session.add(new_account)
        session.commit()
        print(f"DEBUG: New account record created for user: {user_id}")

        # 4. Generate JWT
        access_token = jwt.encode({"sub": user_id, "email": body.email}, SECRET_KEY, algorithm=ALGORITHM)
        print("DEBUG: Registration successful, JWT generated")
        return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/login")
async def login(body: LoginRequest):
    print(f"DEBUG: Login attempt for email: {body.email}")
    with Session(get_engine()) as session:
        # 1. Find User
        stmt = select(User).where(User.email == body.email)
        user = session.exec(stmt).first()
        if not user:
            print(f"DEBUG: User not found: {body.email}")
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        print(f"DEBUG: User found: {user.id}")

        # 2. Find Credential Account and check password
        acc_stmt = select(Account).where(Account.userId == user.id).where(Account.providerId == "credential")
        account = session.exec(acc_stmt).first()
        
        if not account:
            print(f"DEBUG: No account found for user: {user.id}")
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        if not account.password:
            print(f"DEBUG: Account has no password: {user.id}")
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        is_valid = verify_password(body.password, account.password)
        print(f"DEBUG: Password verification result: {is_valid}")
        if not is_valid:
            print(f"DEBUG: Password mismatch for: {body.email}")
            raise HTTPException(status_code=401, detail="Invalid email or password")

        print("DEBUG: Login successful")
        # 3. Generate JWT
        access_token = jwt.encode({"sub": user.id, "email": body.email}, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": access_token, "token_type": "bearer"}

# --- CHAT ENDPOINTS ---
@app.post("/api/chat/message")
async def handle_message(request: Request, body: ChatMessageRequest):
    # Extract user_id from token if possible, else use body or default
    token_user_id = get_user_id_from_request(request)
    user_id = token_user_id if token_user_id != "1" else (body.user_id or "1")
    auth_token = request.headers.get("Authorization", "").replace("Bearer ", "").strip() or None

    # Extract message from 'message' field OR 'messages' list (Vercel AI SDK format)
    user_msg = body.message
    if not user_msg and body.messages and len(body.messages) > 0:
        user_msg = body.messages[-1].get("content", "")
    
    if not user_msg:
         async def err_gen(): 
             yield "Error: No message content provided"
         return StreamingResponse(err_gen(), media_type="text/plain; charset=utf-8")
    
    with Session(get_engine()) as session:
        # Load History
        conv = session.exec(select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())).first()
        history = []
        if conv:
             msgs = session.exec(select(Message).where(Message.conversation_id == conv.id).order_by(Message.created_at.asc())).all()
             history = [{"role": m.role, "content": m.content} for m in msgs]
    
    processor = AgentProcessor(user_id, body.language, auth_token)
    return StreamingResponse(processor.process_stream(user_msg, history), media_type="text/plain; charset=utf-8")

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

# --- TASK API ---
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: int = 1
    category: str = "General"

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[int] = None
    category: Optional[str] = None

@app.get("/api/tasks/")
async def read_tasks(request: Request):
    user_id = get_user_id_from_request(request)
    with Session(get_engine()) as session:
        tasks = session.exec(select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())).all()
        return tasks

@app.post("/api/tasks/")
async def create_task_endpoint(task: TaskCreate, request: Request):
    user_id = get_user_id_from_request(request)
    with Session(get_engine()) as session:
        db_task = Task(user_id=user_id, **task.model_dump())
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

@app.put("/api/tasks/{task_id}")
async def update_task_endpoint(task_id: int, task_update: TaskUpdate, request: Request):
    user_id = get_user_id_from_request(request)
    with Session(get_engine()) as session:
        db_task = session.get(Task, task_id)
        if not db_task or db_task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Task not found")
        task_data = task_update.model_dump(exclude_unset=True)
        for key, value in task_data.items():
            setattr(db_task, key, value)
        db_task.updated_at = datetime.utcnow()
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

@app.delete("/api/tasks/{task_id}")
async def delete_task_endpoint(task_id: int, request: Request):
    user_id = get_user_id_from_request(request)
    with Session(get_engine()) as session:
        db_task = session.get(Task, task_id)
        if not db_task or db_task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Task not found")
        session.delete(db_task)
        session.commit()
        return {"ok": True}

@app.patch("/api/tasks/{task_id}/complete")
async def toggle_task_completion_endpoint(task_id: int, request: Request):
    user_id = get_user_id_from_request(request)
    with Session(get_engine()) as session:
        db_task = session.get(Task, task_id)
        if not db_task or db_task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Task not found")
        db_task.completed = not db_task.completed
        db_task.updated_at = datetime.utcnow()
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

@app.get("/health")
def health(): return {"status": "operational", "version": "4.1.0 (ChatKit Streaming)", "ai_ready": client is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)