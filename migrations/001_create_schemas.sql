-- =====================================================
-- Apex MVP Database Schema
-- Creates schemas for RAG feedback and chat memory
-- =====================================================

-- Create schemas
CREATE SCHEMA IF NOT EXISTS rag_feedback;
CREATE SCHEMA IF NOT EXISTS chat_memory;

-- =====================================================
-- RAG FEEDBACK SCHEMA
-- Stores user feedback on RAG responses
-- =====================================================

CREATE TABLE IF NOT EXISTS rag_feedback.entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    tenant_id VARCHAR(255) NOT NULL,
    project_id VARCHAR(255),
    document_id VARCHAR(255),
    query TEXT NOT NULL,
    result TEXT NOT NULL,
    user_feedback VARCHAR(10) NOT NULL CHECK (user_feedback IN ('thumbs_up', 'thumbs_down')),
    feedback_note TEXT,
    signal_strength INTEGER DEFAULT 1 CHECK (signal_strength >= 1 AND signal_strength <= 10),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_rag_feedback_user_id ON rag_feedback.entries(user_id);
CREATE INDEX IF NOT EXISTS idx_rag_feedback_tenant_id ON rag_feedback.entries(tenant_id);
CREATE INDEX IF NOT EXISTS idx_rag_feedback_project_id ON rag_feedback.entries(project_id);
CREATE INDEX IF NOT EXISTS idx_rag_feedback_document_id ON rag_feedback.entries(document_id);
CREATE INDEX IF NOT EXISTS idx_rag_feedback_created_at ON rag_feedback.entries(created_at);
CREATE INDEX IF NOT EXISTS idx_rag_feedback_user_feedback ON rag_feedback.entries(user_feedback);

-- Composite indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_rag_feedback_user_tenant ON rag_feedback.entries(user_id, tenant_id);
CREATE INDEX IF NOT EXISTS idx_rag_feedback_project_tenant ON rag_feedback.entries(project_id, tenant_id);

-- =====================================================
-- CHAT MEMORY SCHEMA  
-- Stores conversation history for RAG context
-- =====================================================

CREATE TABLE IF NOT EXISTS chat_memory.conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    tenant_id VARCHAR(255) NOT NULL,
    project_id VARCHAR(255),
    session_id VARCHAR(255),
    conversation_title VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chat_memory.messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES chat_memory.conversations(id) ON DELETE CASCADE,
    user_id VARCHAR(255) NOT NULL,
    tenant_id VARCHAR(255) NOT NULL,
    message_type VARCHAR(20) NOT NULL CHECK (message_type IN ('user_query', 'rag_response', 'system_message')),
    content TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chat_memory.rag_queries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    tenant_id VARCHAR(255) NOT NULL,
    project_id VARCHAR(255),
    conversation_id UUID REFERENCES chat_memory.conversations(id) ON DELETE SET NULL,
    query TEXT NOT NULL,
    result TEXT NOT NULL,
    source_documents JSONB,
    confidence_score DECIMAL(3,2) CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0),
    processing_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for chat memory tables
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON chat_memory.conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_tenant_id ON chat_memory.conversations(tenant_id);
CREATE INDEX IF NOT EXISTS idx_conversations_project_id ON chat_memory.conversations(project_id);
CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON chat_memory.conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON chat_memory.conversations(created_at);

CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON chat_memory.messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_user_id ON chat_memory.messages(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_tenant_id ON chat_memory.messages(tenant_id);
CREATE INDEX IF NOT EXISTS idx_messages_message_type ON chat_memory.messages(message_type);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON chat_memory.messages(created_at);

CREATE INDEX IF NOT EXISTS idx_rag_queries_user_id ON chat_memory.rag_queries(user_id);
CREATE INDEX IF NOT EXISTS idx_rag_queries_tenant_id ON chat_memory.rag_queries(tenant_id);
CREATE INDEX IF NOT EXISTS idx_rag_queries_project_id ON chat_memory.rag_queries(project_id);
CREATE INDEX IF NOT EXISTS idx_rag_queries_conversation_id ON chat_memory.rag_queries(conversation_id);
CREATE INDEX IF NOT EXISTS idx_rag_queries_created_at ON chat_memory.rag_queries(created_at);

-- Composite indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_conversations_user_tenant ON chat_memory.conversations(user_id, tenant_id);
CREATE INDEX IF NOT EXISTS idx_messages_user_tenant ON chat_memory.messages(user_id, tenant_id);
CREATE INDEX IF NOT EXISTS idx_rag_queries_user_tenant ON chat_memory.rag_queries(user_id, tenant_id);

-- =====================================================
-- HELPER FUNCTIONS
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers to automatically update updated_at
CREATE TRIGGER update_rag_feedback_updated_at 
    BEFORE UPDATE ON rag_feedback.entries 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_conversations_updated_at 
    BEFORE UPDATE ON chat_memory.conversations 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- SAMPLE DATA INSERTS (for testing)
-- =====================================================

-- Insert sample RAG feedback
INSERT INTO rag_feedback.entries (user_id, tenant_id, project_id, query, result, user_feedback, feedback_note) VALUES
('user123', 'tenant1', 'project1', 'What is machine learning?', 'Machine learning is a subset of AI...', 'thumbs_up', 'Great explanation!'),
('user456', 'tenant2', 'project2', 'How to implement authentication?', 'Authentication can be implemented using...', 'thumbs_down', 'Need more code examples');

-- Insert sample conversation
INSERT INTO chat_memory.conversations (user_id, tenant_id, project_id, session_id, conversation_title) VALUES
('user123', 'tenant1', 'project1', 'session001', 'Machine Learning Discussion');

-- Insert sample messages
INSERT INTO chat_memory.messages (conversation_id, user_id, tenant_id, message_type, content) VALUES
((SELECT id FROM chat_memory.conversations WHERE session_id = 'session001'), 'user123', 'tenant1', 'user_query', 'What is machine learning?'),
((SELECT id FROM chat_memory.conversations WHERE session_id = 'session001'), 'user123', 'tenant1', 'rag_response', 'Machine learning is a subset of AI...');

-- Insert sample RAG query
INSERT INTO chat_memory.rag_queries (user_id, tenant_id, project_id, conversation_id, query, result, confidence_score) VALUES
('user123', 'tenant1', 'project1', (SELECT id FROM chat_memory.conversations WHERE session_id = 'session001'), 'What is machine learning?', 'Machine learning is a subset of AI...', 0.95);

-- =====================================================
-- COMMENTS
-- =====================================================

COMMENT ON SCHEMA rag_feedback IS 'Schema for storing user feedback on RAG responses';
COMMENT ON SCHEMA chat_memory IS 'Schema for storing conversation history and RAG query context';

COMMENT ON TABLE rag_feedback.entries IS 'User feedback entries for RAG responses';
COMMENT ON TABLE chat_memory.conversations IS 'Conversation sessions for chat history';
COMMENT ON TABLE chat_memory.messages IS 'Individual messages within conversations';
COMMENT ON TABLE chat_memory.rag_queries IS 'RAG queries and responses for context retrieval';

COMMENT ON COLUMN rag_feedback.entries.signal_strength IS 'User confidence in feedback (1-10 scale)';
COMMENT ON COLUMN chat_memory.rag_queries.confidence_score IS 'RAG system confidence in response (0.0-1.0)';
COMMENT ON COLUMN chat_memory.rag_queries.source_documents IS 'JSON array of source documents used for response';
COMMENT ON COLUMN chat_memory.rag_queries.processing_time_ms IS 'Time taken to process RAG query in milliseconds';
