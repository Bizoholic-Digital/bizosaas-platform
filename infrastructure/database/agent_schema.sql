-- AI Agent Ecosystem - Core Database Schemas
-- Target: PostgreSQL / Neon DB

-- 1. Agents Registry & Configuration
CREATE TABLE IF NOT EXISTS meta_agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id TEXT UNIQUE NOT NULL, -- e.g., 'market_research_001'
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    category TEXT NOT NULL, -- e.g., 'Business Intelligence'
    status TEXT NOT NULL DEFAULT 'idle', -- active, idle, error, maintenance
    priority TEXT NOT NULL DEFAULT 'medium',
    config JSONB NOT NULL DEFAULT '{}', -- Fine-tuning parameters, modes
    capabilities TEXT[] DEFAULT '{}',
    tools TEXT[] DEFAULT '{}',
    performance_metrics JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Workflow Definitions (Templates)
CREATE TABLE IF NOT EXISTS meta_workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id TEXT UNIQUE NOT NULL, -- e.g., 'content_creation_wf'
    name TEXT NOT NULL,
    description TEXT,
    steps JSONB NOT NULL, -- Sequential/Parallel DAG definition
    triggers JSONB DEFAULT '[]', -- Scheduled, API, Event based
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Workflow Executions & Logs
CREATE TABLE IF NOT EXISTS meta_workflow_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    execution_id TEXT UNIQUE NOT NULL, -- External ID from Temporal/system
    workflow_id UUID REFERENCES meta_workflows(id),
    tenant_id TEXT NOT NULL,
    status TEXT NOT NULL, -- running, completed, failed, terminated
    input_data JSONB DEFAULT '{}',
    output_data JSONB DEFAULT '{}',
    error_log TEXT,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_ms INTEGER,
    cost_estimate DECIMAL(10, 4) DEFAULT 0.0000
);

-- 4. Agent Execution Logs (Audit Trail)
CREATE TABLE IF NOT EXISTS meta_agent_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    execution_id UUID REFERENCES meta_workflow_executions(id),
    agent_id UUID REFERENCES meta_agents(id),
    action TEXT NOT NULL,
    status TEXT NOT NULL,
    input_context JSONB,
    output_result JSONB,
    tokens_used INTEGER DEFAULT 0,
    cost_estimate DECIMAL(10, 4) DEFAULT 0.0000,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tenant/User Agent Permissions
CREATE TABLE IF NOT EXISTS meta_agent_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    agent_id UUID REFERENCES meta_agents(id),
    permission_level TEXT NOT NULL, -- read, execute, configure, admin
    granted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(tenant_id, user_id, agent_id)
);

-- 6. Analytics & Performance Aggregation
CREATE TABLE IF NOT EXISTS meta_agent_analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES meta_agents(id),
    period_start TIMESTAMP WITH TIME ZONE NOT NULL,
    period_end TIMESTAMP WITH TIME ZONE NOT NULL,
    total_tasks INTEGER DEFAULT 0,
    success_rate DECIMAL(5, 4),
    avg_response_time_ms INTEGER,
    total_tokens INTEGER DEFAULT 0,
    total_cost DECIMAL(10, 4) DEFAULT 0.0000,
    UNIQUE(agent_id, period_start, period_end)
);

-- Indexes for performance
CREATE INDEX idx_agents_category ON meta_agents(category);
CREATE INDEX idx_agents_status ON meta_agents(status);
CREATE INDEX idx_executions_tenant ON meta_workflow_executions(tenant_id);
CREATE INDEX idx_executions_status ON meta_workflow_executions(status);
CREATE INDEX idx_logs_agent ON meta_agent_logs(agent_id);
CREATE INDEX idx_logs_execution ON meta_agent_logs(execution_id);
