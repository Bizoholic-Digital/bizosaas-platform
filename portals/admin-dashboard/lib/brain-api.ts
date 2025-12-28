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

const apiFetch = async (endpoint: string, options: any = {}, token?: string) => {
    let authToken = token;

    // Auto-retrieve token from Clerk if not provided (Client-side only)
    if (!authToken && typeof window !== 'undefined') {
        try {
            // @ts-ignore
            authToken = await window.Clerk?.session?.getToken();
        } catch (e) {
            console.warn('[BrainAPI] Failed to auto-retrieve Clerk token', e);
        }
    }

    const headers = {
        'Content-Type': 'application/json',
        ...(authToken ? { 'Authorization': `Bearer ${authToken}` } : {}),
        ...options.headers,
    };

    const baseUrl = typeof window !== 'undefined' ? '/api/brain' : BRAIN_GATEWAY_URL;

    // Strip /api prefix if using proxied baseUrl to avoid double prefixing
    const sanitizedEndpoint = (typeof window !== 'undefined' && endpoint.startsWith('/api'))
        ? endpoint.substring(4)
        : endpoint;

    const fetchUrl = `${baseUrl}${sanitizedEndpoint}`;

    if (process.env.NODE_ENV === 'development') {
        console.log(`[BrainAPI] Fetching: ${fetchUrl}`, { method: options.method || 'GET' });
    }

    const res = await fetch(fetchUrl, {
        ...options,
        headers,
    });


    if (!res.ok) {
        // Handle 401/403 specifically if needed
        if (res.status === 401) {
            console.error('[BrainAPI] Unauthorized access to Brain Gateway');
        }

        let errorDetail = 'API request failed';
        try {
            const errorData = await res.json();
            errorDetail = errorData.detail || errorData.message || `Error ${res.status}: ${res.statusText}`;
        } catch (e) {
            errorDetail = `Error ${res.status}: ${res.statusText}`;
            // If it's a 404/500 with HTML body, log it
            console.warn(`[BrainAPI] Non-JSON error response from ${fetchUrl}`, res.status);
        }

        throw new Error(errorDetail);
    }

    return res.json();
};

export const brainApi = {
    connectors: {
        listTypes: async (token?: string): Promise<Connector[]> => {
            return apiFetch('/api/connectors/types', {}, token);
        },
        connect: async (connectorId: string, credentials: any, token?: string) => {
            return apiFetch(`/api/connectors/${connectorId}/connect`, {
                method: 'POST',
                body: JSON.stringify(credentials)
            }, token);
        },
        sync: async (connectorId: string, resource: string, token?: string) => {
            return apiFetch(`/api/connectors/${connectorId}/sync/${resource}`, {}, token);
        },
        performAction: async (connectorId: string, action: string, payload: any, token?: string) => {
            return apiFetch(`/api/connectors/${connectorId}/action/${action}`, {
                method: 'POST',
                body: JSON.stringify(payload)
            }, token);
        },
        getStatus: async (connectorId: string, token?: string) => {
            try {
                return await apiFetch(`/api/connectors/${connectorId}/status`, {}, token);
            } catch (e) {
                return { status: 'disconnected' };
            }
        }
    },
    agents: {
        list: async (token?: string): Promise<Agent[]> => {
            const data = await apiFetch('/api/agents', {}, token);
            return data.map((agent: any) => ({
                ...agent,
                status: 'active',
                category: 'general',
                costTier: 'standard'
            }));
        },
        get: async (agentId: string, token?: string): Promise<Agent> => {
            const data = await apiFetch(`/api/agents/${agentId}`, {}, token);
            return {
                ...data,
                status: 'active',
                category: 'general',
                costTier: 'standard'
            };
        },
        chat: async (agentId: string, message: string, context?: any, token?: string): Promise<ChatResponse> => {
            return apiFetch(`/api/agents/${agentId}/chat`, {
                method: 'POST',
                body: JSON.stringify({ message, context })
            }, token);
        },
        updateConfig: async (agentId: string, config: any, token?: string) => {
            return { success: true };
        },
        getHistory: async (agentId: string, token?: string) => {
            try {
                return await apiFetch(`/api/agents/${agentId}/history`, {}, token);
            } catch (e) {
                return [];
            }
        }
    },
    mcp: {
        listCategories: async (token?: string): Promise<any[]> => {
            return apiFetch('/api/mcp/categories', {}, token);
        },
        getRegistry: async (categorySlug?: string, token?: string): Promise<any[]> => {
            const path = categorySlug
                ? `/api/mcp/registry?category=${categorySlug}`
                : '/api/mcp/registry';
            return apiFetch(path, {}, token);
        },
        install: async (mcpSlug: string, config?: any, token?: string) => {
            return apiFetch('/api/mcp/install', {
                method: 'POST',
                body: JSON.stringify({ mcp_slug: mcpSlug, config })
            }, token);
        },
        getInstalled: async (token?: string): Promise<any[]> => {
            return apiFetch('/api/mcp/installed', {}, token);
        }
    }
};
