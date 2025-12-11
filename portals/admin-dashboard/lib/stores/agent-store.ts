import { create } from 'zustand'

export interface Agent {
    id: string
    name: string
    description: string
    status: 'active' | 'inactive' | 'error' | 'starting'
    domain: string
    type: string
    performance: number // 0-100
    lastActive: string
}

export interface AgentStats {
    total: number
    active: number
    inactive: number
    error: number
    performance: number
}

interface AgentStore {
    agents: Agent[]
    isLoading: boolean
    error: string | null
    fetchAgents: () => Promise<void>
    getAgentStats: () => AgentStats
}

// Mock data
const MOCK_AGENTS: Agent[] = [
    {
        id: '1',
        name: 'Sales Assistant AI',
        description: 'Handles initial customer inquiries and lead qualification',
        status: 'active',
        domain: 'Sales',
        type: 'Conversational',
        performance: 92,
        lastActive: '2 mins ago'
    },
    {
        id: '2',
        name: 'Support Bot Alpha',
        description: 'Level 1 technical support and ticket triage',
        status: 'active',
        domain: 'Support',
        type: 'Conversational',
        performance: 88,
        lastActive: '5 mins ago'
    },
    {
        id: '3',
        name: 'Data Analyst Pro',
        description: 'Processes daily usage metrics and generates reports',
        status: 'inactive',
        domain: 'Analytics',
        type: 'Data Processing',
        performance: 95,
        lastActive: '12 hours ago'
    },
    {
        id: '4',
        name: 'Security Sentinel',
        description: 'Monitors system access logs for suspicious activity',
        status: 'active',
        domain: 'Security',
        type: 'Monitoring',
        performance: 99,
        lastActive: 'Just now'
    },
    {
        id: '5',
        name: 'Marketing Copywriter',
        description: 'Generates social media content drafts',
        status: 'error',
        domain: 'Marketing',
        type: 'Generative',
        performance: 75,
        lastActive: '1 day ago'
    }
]

export const useAgentStore = create<AgentStore>((set, get) => ({
    agents: [],
    isLoading: false,
    error: null,

    fetchAgents: async () => {
        set({ isLoading: true })
        try {
            // TODO: Replace with actual API call
            await new Promise(resolve => setTimeout(resolve, 1000))
            set({ agents: MOCK_AGENTS, isLoading: false })
        } catch (error) {
            set({ error: 'Failed to fetch agents', isLoading: false })
        }
    },

    getAgentStats: () => {
        const { agents } = get()
        const total = agents.length
        if (total === 0) {
            return { total: 0, active: 0, inactive: 0, error: 0, performance: 0 }
        }

        const active = agents.filter(a => a.status === 'active').length
        const inactive = agents.filter(a => a.status === 'inactive').length
        const error = agents.filter(a => a.status === 'error').length

        // Calculate average performance
        const totalPerformance = agents.reduce((sum, agent) => sum + agent.performance, 0)
        const avgPerformance = Math.round(totalPerformance / total)

        return {
            total,
            active,
            inactive,
            error,
            performance: avgPerformance
        }
    }
}))
