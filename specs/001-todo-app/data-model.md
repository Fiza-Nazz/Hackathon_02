# Data Model: AI-Native Todo Application

## Task Entity

### Attributes
- **id**: Integer (required, unique, auto-generated)
  - Primary identifier for the task
  - Sequential integer starting from 1
  - Generated automatically when a task is created

- **title**: String (required)
  - The main text of the task
  - Must not be empty or null
  - Maximum length: 255 characters

- **description**: String (optional)
  - Additional details about the task
  - Can be null or empty string
  - Maximum length: 1000 characters

- **completed**: Boolean (required)
  - Indicates whether the task is completed
  - Default value: false (incomplete)
  - Can be toggled between true and false

### Validation Rules
- Title must be provided (not empty or null)
- Title must be between 1 and 255 characters
- Description, if provided, must be between 1 and 1000 characters
- ID must be unique within the task collection
- ID must be a positive integer

### State Transitions
- **Creation**: New task is created with `completed = false`
- **Update**: Task attributes (title, description) can be modified
- **Toggle Completion**: `completed` status toggles between true/false
- **Deletion**: Task is removed from the collection

## Task Collection (In-Memory Storage)

### Structure
- **tasks**: Dictionary/Map with ID as key and Task object as value
  - Provides O(1) lookup by ID
  - Maintains uniqueness of task IDs
  - Stored in memory for Phase I as required by specification

### Operations
- **Add Task**: Insert a new task with auto-generated unique ID
- **Get Task**: Retrieve a task by its ID
- **Update Task**: Modify existing task attributes
- **Delete Task**: Remove a task by its ID
- **List Tasks**: Retrieve all tasks in the collection
- **Find Tasks**: Search/filter tasks based on criteria (e.g., completed status)

### Constraints
- All data remains in memory only (no persistence)
- Collection is reset when application terminates
- Maximum reasonable size limited by available memory