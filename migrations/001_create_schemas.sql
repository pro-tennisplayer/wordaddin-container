-- Migration: 001_create_schemas.sql
-- Description: Create initial schemas and tables for RAG memory and feedback

-- Create RAG Memory schema
CREATE SCHEMA IF NOT EXISTS rag_memory;

-- Create RAG Feedback schema
CREATE SCHEMA IF NOT EXISTS rag_feedback;

-- Create embeddings table in rag_memory schema
CREATE TABLE IF NOT EXISTS rag_memory.embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id VARCHAR(255) NOT NULL,
    project_id VARCHAR(255) NOT NULL,
    embedding JSONB NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    source VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create feedback entries table in rag_feedback schema
CREATE TABLE IF NOT EXISTS rag_feedback.entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    document_id UUID REFERENCES rag_memory.embeddings(id),
    feedback JSONB NOT NULL,
    signal VARCHAR(50) NOT NULL CHECK (signal IN ('positive', 'negative', 'neutral')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_embeddings_tenant_id ON rag_memory.embeddings(tenant_id);
CREATE INDEX IF NOT EXISTS idx_embeddings_project_id ON rag_memory.embeddings(project_id);
CREATE INDEX IF NOT EXISTS idx_embeddings_created_at ON rag_memory.embeddings(created_at);

CREATE INDEX IF NOT EXISTS idx_feedback_tenant_id ON rag_feedback.entries(tenant_id);
CREATE INDEX IF NOT EXISTS idx_feedback_user_id ON rag_feedback.entries(user_id);
CREATE INDEX IF NOT EXISTS idx_feedback_document_id ON rag_feedback.entries(document_id);
CREATE INDEX IF NOT EXISTS idx_feedback_signal ON rag_feedback.entries(signal);
CREATE INDEX IF NOT EXISTS idx_feedback_created_at ON rag_feedback.entries(created_at);

-- Add comments for documentation
COMMENT ON SCHEMA rag_memory IS 'Schema for storing RAG memory embeddings and content';
COMMENT ON SCHEMA rag_feedback IS 'Schema for storing user feedback on RAG responses';

COMMENT ON TABLE rag_memory.embeddings IS 'Stores vector embeddings and content for RAG memory';
COMMENT ON TABLE rag_feedback.entries IS 'Stores user feedback on RAG responses';

COMMENT ON COLUMN rag_memory.embeddings.tenant_id IS 'Multi-tenant identifier';
COMMENT ON COLUMN rag_memory.embeddings.project_id IS 'Project identifier within tenant';
COMMENT ON COLUMN rag_memory.embeddings.embedding IS 'Vector embedding as JSONB array';
COMMENT ON COLUMN rag_memory.embeddings.content IS 'Original content text';
COMMENT ON COLUMN rag_memory.embeddings.metadata IS 'Additional metadata as JSONB';
COMMENT ON COLUMN rag_memory.embeddings.source IS 'Source of the content';

COMMENT ON COLUMN rag_feedback.entries.tenant_id IS 'Multi-tenant identifier';
COMMENT ON COLUMN rag_feedback.entries.user_id IS 'User identifier within tenant';
COMMENT ON COLUMN rag_feedback.entries.document_id IS 'Reference to the embedding document';
COMMENT ON COLUMN rag_feedback.entries.feedback IS 'Feedback data as JSONB';
COMMENT ON COLUMN rag_feedback.entries.signal IS 'Feedback signal (positive/negative/neutral)';
