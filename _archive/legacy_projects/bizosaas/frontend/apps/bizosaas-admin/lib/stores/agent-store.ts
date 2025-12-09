import { create } from 'zustand';

// Simplified Agent type for UI components
export interface SimpleAgent {
  id: string;
  name: string;
  status: 'active' | 'inactive' | 'error' | 'starting' | 'stopping';
  type: string;
  lastActive: string;
  description?: string;
  domain?: string;
  performance?: number;
  children?: SimpleAgent[];
  tasksCompleted?: number;
  successRate?: number;
  avgResponseTime?: number;
  errorRate?: number;
  uptime?: number;
}

interface AgentStore {
  agents: SimpleAgent[];
  isLoading: boolean;
  error: string | null;
  fetchAgents: () => Promise<void>;
  getAgentStats: () => { total: number; active: number; inactive: number; error: number; performance: number };
  addAgent: (agent: SimpleAgent) => void;
  updateAgent: (id: string, updates: Partial<SimpleAgent>) => void;
}

export const useAgentStore = create<AgentStore>((set, get) => ({
  agents: [],
  isLoading: false,
  error: null,
  fetchAgents: async () => {
    set({ isLoading: true });
    try {
      // Mock fetch
      await new Promise(resolve => setTimeout(resolve, 1000));
      set({ 
        agents: [
          { id: '1', name: 'Sales Agent', status: 'active', type: 'specialist', lastActive: new Date().toISOString() },
          { id: '2', name: 'Support Agent', status: 'inactive', type: 'specialist', lastActive: new Date().toISOString() }
        ], 
        isLoading: false 
      });
    } catch (error) {
      set({ error: 'Failed to fetch agents', isLoading: false });
    }
  },
  getAgentStats: () => {
    const state = get();
    const activeAgents = state.agents.filter((a: SimpleAgent) => a.status === 'active');
    const inactiveAgents = state.agents.filter((a: SimpleAgent) => a.status === 'inactive' || a.status === 'stopping');
    return {
      total: state.agents.length,
      active: activeAgents.length,
      inactive: inactiveAgents.length,
      error: state.agents.filter((a: SimpleAgent) => a.status === 'error').length,
      performance: state.agents.length > 0 ? Math.round((activeAgents.length / state.agents.length) * 100) : 0
    };
  },
  addAgent: (agent) => set((state) => ({ agents: [...state.agents, agent] })),
  updateAgent: (id, updates) => set((state) => ({
    agents: state.agents.map((agent) => 
      agent.id === id ? { ...agent, ...updates } : agent
    )
  }))
}));
