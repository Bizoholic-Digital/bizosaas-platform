// Brain API Client
// Handles communication with the Brain Gateway Service

const BRAIN_GATEWAY_URL = process.env.NEXT_PUBLIC_BRAIN_GATEWAY_URL || 'http://localhost:8000';

export interface Connector {
    id: string;
    name: string;
    type: string;
    icon: string;
    description: string;
    auth_schema?: any;
    status?: string;
}

export interface Agent {
    id: string;
    name: string;
    description: string;
    role: string;
    capabilities: string[];
    tools: string[];
    icon: string;
    color: string;
    status: 'active' | 'inactive';
    category: string;
    costTier: 'free' | 'standard' | 'premium';
}

export interface ChatResponse {
    agent_id: string;
    message: string;
    suggestions: string[];
    actions: any[];
}

export const brainApi = {
    connectors: {
        listTypes: async (): Promise<Connector[]> => {
            const res = await fetch(`${BRAIN_GATEWAY_URL}/api/connectors/types`);
            if (!res.ok) throw new Error('Failed to fetch connector types');
            return res.json();
        },
        connect: async (connectorId: string, credentials: any) => {
            const res = await fetch(`${BRAIN_GATEWAY_URL}/api/connectors/${connectorId}/connect`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(credentials)
            });
            if (!res.ok) {
                const error = await res.json();
                throw new Error(error.detail || 'Connection failed');
            }
            return res.json();
        },
        sync: async (connectorId: string, resource: string) => {
            const res = await fetch(`${BRAIN_GATEWAY_URL}/api/connectors/${connectorId}/sync/${resource}`);
            if (!res.ok) throw new Error('Sync failed');
            return res.json();
        },
        performAction: async (connectorId: string, action: string, payload: any) => {
            const res = await fetch(`${BRAIN_GATEWAY_URL}/api/connectors/${connectorId}/action/${action}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!res.ok) throw new Error('Action failed');
            return res.json();
        },
        getStatus: async (connectorId: string) => {
            // Note: tenant_id currently mocked as default_tenant on backend
            const res = await fetch(`${BRAIN_GATEWAY_URL}/api/connectors/${connectorId}/status`);
            if (!res.ok) return { status: 'disconnected' };
            return res.json();
        }
    },
    agents: {
        list: async (): Promise<Agent[]> => {
            const res = await fetch(`${BRAIN_GATEWAY_URL}/api/agents/`);
            if (!res.ok) throw new Error('Failed to fetch agents');
            const data = await res.json();
            // Map backend response to frontend Agent interface if needed
            return data.map((agent: any) => ({
                ...agent,
                status: 'active', // Backend doesn't return status yet, default to active
                category: 'general', // Default category
                costTier: 'standard' // Default tier
            }));
        },
        get: async (agentId: string): Promise<Agent> => {
            const res = await fetch(`${BRAIN_GATEWAY_URL}/api/agents/${agentId}`);
            if (!res.ok) throw new Error('Failed to fetch agent');
            const data = await res.json();
            return {
                ...data,
                status: 'active',
                category: 'general',
                costTier: 'standard'
            };
        },
        chat: async (agentId: string, message: string, context?: any): Promise<ChatResponse> => {
            const res = await fetch(`${BRAIN_GATEWAY_URL}/api/agents/${agentId}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, context })
            });
            if (!res.ok) throw new Error('Chat failed');
            return res.json();
        },
        updateConfig: async (agentId: string, config: any) => {
            // Placeholder: Backend doesn't support config update yet
            console.log(`[Mock] Updating config for agent ${agentId}`, config);
            return { success: true };
        },
        getHistory: async (agentId: string) => {
            const res = await fetch(`${BRAIN_GATEWAY_URL}/api/agents/${agentId}/history`);
            if (!res.ok) return [];
            return res.json();
        }
    },
    mcp: {
        listCategories: async (): Promise<any[]> => {
            const res = await fetch(`${BRAIN_GATEWAY_URL}/api/mcp/categories`);
            if (!res.ok) throw new Error('Failed to fetch categories');
            return res.json();
        },
        getRegistry: async (categorySlug?: string): Promise<any[]> => {
            const url = categorySlug
                ? `${BRAIN_GATEWAY_URL}/api/mcp/registry?category=${categorySlug}`
                : `${BRAIN_GATEWAY_URL}/api/mcp/registry`;
            const res = await fetch(url);
            if (!res.ok) throw new Error('Failed to fetch registry');
            return res.json();
        },
        install: async (mcpSlug: string, config?: any) => {
            const res = await fetch(`${BRAIN_GATEWAY_URL}/api/mcp/install`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mcp_slug: mcpSlug, config })
            });
            if (!res.ok) throw new Error('Installation failed');
            return res.json();
        }
    },
    cms: {
        listPages: async () => {
            const res = await fetch(`${BRAIN_GATEWAY_URL}/api/cms/pages`);
            if (!res.ok) return [];
            return res.json();
        },
        listPosts: async () => {
            const res = await fetch(`${BRAIN_GATEWAY_URL}/api/cms/posts`);
            if (!res.ok) return [];
            return res.json();
        },
        listMedia: async () => {
            const res = await fetch(`${BRAIN_GATEWAY_URL}/api/cms/media`);
            if (!res.ok) return [];
            return res.json();
        }
    }
};
