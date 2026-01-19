# Conversational AI Chatbot Foundation

This project implements a conversational AI chatbot foundation with persistent conversation history and integrated task management tools.

## Features

- **Persistent Chat History**: All conversations and messages are stored in the database
- **Task Management**: 5 standardized MCP tools for managing tasks (add, list, complete, update, delete)
- **User Isolation**: Complete data isolation between users
- **Natural Language Processing**: Designed for integration with AI assistants
- **Security**: JWT-based authentication and authorization

## Architecture

- **Backend**: Python 3.11 with FastAPI
- **Database**: PostgreSQL (Neon Serverless)
- **ORM**: SQLModel
- **Protocol**: Model Context Protocol (MCP) for tool integration
- **Testing**: pytest for unit, integration, and security tests

## Technology Stack

- Python 3.11
- FastAPI 0.104+
- SQLModel 0.0.14+
- Pydantic 2.0+
- mcp python-sdk
- OpenAI Agents SDK
- asyncpg 0.29+
- PostgreSQL (Neon Serverless)

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

## Database Setup

1. Create a PostgreSQL database (Neon recommended)
2. Update the `DATABASE_URL` in your `.env` file:
   ```env
   DATABASE_URL="postgresql://your_username:your_password@ep-xxx.us-east-1.aws.neon.tech/chatbot_db?sslmode=require"
   ```
3. Run the database migrations to create the required tables:
   ```bash
   python backend/db.py  # Or use your migration system
   ```

## Running the Application

1. Start the MCP server:
   ```bash
   python -m backend.mcp_server.server
   ```

## MCP Tools

The application exposes 5 standardized task management tools via the Model Context Protocol:

### 1. add_task
Create a new task for a user
- Parameters: `user_id`, `title` (1-200 chars), `description` (optional, 0-1000 chars)

### 2. list_tasks
List tasks for a user with optional status filter
- Parameters: `user_id`, `status` (all, pending, completed)

### 3. complete_task
Mark a task as completed
- Parameters: `user_id`, `task_id`

### 4. delete_task
Delete a task
- Parameters: `user_id`, `task_id`

### 5. update_task
Update task title and/or description
- Parameters: `user_id`, `task_id`, `title` (optional), `description` (optional)

## Testing

Run the full test suite:
```bash
python -m pytest tests/ -v
```

Run specific test categories:
```bash
# Unit tests
python -m pytest tests/unit/

# Integration tests
python -m pytest tests/integration/

# Security tests
python -m pytest tests/security/
```

## Project Structure

```
backend/
├── models/                 # Database models (Conversation, Message, Task)
├── mcp_server/            # MCP server implementation
│   ├── server.py          # Main MCP server
│   ├── schemas.py         # Pydantic schemas for tools
│   └── tools/             # Individual MCP tools
│       ├── add_task.py
│       ├── list_tasks.py
│       ├── complete_task.py
│       ├── delete_task.py
│       └── update_task.py
├── db.py                  # Database connection
└── migrations/            # Database migrations

tests/
├── unit/                  # Unit tests for individual components
├── integration/           # Integration tests
└── security/              # Security tests
```

## Database Schema

### conversations table
- `id`: Primary key
- `user_id`: Foreign key to users table
- `created_at`: Timestamp
- `updated_at`: Timestamp

### messages table
- `id`: Primary key
- `conversation_id`: Foreign key to conversations table
- `user_id`: Foreign key to users table
- `role`: 'user' or 'assistant'
- `content`: Message text content
- `tool_calls`: JSONB for tool invocation metadata
- `created_at`: Timestamp

### tasks table
- `id`: Primary key
- `user_id`: Foreign key to users table
- `title`: Task title
- `description`: Optional task description
- `completed`: Boolean completion status
- `created_at`: Timestamp
- `updated_at`: Timestamp

## Security Features

- User data isolation: All queries filter by user_id
- Input validation: All parameters validated before database operations
- Error handling: Structured error responses without sensitive information
- Authentication: Designed for JWT-based authentication

## Development

To add new MCP tools:
1. Create a new tool in `backend/mcp_server/tools/`
2. Follow the same pattern as existing tools
3. Add corresponding unit and integration tests
4. Register the tool in the MCP server

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

[Specify your license here]