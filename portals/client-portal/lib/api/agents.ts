import { brainApi, ApiResponse } from './brain-client';

export interface AgentConfig {
    id: string;
    name: string;
    description: string;
    role: string;
    capabilities: string[];
    tools: string[];
    icon: string;
    color: string;
    category?: string;
}

export interface AgentTaskRequest {
    agent_id: string;
    task_description: string;
    input_data: Record<string, any>;
    priority?: 'low' | 'normal' | 'high' | 'urgent';
}

export interface AgentTaskResponse {
    task_id: string;
    status: 'pending' | 'running' | 'completed' | 'failed';
    result_data?: any;
    error_message?: string;
}

export const agentsApi = {
    getAgents: (): Promise<ApiResponse<AgentConfig[]>> =>
        brainApi.get('/api/brain/agents/'),

    getAgent: (agentId: string): Promise<ApiResponse<AgentConfig>> =>
        brainApi.get(`/api/brain/agents/${agentId}/`),

    createAgent: (agent: Partial<AgentConfig> & { instructions: string }): Promise<ApiResponse<AgentConfig>> =>
        brainApi.post('/api/brain/agents/', agent),

    executeTask: (request: AgentTaskRequest): Promise<ApiResponse<AgentTaskResponse>> =>
        brainApi.post(`/api/brain/agents/${request.agent_id}/task/`, request),

    getTaskStatus: (taskId: string): Promise<ApiResponse<AgentTaskResponse>> =>
        brainApi.get(`/api/brain/tasks/${taskId}/`),

    getAgentHistory: (agentId: string): Promise<ApiResponse<any[]>> =>
        brainApi.get(`/api/brain/agents/${agentId}/history/`)
};
