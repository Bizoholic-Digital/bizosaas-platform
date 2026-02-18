/**
 * Agents API Client
 * Handles all AI agent-related API operations
 */

import { apiClient } from '../utils/base-client'
import type {
    Agent,
    AgentCreate,
    AgentUpdate,
    AgentOptimization,
    ApiResponse,
} from '../types'

export class AgentsClient {
    private basePath = '/api/agents'

    /**
     * List all available AI agents (System + Custom)
     */
    async list(): Promise<Agent[]> {
        return apiClient.get<Agent[]>(this.basePath)
    }

    /**
     * Get a single agent by ID
     */
    async get(agentId: string): Promise<Agent> {
        return apiClient.get<Agent>(`${this.basePath}/${agentId}`)
    }

    /**
     * Create a new custom AI agent
     */
    async create(data: AgentCreate): Promise<Agent> {
        return apiClient.post<Agent>(this.basePath, data)
    }

    /**
     * Update an existing custom agent
     */
    async update(agentId: string, data: AgentUpdate): Promise<Agent> {
        return apiClient.put<Agent>(`${this.basePath}/${agentId}`, data)
    }

    /**
     * Delete a custom agent
     */
    async delete(agentId: string): Promise<void> {
        return apiClient.delete<void>(`${this.basePath}/${agentId}`)
    }

    /**
     * List AI-suggested optimizations for agents
     */
    async listOptimizations(agentId?: string): Promise<{ optimizations: AgentOptimization[] }> {
        const params = agentId ? { agent_id: agentId } : {}
        return apiClient.get<{ optimizations: AgentOptimization[] }>(`${this.basePath}/optimizations`, { params })
    }

    /**
     * Approve an optimization for execution
     */
    async approveOptimization(optId: string): Promise<any> {
        return apiClient.post(`${this.basePath}/optimizations/${optId}/approve`)
    }

    /**
     * Get agent performance metrics
     */
    async getMetrics(agentId: string): Promise<any> {
        return apiClient.get(`${this.basePath}/${agentId}/metrics`)
    }
}

export const agentsClient = new AgentsClient()
