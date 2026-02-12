-- PHASE V DATABASE SCHEMA UPDATES
-- Advanced Features: Priorities, Due Dates, Recurring Tasks, Tags

-- Add new columns to existing tasks table
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS priority VARCHAR(10) DEFAULT 'medium';
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS due_date TIMESTAMP NULL;
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurring_pattern VARCHAR(20) NULL;
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurring_interval INTEGER DEFAULT 1;
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS parent_task_id INTEGER NULL;
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT FALSE;

-- Create task_tags table for many-to-many relationship
CREATE TABLE IF NOT EXISTS task_tags (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    tag_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(task_id, tag_name)
);

-- Create tags table for tag management
CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    color VARCHAR(7) DEFAULT '#3B82F6', -- Default blue color
    user_id VARCHAR(255) NOT NULL,
    usage_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create reminders table for scheduled notifications
CREATE TABLE IF NOT EXISTS reminders (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    user_id VARCHAR(255) NOT NULL,
    remind_at TIMESTAMP NOT NULL,
    reminder_type VARCHAR(20) DEFAULT 'due_date', -- 'due_date', 'custom'
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'sent', 'cancelled'
    message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create audit_log table for event tracking
CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    aggregate_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    event_data JSONB NOT NULL,
    correlation_id UUID,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Add foreign key constraint for parent task
ALTER TABLE tasks ADD CONSTRAINT IF NOT EXISTS fk_parent_task 
    FOREIGN KEY (parent_task_id) REFERENCES tasks(id) ON DELETE SET NULL;

-- Create indexes after tables are created
CREATE INDEX IF NOT EXISTS idx_task_tags_task_id ON task_tags(task_id);
CREATE INDEX IF NOT EXISTS idx_task_tags_name ON task_tags(tag_name);
CREATE INDEX IF NOT EXISTS idx_reminders_task_id ON reminders(task_id);
CREATE INDEX IF NOT EXISTS idx_reminders_user_id ON reminders(user_id);
CREATE INDEX IF NOT EXISTS idx_reminders_remind_at ON reminders(remind_at);
CREATE INDEX IF NOT EXISTS idx_reminders_status ON reminders(status);
CREATE INDEX IF NOT EXISTS idx_audit_log_event_type ON audit_log(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_log_aggregate_id ON audit_log(aggregate_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON audit_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_tags_user_id ON tags(user_id);
CREATE INDEX IF NOT EXISTS idx_tags_name ON tags(name);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
CREATE INDEX IF NOT EXISTS idx_tasks_user_id_status ON tasks(user_id, completed);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at);

-- Insert default tags if not exists
INSERT INTO tags (name, color, user_id, usage_count) VALUES
    ('work', '#EF4444', 'system', 0),
    ('personal', '#10B981', 'system', 0),
    ('urgent', '#F59E0B', 'system', 0),
    ('important', '#8B5CF6', 'system', 0)
ON CONFLICT (name) DO NOTHING;

-- Update existing tasks to have default priority if NULL
UPDATE tasks SET priority = 'medium' WHERE priority IS NULL;