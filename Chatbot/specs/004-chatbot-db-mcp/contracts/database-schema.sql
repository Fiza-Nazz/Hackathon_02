-- Database Schema for Conversational AI Chatbot Foundation
-- Feature: 004-chatbot-db-mcp
-- Migration: 003_add_conversation_tables
-- Database: PostgreSQL (Neon Serverless)
-- Date: 2026-01-09

-- ============================================
-- EXISTING TABLES (Phase 2)
-- ============================================

-- Users table (managed by Better Auth)
-- Created in Phase 2 - do NOT recreate
-- Schema:
--   id VARCHAR(255) PRIMARY KEY
--   email VARCHAR(255) UNIQUE NOT NULL
--   name VARCHAR(255) NOT NULL
--   created_at TIMESTAMP NOT NULL DEFAULT NOW()

-- Tasks table
-- Created in Phase 2 - do NOT recreate
-- Schema:
--   id SERIAL PRIMARY KEY
--   user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE
--   title VARCHAR(200) NOT NULL
--   description TEXT
--   completed BOOLEAN NOT NULL DEFAULT FALSE
--   created_at TIMESTAMP NOT NULL DEFAULT NOW()
--   updated_at TIMESTAMP NOT NULL DEFAULT NOW()

-- ============================================
-- NEW TABLES (Phase 3)
-- ============================================

-- Conversation table: Represents a chat session between user and AI
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_conversation_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- Index for efficient user conversation queries (sorted by newest first)
CREATE INDEX IF NOT EXISTS idx_user_conversations
    ON conversations(user_id, created_at DESC);

-- Message table: Represents individual messages in a conversation
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    tool_calls JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_message_conversation
        FOREIGN KEY (conversation_id)
        REFERENCES conversations(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_message_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- Index for efficient message retrieval per conversation (chronological order)
CREATE INDEX IF NOT EXISTS idx_conversation_messages
    ON messages(conversation_id, created_at ASC);

-- Index for direct user message queries without joins
CREATE INDEX IF NOT EXISTS idx_user_messages
    ON messages(user_id, created_at DESC);

-- ============================================
-- CASCADE DELETION BEHAVIOR
-- ============================================

-- 1. When a user is deleted:
--    - All their conversations are deleted CASCADE
--    - All their tasks are deleted CASCADE
--    - All their messages are deleted CASCADE (via conversation deletion)

-- 2. When a conversation is deleted:
--    - All messages in that conversation are deleted CASCADE

-- ============================================
-- CONSTRAINTS & VALIDATION
-- ============================================

-- Role constraint (enforced by CHECK constraint):
--   - Only 'user' or 'assistant' allowed in messages.role

-- Foreign key constraints:
--   - All conversations must belong to a valid user
--   - All messages must belong to a valid conversation
--   - All messages must belong to a valid user (redundant for query optimization)

-- ============================================
-- SAMPLE QUERIES
-- ============================================

-- Get all conversations for a user (newest first):
-- SELECT * FROM conversations
-- WHERE user_id = 'user_abc123'
-- ORDER BY created_at DESC;

-- Get all messages for a conversation (chronological order):
-- SELECT * FROM messages
-- WHERE conversation_id = 123
-- ORDER BY created_at ASC;

-- Create a new conversation:
-- INSERT INTO conversations (user_id) VALUES ('user_abc123');

-- Add a message to a conversation:
-- INSERT INTO messages (conversation_id, user_id, role, content)
-- VALUES (123, 'user_abc123', 'user', 'Hello AI assistant!');

-- ============================================
-- MIGRATION COMMANDS
-- ============================================

-- Apply migration (up):
--   psql $DATABASE_URL < 003_add_conversation_tables.sql
--   OR
--   python backend/migrations/003_add_conversation_tables.py upgrade

-- Rollback migration (down):
--   DROP TABLE IF EXISTS messages CASCADE;
--   DROP TABLE IF EXISTS conversations CASCADE;
--   OR
--   python backend/migrations/003_add_conversation_tables.py downgrade
