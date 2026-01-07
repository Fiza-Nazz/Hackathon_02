# Quickstart Guide: AI-Native Todo Application

## Phase I: Python Console Application

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Setup
1. Clone or create the project directory
2. Navigate to the project root
3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

### Running the Application
1. Navigate to the project root directory
2. Run the console application:
   ```bash
   python src/cli/todo_app.py
   ```

### Basic Usage
1. The application starts and displays a menu of available operations
2. Follow the on-screen prompts to:
   - Create a new task (provide title and optional description)
   - View all tasks (displays ID, title, and completion status)
   - Update an existing task (specify ID and new title/description)
   - Delete a task (specify ID)
   - Mark a task as complete/incomplete (specify ID)

### Example Workflow
1. Start the application: `python src/cli/todo_app.py`
2. Choose option 1 to create a task
3. Enter a title (required) and description (optional)
4. Choose option 2 to view all tasks
5. Choose option 5 to mark a task complete (specify ID)
6. Choose option 4 to delete a task (specify ID)

### Data Storage
- All data is stored in memory only
- Data is lost when the application terminates
- No persistent storage is used (as specified in requirements)

## Phase II: Web Application (Future)

The web application will be built using Next.js for the frontend and FastAPI for the backend after Phase I is complete.