import { brainClient as brainApi, ApiResponse } from './brain-client';

export interface AgentNode {
    id: string;
    name: string;
    type: string;
    status: 'active' | 'idle' | 'warning' | 'error';
    health: number;
}

export interface AgentEdge {
    from: string;
    to: string;
    type: string;
}

export interface AgentMesh {
    nodes: AgentNode[];
    edges: AgentEdge[];
}

export class AgentsApi {
    async getAgentMesh(): Promise<ApiResponse<AgentMesh>> {
        return brainApi.get<AgentMesh>('/agents/mesh');
    }

    async getAgentLogs(agentId: string): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>(`/agents/${agentId}/logs`);
    }

    async updateAgentConfig(agentId: string, config: any): Promise<ApiResponse<any>> {
        return brainApi.post<any>(`/agents/${agentId}/config`, config);
    }
}

export const agentsApi = new AgentsApi();
