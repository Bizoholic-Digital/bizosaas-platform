import { brainClient as brainApi, ApiResponse } from './brain-client';

export interface AgentNode {
    id: string;
    name: string;
    role: string;
    status: 'active' | 'idle' | 'error';
    type: 'supervisor' | 'specialist';
}

export interface AgentEdge {
    from: string;
    to: string;
    action: string;
    status: 'active' | 'pending' | 'success';
}

export interface AgentMesh {
    nodes: AgentNode[];
    edges: AgentEdge[];
}

// Backend Agent Interface
interface Agent {
    id: string;
    name: string;
    description: string;
    role: string;
    category: string;
    status?: string;
    tools: string[];
}

export class AgentsApi {
    async getAgentMesh(): Promise<ApiResponse<AgentMesh>> {
        try {
            // 1. Fetch real agents from backend
            const response = await brainApi.get<Agent[]>('/agents/');

            if (response.error || !response.data) {
                return { error: response.error || 'Failed to fetch agents', data: undefined };
            }

            const agents = response.data;
            const nodes: AgentNode[] = [];
            const edges: AgentEdge[] = [];

            // 2. Identify Orchestrator (Mock logic if not explicit)
            const orchestratorId = 'master_orchestrator';

            // 3. Map Agents to Nodes
            agents.forEach(agent => {
                const isOrchestrator = agent.id === orchestratorId;
                // Supervisor heuristic: "Manager", "Strategist", "Head" in role or Orchestrator
                const isSupervisor = isOrchestrator ||
                    agent.role.includes('Manager') ||
                    agent.role.includes('Strategist') ||
                    agent.role.includes('Head') ||
                    agent.role.includes('Director');

                nodes.push({
                    id: agent.id,
                    name: agent.name,
                    role: agent.role,
                    status: (agent.status as any) || 'active', // Default to active
                    type: isSupervisor ? 'supervisor' : 'specialist'
                });

                // 4. Create Edges (Heuristic for demo visualization)
                if (!isOrchestrator) {
                    // Connect Orchestrator to Supervisors
                    if (isSupervisor) {
                        const orchestratorNode = agents.find(a => a.id === orchestratorId);
                        if (orchestratorNode) {
                            edges.push({
                                from: orchestratorId,
                                to: agent.id,
                                action: 'Delegate Task',
                                status: 'success'
                            });
                        }
                    }
                }
            });

            // Connect Supervisors to Specialists (Mock logic based on category)
            const supervisors = nodes.filter(n => n.type === 'supervisor' && n.id !== orchestratorId);
            const specialists = nodes.filter(n => n.type === 'specialist');

            supervisors.forEach(sup => {
                // Find specialists in same/related category - simplified by just picking random or doing string matching
                // For now, let's just connect supervisors to specialists if they share some keyword in role or Id
                specialists.forEach(spec => {
                    // Simple heuristic: if supervisor is 'Marketing Strategist' and specialist is 'Content Creator'
                    if (
                        (sup.id.includes('marketing') && spec.id.includes('content')) ||
                        (sup.id.includes('sales') && spec.id.includes('crm')) ||
                        (sup.id.includes('customer') && spec.id.includes('support')) ||
                        (sup.role.includes('Marketing') && spec.role.includes('Content'))
                    ) {
                        edges.push({
                            from: sup.id,
                            to: spec.id,
                            action: 'Coordinate',
                            status: 'active'
                        });
                    }
                });
            });

            return { data: { nodes, edges } };

        } catch (e: any) {
            return { error: e.message };
        }
    }

    async getAgentLogs(agentId: string): Promise<ApiResponse<any[]>> {
        return brainApi.get<any[]>(`/agents/${agentId}/history`);
    }

    async updateAgentConfig(agentId: string, config: any): Promise<ApiResponse<any>> {
        return brainApi.post<any>(`/agents/`, { id: agentId, ...config }); // Backend create/update is POST /agents/ for now? Adjust if needed
    }
}

export const agentsApi = new AgentsApi();

